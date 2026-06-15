import os
from dotenv import find_dotenv, load_dotenv

# Carrega o .env antes de qualquer import do CrewAI
load_dotenv(find_dotenv())

# Validação antecipada da chave
groq_api_key = os.getenv("GROQ_API_KEY", "").strip()
if not groq_api_key:
    raise EnvironmentError(
        "\n❌ GROQ_API_KEY não encontrada ou está vazia!\n"
        "   1. Verifique se o arquivo .env existe na raiz do projeto\n"
        "   2. Adicione: GROQ_API_KEY=<sua-chave-válida>\n"
        "   3. Se estiver usando variável de ambiente no shell, reinicie o terminal/IDE\n"
    )

# Log de diagnóstico (mascarado): mostra se a chave foi carregada e formato esperado
def _mask_key(k: str) -> str:
    if not k:
        return "(vazia)"
    if len(k) <= 8:
        return k
    return f"{k[:4]}...{k[-4:]} (len={len(k)})"

print(f"[diagnóstico] GROQ_API_KEY carregada: {_mask_key(groq_api_key)}; prefix_ok={groq_api_key.startswith('gsk_')}")

from crew import criar_crew


def main():
    print("\n" + "=" * 60)
    print("🚛  EcoTrack — Sistema Inteligente de Coleta de Lixo")
    print("=" * 60 + "\n")

    crew = criar_crew()
    resultado = crew.kickoff()

    print("\n" + "=" * 60)
    print("✅  RESULTADO FINAL DA OPERAÇÃO")
    print("=" * 60)
    print(resultado)


if __name__ == "__main__":
    main()