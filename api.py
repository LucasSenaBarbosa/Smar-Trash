"""
api.py — Backend FastAPI para o EcoTrack
Roda a Crew e transmite os logs dos agentes em tempo real via SSE.
"""

import os
import sys
import json
import queue
import threading
import io
from contextlib import redirect_stdout
from dotenv import find_dotenv, load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse, FileResponse
from pathlib import Path

load_dotenv(find_dotenv())

groq_key = os.getenv("GROQ_API_KEY", "").strip()
if not groq_key:
    raise EnvironmentError(
        "\n❌ GROQ_API_KEY não encontrada ou está vazia!\n"
        "   1. Verifique se o arquivo .env está na raiz do projeto.\n"
        "   2. Adicione: GROQ_API_KEY=<sua-chave-válida>\n"
        "   3. Reinicie o terminal/IDE se estiver usando variáveis de ambiente do sistema.\n"
    )

# Log de diagnóstico (mascarado) para o backend
def _mask_key(k: str) -> str:
    if not k:
        return "(vazia)"
    if len(k) <= 8:
        return k
    return f"{k[:4]}...{k[-4:]} (len={len(k)})"

print(f"[diagnóstico - api] GROQ_API_KEY carregada: {_mask_key(groq_key)}; prefix_ok={groq_key.startswith('gsk_')}")

app = FastAPI(title="EcoTrack API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Estado global da operação ──────────────────────────────────────────────────
state = {
    "running": False,
    "done": False,
    "resultado_final": None,
    "log_queue": queue.Queue(),
}


# ── Captura de stdout para transformar em eventos SSE ─────────────────────────
class QueueWriter(io.TextIOBase):
    """Redireciona writes para a fila de logs."""

    def __init__(self, q: queue.Queue):
        self.q = q

    def write(self, text: str):
        if text and text.strip():
            self.q.put({"type": "log", "text": text.rstrip()})
        return len(text)

    def flush(self):
        pass


def _run_crew_thread():
    """Executa a Crew em thread separada e captura todo o output."""
    from crew import criar_crew

    state["running"] = True
    state["done"] = False
    state["resultado_final"] = None

    writer = QueueWriter(state["log_queue"])

    try:
        state["log_queue"].put({"type": "status", "text": "iniciando"})
        crew = criar_crew()

        # Redireciona stdout para capturar logs do CrewAI
        with redirect_stdout(writer):
            resultado = crew.kickoff()

        state["resultado_final"] = str(resultado)
        state["log_queue"].put({"type": "resultado", "text": str(resultado)})
        state["log_queue"].put({"type": "status", "text": "concluido"})

    except Exception as e:
        state["log_queue"].put({"type": "erro", "text": str(e)})
        state["log_queue"].put({"type": "status", "text": "erro"})

    finally:
        state["running"] = False
        state["done"] = True
        state["log_queue"].put(None)  # sentinel — fim do stream


# ── Endpoints ──────────────────────────────────────────────────────────────────
@app.post("/api/iniciar")
def iniciar_operacao():
    """Inicia a Crew em background."""
    if state["running"]:
        return {"ok": False, "msg": "Operação já em andamento."}

    # Limpa fila anterior
    while not state["log_queue"].empty():
        try:
            state["log_queue"].get_nowait()
        except queue.Empty:
            break

    t = threading.Thread(target=_run_crew_thread, daemon=True)
    t.start()
    return {"ok": True, "msg": "Operação iniciada."}


@app.get("/api/stream")
def stream_logs():
    """SSE — transmite logs em tempo real."""

    def event_generator():
        while True:
            item = state["log_queue"].get()
            if item is None:
                yield "data: {\"type\": \"fim\"}\n\n"
                break
            yield f"data: {json.dumps(item, ensure_ascii=False)}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )


@app.get("/api/status")
def status():
    return {
        "running": state["running"],
        "done": state["done"],
        "resultado": state["resultado_final"],
    }


# ── Serve o frontend ──────────────────────────────────────────────────────────
frontend_dir = Path(__file__).parent / "frontend"
if frontend_dir.exists():
    app.mount("/", StaticFiles(directory=str(frontend_dir), html=True), name="frontend")


# ── Entrypoint ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=False)