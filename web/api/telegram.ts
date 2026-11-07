// Webhook do bot do Telegram: recebe os cliques nos botões da fila de aprovação e responde no chat.
// Só aceita chamadas com o segredo configurado no setWebhook (header X-Telegram-Bot-Api-Secret-Token).
// Ações simuladas: registra a decisão na própria mensagem, aplicando as regras de alçada e aprovação dupla.

const TG = () => `https://api.telegram.org/bot${process.env.TELEGRAM_BOT_TOKEN}`;

async function tg(metodo: string, corpo: Record<string, unknown>) {
  await fetch(`${TG()}/${metodo}`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(corpo) });
}

function hora() {
  return new Date().toLocaleTimeString("pt-BR", { hour: "2-digit", minute: "2-digit", timeZone: "America/Fortaleza" });
}

function resposta(acao: string, titulo: string, extra: string | undefined, quem: string): { aviso: string; linha: string } {
  if (acao === "ap") return { aviso: "Aprovado", linha: `✅ Aprovado por ${quem} às ${hora()} (simulado). ${titulo} volta para o lote.` };
  if (acao === "rc") return { aviso: "Recusado", linha: `⛔ Recusado por ${quem} às ${hora()} (simulado). ${titulo} fica fora do lote.` };
  if (acao === "mr") return { aviso: "Mantido retido", linha: `🔒 ${quem} confirmou a retenção às ${hora()} (simulado). ${titulo} não sai no lote.` };
  // liberar um título retido: a política não deixa uma pessoa sozinha liberar caso de golpe ou troca bancária
  if (extra === "bloquear_titulo")
    return {
      aviso: "Exige aprovação dupla",
      linha: `⚠️ ${quem} pediu para liberar ${titulo}, mas título bloqueado por suspeita de golpe só sai com aprovação dupla (coordenadora + diretora) e confirmação pelo telefone anterior do cadastro. Pedido registrado (simulado).`,
    };
  return { aviso: "Liberação registrada", linha: `🟢 ${quem} liberou ${titulo} às ${hora()} (simulado); a decisão fica no log de auditoria.` };
}

export async function POST(req: Request): Promise<Response> {
  if (req.headers.get("x-telegram-bot-api-secret-token") !== process.env.TELEGRAM_WEBHOOK_SECRET) {
    return new Response("forbidden", { status: 403 });
  }
  const u: any = await req.json().catch(() => ({}));
  const cq = u.callback_query;
  if (cq?.data && cq.message) {
    const [acao, titulo, extra] = String(cq.data).split(":");
    const quem = cq.from?.first_name ?? "alguém";
    const { aviso, linha } = resposta(acao, titulo, extra, quem);
    await tg("answerCallbackQuery", { callback_query_id: cq.id, text: aviso });
    await tg("editMessageText", {
      chat_id: cq.message.chat.id,
      message_id: cq.message.message_id,
      text: `${cq.message.text}\n\n${linha}`,
      reply_markup: { inline_keyboard: [] },
    });
  } else if (u.message?.text) {
    await tg("sendMessage", {
      chat_id: u.message.chat.id,
      text: "Sou o Guarda do Lote. Antes de cada fechamento eu confiro os títulos do lote e mando aqui os casos que precisam de uma pessoa. Painel: https://guarda-do-lote.vercel.app",
    });
  }
  return Response.json({ ok: true });
}
