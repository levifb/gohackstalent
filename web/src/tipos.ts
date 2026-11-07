export type Alerta = {
  codigo: string;
  gravidade: "bloqueio" | "aprovacao" | "correcao" | "atencao";
  evidencia: string;
  regra: string;
  acionar: string[];
  valor_corrigido: number | null;
  contestavel: boolean;
};

export type Decisao = {
  diagnostico: string;
  acao: string;
  valor_corrigido: number | null;
  acionar: string[];
  alertas_descartados: string[];
  confianca: number;
  motivo: string;
  evidencias: string[];
  instrucao_suspeita_no_texto: boolean;
};

export type Item = {
  titulo_id: string;
  lote: string;
  fornecedor_id: string;
  fornecedor: string;
  categoria: string;
  valor: number;
  vencimento: string;
  forma: string;
  lancado_por: string;
  decisao: Decisao;
  origem_decisao: "regras" | "modelo" | "trava" | "revisao_humana";
  fila_humana: boolean;
  pessoas: { id: string; nome: string }[];
  etapas: {
    triagem: { alertas: Alerta[]; precisa_analise: boolean };
    dossie?: { fontes: string[] };
    analise?: { cache: boolean; tentativas: number; erro: string | null; proposta: Decisao | null };
    trava: { acionada: boolean; motivo: string | null };
    execucao: { acao: string; simulada: boolean; sai_no_lote: boolean; valor_que_sai: number };
  };
};

export type Resumo = {
  titulos: number;
  valor_total: number;
  resolvidos_sozinho: number;
  na_fila_humana: number;
  liberados: number;
  valor_liberado: number;
  retidos: number;
  valor_retido: number;
  analisados_pelo_modelo: number;
  travas_acionadas: number;
  por_acao: Record<string, { n: number; valor: number }>;
  por_pessoa: Record<string, number>;
};

export type Lote = {
  lote: string;
  banco: string;
  data: string;
  fechamento: string;
  modo: string;
  resumo: Resumo;
  itens: Item[];
};

export type EmailSentinela = {
  comunicacao_id: string;
  data_hora: string;
  remetente: string;
  assunto: string;
  texto: string;
  fornecedor: string | null;
  remetente_no_cadastro: boolean;
  acao: string;
  acionar: string[];
  motivo: string;
  jev: { categoria: string; confianca: number; instrucao_ao_sistema: number; pressao_ou_credencial: number } | null;
};

export type Resultado = {
  sentinela?: { resumo: { emails: number; por_acao: Record<string, number>; para_humano: number }; itens: EmailSentinela[] };
  gerado_em: string;
  agora_ficticio: string;
  modo: string;
  lotes: Lote[];
  semana: Resumo;
  uso_modelo: Record<string, number>;
  segundos: number;
};
