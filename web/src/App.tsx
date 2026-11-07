import { useEffect, useMemo, useState } from "react";
import type { Item, Lote, Resultado, Resumo } from "./tipos";

type EvalResumo = {
  n: number;
  tudo_certo: number;
  dinheiro: number;
  em: string;
  placar: Record<"agente" | "assinar_sem_conferir" | "bloquear_todo_alerta", { total: number }>;
};

const brl = (v: number) => v.toLocaleString("pt-BR", { style: "currency", currency: "BRL", maximumFractionDigits: 0 });
const brl2 = (v: number) => v.toLocaleString("pt-BR", { style: "currency", currency: "BRL" });
const pct = (a: number, b: number) => (b ? Math.round((100 * a) / b) : 0);
const dataBR = (iso: string) => iso.split("-").reverse().slice(0, 2).join("/");

const ACAO: Record<string, { rotulo: string; cor: string; ordem: number }> = {
  bloquear_titulo: { rotulo: "Bloqueado", cor: "rosa", ordem: 0 },
  retirar_do_lote: { rotulo: "Retirado do lote", cor: "rosa", ordem: 1 },
  cancelar_titulo: { rotulo: "Cancelado (duplicidade)", cor: "ambar", ordem: 2 },
  revisao_humana: { rotulo: "Revisão humana", cor: "ambar", ordem: 3 },
  solicitar_aprovacao: { rotulo: "Aguarda aprovação", cor: "azul", ordem: 4 },
  corrigir_lancamento: { rotulo: "Corrigido e liberado", cor: "ciano", ordem: 5 },
  liberar: { rotulo: "Liberado", cor: "verde", ordem: 6 },
};

const ORIGEM: Record<string, string> = {
  regras: "regras",
  modelo: "modelo + regras",
  trava: "trava da política",
  revisao_humana: "sem resposta do modelo",
};

function Tag({ acao }: { acao: string }) {
  const a = ACAO[acao] ?? { rotulo: acao, cor: "cinza" };
  return <span className={`tag tag-${a.cor}`}>{a.rotulo}</span>;
}

function Placar({ r, lote }: { r: Resumo; lote?: Lote }) {
  const quando = lote ? `às ${lote.fechamento} de ${dataBR(lote.data)}` : "nos lotes de 03/11 a 13/11";
  const pa = (k: string) => r.por_acao[k] ?? { n: 0, valor: 0 };
  const barrado = ["bloquear_titulo", "retirar_do_lote", "cancelar_titulo", "revisao_humana"].reduce(
    (s, k) => ({ n: s.n + pa(k).n, valor: s.valor + pa(k).valor }),
    { n: 0, valor: 0 }
  );
  const alcada = pa("solicitar_aprovacao");
  return (
    <section className="antes-depois">
      <div className="lado antes">
        <span className="rotulo">ANTES · HOJE</span>
        <p className="grande">{brl(r.valor_total)}</p>
        <p>
          {r.titulos} títulos saem {quando}. O lote é assinado sem abrir título por título.
        </p>
      </div>
      <div className="seta">→</div>
      <div className="lado depois">
        <span className="rotulo">DEPOIS · COM O AGENTE</span>
        <div className="numeros">
          <div>
            <p className="grande">{pct(r.resolvidos_sozinho, r.titulos)}%</p>
            <p>
              resolvidos sozinho ({r.resolvidos_sozinho} de {r.titulos})
            </p>
          </div>
          <div>
            <p className="grande destaque">{brl(barrado.valor)}</p>
            <p>barrados por erro ou golpe ({barrado.n} títulos)</p>
          </div>
          <div>
            <p className="grande">{brl(alcada.valor)}</p>
            <p>conferidos, aguardam a alçada ({alcada.n} títulos)</p>
          </div>
        </div>
      </div>
    </section>
  );
}

function Trilha({ it, fechar }: { it: Item; fechar: () => void }) {
  const e = it.etapas;
  const graves = e.triagem.alertas.filter((a) => a.gravidade !== "atencao");
  const contexto = e.triagem.alertas.filter((a) => a.gravidade === "atencao");
  return (
    <div className="modal-fundo" onClick={fechar}>
      <div className="modal" onClick={(ev) => ev.stopPropagation()}>
        <button className="fechar" onClick={fechar} aria-label="fechar">
          ×
        </button>
        <span className="rotulo">TRILHA DO AGENTE · {it.titulo_id}</span>
        <h2>
          {it.fornecedor} · {brl2(it.valor)}
        </h2>
        <p className="sub">
          {it.categoria} · {it.forma} · vence {it.vencimento} · lançado por {it.lancado_por} · lote {it.lote}
        </p>
        <ol className="etapas">
          <li>
            <b>1. Triagem por regras</b>
            {graves.length === 0 ? (
              <p>Nenhuma divergência: NF, duplicata, cadastro e boleto conferem. Liberado sem chamar o modelo.</p>
            ) : (
              <ul>
                {graves.map((a, i) => (
                  <li key={i}>
                    <span className={`tag tag-${a.gravidade === "bloqueio" ? "rosa" : a.gravidade === "aprovacao" ? "azul" : "ciano"}`}>
                      {a.codigo}
                    </span>{" "}
                    {a.evidencia} <em>Regra: {a.regra}.</em>
                  </li>
                ))}
              </ul>
            )}
            {contexto.length > 0 && <p className="sub">Contexto: {contexto.map((a) => a.evidencia).join(" · ")}</p>}
          </li>
          {e.dossie && (
            <li>
              <b>2. Dossiê</b>
              <p>Ferramentas consultadas: {e.dossie.fontes.join(", ")}.</p>
            </li>
          )}
          {e.analise && (
            <li>
              <b>3. Análise do modelo</b> {e.analise.cache && <span className="tag tag-cinza">resposta em cache</span>}
              {e.analise.proposta ? (
                <>
                  <p>
                    Propôs <Tag acao={e.analise.proposta.acao} /> com confiança {Math.round(e.analise.proposta.confianca * 100)}%
                    {e.analise.proposta.instrucao_suspeita_no_texto && (
                      <span className="tag tag-rosa">texto tentou dar ordem ao agente</span>
                    )}
                  </p>
                  <ul>
                    {e.analise.proposta.evidencias.map((x, i) => (
                      <li key={i}>{x}</li>
                    ))}
                  </ul>
                </>
              ) : (
                <p>Sem resposta válida: {e.analise.erro}</p>
              )}
            </li>
          )}
          <li>
            <b>{e.analise ? "4" : "2"}. Trava da política</b>
            <p>{e.trava.acionada ? `Acionada: ${e.trava.motivo}.` : "A ação respeita alçada, aprovação dupla e regras de bloqueio."}</p>
          </li>
          <li>
            <b>{e.analise ? "5" : "3"}. Ação</b>
            <p>
              <Tag acao={it.decisao.acao} />{" "}
              {e.execucao.sai_no_lote ? `Sai no lote: ${brl2(e.execucao.valor_que_sai)}.` : "Não sai no lote."} (simulada)
            </p>
            <p className="motivo">{it.decisao.motivo}</p>
            {it.pessoas.length > 0 && <p>Acionado: {it.pessoas.map((p) => p.nome).join("; ")}.</p>}
          </li>
        </ol>
      </div>
    </div>
  );
}

function CartaoFila({ it, abrir }: { it: Item; abrir: () => void }) {
  const [resposta, setResposta] = useState<string | null>(null);
  return (
    <article className="cartao">
      <header>
        <Tag acao={it.decisao.acao} />
        <span className="valor">{brl2(it.valor)}</span>
      </header>
      <h3>{it.fornecedor}</h3>
      <p className="motivo">{it.decisao.motivo}</p>
      <p className="pessoas">
        <span className="rotulo">PARA</span> {it.pessoas.map((p) => p.nome).join(" · ") || "Renata Paiva, coordenadora de contas a pagar"}
      </p>
      <footer>
        <button className="link" onClick={abrir}>
          ver trilha do agente
        </button>
        {resposta ? (
          <span className="sub">{resposta} (simulado)</span>
        ) : (
          <span className="botoes">
            <button onClick={() => setResposta("Aprovado")}>Aprovar</button>
            <button className="sec" onClick={() => setResposta("Mantido retido")}>
              Manter retido
            </button>
          </span>
        )}
      </footer>
    </article>
  );
}

export default function App() {
  const [dados, setDados] = useState<Resultado | null>(null);
  const [erro, setErro] = useState<string | null>(null);
  const [loteId, setLoteId] = useState("RM20261103-MER");
  const [filtro, setFiltro] = useState<"todos" | "liberados" | "retidos">("todos");
  const [aberto, setAberto] = useState<Item | null>(null);

  const [evalRes, setEvalRes] = useState<Record<string, EvalResumo> | null>(null);

  useEffect(() => {
    fetch("/resultado.json")
      .then((r) => r.json())
      .then(setDados)
      .catch((e) => setErro(String(e)));
    fetch("/eval.json")
      .then((r) => r.json())
      .then(setEvalRes)
      .catch(() => setEvalRes(null));
  }, []);

  const lote = dados?.lotes.find((l) => l.lote === loteId);
  const itens = useMemo(() => (loteId === "semana" ? dados?.lotes.flatMap((l) => l.itens) : lote?.itens) ?? [], [dados, lote, loteId]);
  const resumo = loteId === "semana" ? dados?.semana : lote?.resumo;
  const fila = itens.filter((i) => i.fila_humana).sort((a, b) => (ACAO[a.decisao.acao]?.ordem ?? 9) - (ACAO[b.decisao.acao]?.ordem ?? 9) || b.valor - a.valor);
  const autonomos = itens.filter((i) => !i.fila_humana && i.decisao.acao !== "liberar");
  const lista = itens
    .filter((i) => (filtro === "todos" ? true : filtro === "liberados" ? i.etapas.execucao.sai_no_lote : !i.etapas.execucao.sai_no_lote))
    .sort((a, b) => (ACAO[a.decisao.acao]?.ordem ?? 9) - (ACAO[b.decisao.acao]?.ordem ?? 9) || b.valor - a.valor);

  if (erro) return <main className="pagina">Não consegui carregar o resultado: {erro}</main>;
  if (!dados || !resumo) return <main className="pagina">Carregando o lote…</main>;

  return (
    <main className="pagina">
      <header className="topo">
        <div>
          <span className="rotulo">GUARDA DO LOTE · AGENTE DE CONTAS A PAGAR</span>
          <h1>O agente confere cada título antes de o dinheiro sair.</h1>
          <p className="sub">
            Para <b>Marcos Teles, tesoureiro</b>. Libera sozinho o que está certo, corrige ou retira o que tem erro e chama a pessoa certa nos casos de risco.
          </p>
        </div>
        <label className="seletor">
          <span className="rotulo">LOTE</span>
          <select value={loteId} onChange={(e) => setLoteId(e.target.value)}>
            {dados.lotes.map((l) => (
              <option key={l.lote} value={l.lote}>
                {l.banco} · {dataBR(l.data)} {l.fechamento} · {l.resumo.titulos} títulos
              </option>
            ))}
            <option value="semana">Semana inteira (03/11 a 13/11)</option>
          </select>
        </label>
      </header>

      <Placar r={resumo} lote={loteId === "semana" ? undefined : lote} />

      {evalRes?.gabarito && (
        <section className="eval">
          <span className="rotulo">CONFERÊNCIA · EVAL</span>
          <p>
            <b>
              {evalRes.gabarito.tudo_certo}/{evalRes.gabarito.n}
            </b>{" "}
            casos do gabarito com ação, pessoa e valor certos
            {evalRes.validacao && (
              <>
                {" "}
                · <b>
                  {evalRes.validacao.tudo_certo}/{evalRes.validacao.n}
                </b>{" "}
                na validação cega
              </>
            )}{" "}
            · custo no placar da área: agente <b>{brl(evalRes.gabarito.placar.agente.total)}</b>, assinar sem conferir{" "}
            <b>{brl(evalRes.gabarito.placar.assinar_sem_conferir.total)}</b>, bloquear todo alerta{" "}
            <b>{brl(evalRes.gabarito.placar.bloquear_todo_alerta.total)}</b>. Primeira versão: 26/29; erros corrigidos no LOG.md.
          </p>
        </section>
      )}

      <section className="como">
        <span className="rotulo">COMO O AGENTE DECIDIU</span>
        <div className="fluxo">
          <div>
            <b>{resumo.titulos}</b> títulos entraram
          </div>
          <div>
            <b>{resumo.titulos - resumo.analisados_pelo_modelo}</b> sem divergência nas regras → liberados
          </div>
          <div>
            <b>{resumo.analisados_pelo_modelo}</b> com alerta → dossiê e análise do modelo
          </div>
          <div>
            <b>{autonomos.length}</b> corrigidos ou cancelados sozinho
          </div>
          <div>
            <b>{resumo.na_fila_humana}</b> para uma pessoa, com motivo
          </div>
        </div>
      </section>

      <section>
        <h2>
          Fila de aprovação <span className="sub">({fila.length})</span>
        </h2>
        {fila.length === 0 ? (
          <p className="sub">Nenhum caso precisa de uma pessoa neste lote.</p>
        ) : (
          <div className="grade">
            {fila.map((it) => (
              <CartaoFila key={it.titulo_id} it={it} abrir={() => setAberto(it)} />
            ))}
          </div>
        )}
      </section>

      <section>
        <div className="titulo-lista">
          <h2>Todos os títulos</h2>
          <div className="filtros">
            {(["todos", "liberados", "retidos"] as const).map((f) => (
              <button key={f} className={filtro === f ? "ativo" : "sec"} onClick={() => setFiltro(f)}>
                {f === "todos" ? "Todos" : f === "liberados" ? "Saem no lote" : "Não saem"}
              </button>
            ))}
          </div>
        </div>
        <table>
          <thead>
            <tr>
              <th>Título</th>
              <th>Fornecedor</th>
              <th className="num">Valor</th>
              <th>Ação</th>
              <th>Quem decidiu</th>
            </tr>
          </thead>
          <tbody>
            {lista.slice(0, 300).map((it) => (
              <tr key={it.titulo_id} onClick={() => setAberto(it)}>
                <td className="mono">{it.titulo_id}</td>
                <td>{it.fornecedor}</td>
                <td className="num">{brl2(it.valor)}</td>
                <td>
                  <Tag acao={it.decisao.acao} />
                </td>
                <td className="sub">{ORIGEM[it.origem_decisao]}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>

      <footer className="rodape">
        Dados fictícios do GoHacks Talent 2026 (situação em 02/11/2026 08:00). Ações simuladas: nenhum sistema real é alterado. Lotes processados pelo agente
        em {dados.gerado_em}; respostas do modelo (gpt-6-astra via AI Proxy) guardadas em cache.
      </footer>

      {aberto && <Trilha it={aberto} fechar={() => setAberto(null)} />}
    </main>
  );
}
