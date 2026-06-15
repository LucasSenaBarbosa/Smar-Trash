from dotenv import find_dotenv, load_dotenv
import os

load_dotenv(find_dotenv())

def _mask_key(k: str) -> str:
    if not k:
        return "(vazia)"
    if len(k) <= 8:
        return k
    return f"{k[:4]}...{k[-4:]} (len={len(k)})"

key = os.getenv("GROQ_API_KEY", "").strip()
print(f"[diagnóstico] GROQ_API_KEY carregada: {_mask_key(key)}; prefix_ok={key.startswith('gsk_')}")

if not key:
    print("Erro: nenhuma chave encontrada. Verifique .env e variáveis do sistema.")
    raise SystemExit(1)

try:
    from groq import Groq
    client = Groq(api_key=key)
    print("Instanciado Groq client com sucesso. Fazendo requisição de teste: client.models.list()")
    models = client.models.list()
    # models is an object; try to show a short summary
    if hasattr(models, 'data'):
        print(f"Resposta: models.data length={len(models.data)}")
    else:
        print(repr(models))
except Exception as e:
    print("Exceção ao testar a chave Groq:", type(e).__name__, str(e))
    raise
