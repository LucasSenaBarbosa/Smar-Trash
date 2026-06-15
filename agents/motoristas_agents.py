from crewai import Agent


def criar_motorista(numero: int, llm):
    return Agent(
        role=f"Motorista de Caminhão de Lixo 0{numero}",
        goal="Executar a rota gerada pelo rotas_agent e coletar as caçambas de lixo.",
        backstory="Experiente motorista de caminhão com carta de motorista categoria D e E.",
        llm=llm,
        verbose=True,
    )


def criar_relatorio_agent(llm):
    return Agent(
        role="Gerente da Empresa de Coleta de Lixo",
        goal="Analisar os relatórios gerados pelos caminhões e gerar um relatório geral.",
        backstory=(
            "Experiente gerente em logística e análise de dados com mais de 30 anos de carreira."
        ),
        llm=llm,
        verbose=True,
    )