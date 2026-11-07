// POST /api/reprocessar { titulo_id, demo? } — reanalisa um título com o modelo, ao vivo, e aplica a trava da política.
// O token do AI Proxy fica só no servidor (vercel env). Se a rede ou o proxy falharem, devolve a decisão em cache.
import dados from "./_casos.js";

export const config = { maxDuration: 60 };

const ACOES = ["liberar", "corrigir_lancamento", "cancelar_titulo", "retirar_do_lote", "bloquear_titulo", "solicitar_aprovacao", "revisao_humana"];
const PAGAM = new Set(["liberar", "corrigir_lancamento"]);
const ALCADA_ANALISTA = 5000;

type Alerta = { codigo: string; gravidade: string; contestavel: boolean; valor_corrigido: number | null };
type Decisao = Record<string, any> & { acao: string; acionar: string[]; valor_corrigido: number | null };

function extrairJson(texto: string): any {
  const ini = texto.indexOf("{");
  const fim = texto.lastIndexOf("}");
  return JSON.parse(texto.slice(ini, fim + 1));
}

function validar(d: any): string | null {
  if (!d || typeof d !== "object") return "não é objeto";
  if (!ACOES.includes(d.acao)) return `acao inválida: ${d.acao}`;
  if (typeof d.confianca !== "number" || d.confianca < 0 || d.confianca > 1) return "confianca fora de 0..1";
  if (typeof d.motivo !== "string" || !d.motivo) return "motivo vazio";
  if (!Array.isArray(d.acionar ?? [])) return "acionar não é lista";
  return null;
}

function travar(d: Decisao, alertas: Alerta[], valor: number, base: Decisao): { final: Decisao; motivo: string | null } {
  const descartados = new Set<string>(d.alertas_descartados ?? []);
  const vc = d.valor_corrigido;
  const resolvido = (a: Alerta) => d.acao === "corrigir_lancamento" && a.valor_corrigido != null && vc != null && Math.abs(vc - a.valor_corrigido) <= 0.1;
  const duros = alertas.filter((a) => ["bloqueio", "aprovacao"].includes(a.gravidade) && !(a.contestavel && descartados.has(a.codigo)) && !resolvido(a));
  const descartouDuro = [...descartados].filter((c) => alertas.some((a) => a.codigo === c && !a.contestavel));
  if (descartouDuro.length) return { final: base, motivo: `o modelo tentou descartar alerta que só uma pessoa resolve (${descartouDuro.join(", ")})` };
  if (PAGAM.has(d.acao) && duros.length) return { final: base, motivo: `o modelo propôs '${d.acao}' com alerta ${duros[0].codigo} (${duros[0].gravidade}) ativo` };
  if (d.acao === "corrigir_lancamento" && (vc == null || Math.max(valor, vc) > ALCADA_ANALISTA)) return { final: base, motivo: "correção acima da alçada do analista (R$ 5 mil) ou sem valor" };
  if (d.acao === "cancelar_titulo" && valor > ALCADA_ANALISTA) return { final: base, motivo: "cancelamento acima da alçada do analista (R$ 5 mil)" };
  return { final: d, motivo: null };
}

async function chamarModelo(usuario: string, extra = ""): Promise<{ texto: string; uso: any; modelo: string }> {
  const url = (process.env.AI_PROXY_URL || "https://ai-proxy.gogroupbr.com/v1").replace(/\/$/, "");
  const chave = process.env.AI_PROXY_API_KEY;
  const modelo = process.env.AI_MODEL || "gpt-6-astra";
  if (!chave) throw new Error("AI_PROXY_API_KEY não configurada");
  const r = await fetch(`${url}/chat/completions`, {
    method: "POST",
    headers: { Authorization: `Bearer ${chave}`, "Content-Type": "application/json" },
    body: JSON.stringify({ model: modelo, temperature: 0, messages: [{ role: "system", content: dados.sistema }, { role: "user", content: usuario + extra }] }),
    signal: AbortSignal.timeout(45000),
  });
  if (!r.ok) throw new Error(`proxy HTTP ${r.status}`);
  const j = await r.json();
  const u = j.usage ?? {};
  console.log(`💲 ${r.headers.get("x-model-served") ?? j.model} · entrada ${u.prompt_tokens} tok · saída ${u.completion_tokens} tok · sem preço por chamada`);
  return { texto: j.choices[0].message.content, uso: u, modelo: r.headers.get("x-model-served") ?? j.model ?? modelo };
}

export async function POST(req: Request): Promise<Response> {
  const ini = Date.now();
  let corpo: any = {};
  try {
    corpo = await req.json();
  } catch {
    return Response.json({ erro: "corpo inválido" }, { status: 400 });
  }
  const caso = (dados.casos as Record<string, any>)[corpo.titulo_id];
  if (!caso) return Response.json({ erro: "título não analisado pelo modelo neste lote" }, { status: 404 });

  const emCache = (motivo: string) =>
    Response.json({ origem: "cache", aviso: motivo, proposta: caso.cache, final: caso.final_cache, trava: null, ms: Date.now() - ini });
  if (corpo.demo) return emCache("modo demo ligado");

  let extra = "";
  for (let tentativa = 1; tentativa <= 2; tentativa++) {
    try {
      const { texto, uso, modelo } = await chamarModelo(caso.usuario, extra);
      const d = extrairJson(texto);
      const erro = validar(d);
      if (erro) {
        extra = `\n\nSua resposta anterior não passou na validação: ${erro}. Responda de novo só com o JSON válido.`;
        continue;
      }
      d.titulo_id = corpo.titulo_id;
      d.acionar = d.acionar ?? [];
      const { final, motivo } = travar(d, caso.alertas, caso.valor, { ...d, ...caso.base });
      return Response.json({ origem: "ao_vivo", modelo, tentativas: tentativa, uso, proposta: d, final, trava: motivo, ms: Date.now() - ini });
    } catch (e: any) {
      return emCache(`modelo indisponível (${String(e?.message ?? e).slice(0, 80)}); resposta em cache`);
    }
  }
  return Response.json({
    origem: "revisao_humana",
    final: { acao: "revisao_humana", acionar: ["PS01"], motivo: "Saída do modelo inválida duas vezes; caso vai para a coordenadora." },
    trava: null,
    ms: Date.now() - ini,
  });
}
