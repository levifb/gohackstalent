import { useEffect, useState } from "react";
import Historia from "./Historia";
import Painel from "./Painel";

// "#painel" abre o painel detalhado do agente; o resto é a história.
export default function App() {
  const [rota, setRota] = useState(() => (location.hash.startsWith("#painel") ? "painel" : "historia"));
  useEffect(() => {
    const f = () => setRota(location.hash.startsWith("#painel") ? "painel" : "historia");
    window.addEventListener("hashchange", f);
    return () => window.removeEventListener("hashchange", f);
  }, []);
  const so = new URLSearchParams(location.search).get("so");
  return (
    <>
      {!so && <nav className="nav">
        <a href="#" className="nav-marca" onClick={() => window.scrollTo({ top: 0 })}>
          <img src="/marca/logo_azul.png" alt="Gogroup" />
          <span>Guarda do Lote</span>
        </a>
        <div className="nav-links">
          <a href="#" className={rota === "historia" ? "ativo" : ""}>
            A história
          </a>
          <a href="#painel" className={rota === "painel" ? "ativo" : ""}>
            Painel do agente
          </a>
          <a href="https://t.me/guardadolote_bot" target="_blank" rel="noreferrer">
            Telegram
          </a>
          <a href="https://github.com/levifb/gohackstalent" target="_blank" rel="noreferrer">
            GitHub
          </a>
        </div>
      </nav>}
      {rota === "painel" ? <Painel /> : <Historia />}
    </>
  );
}
