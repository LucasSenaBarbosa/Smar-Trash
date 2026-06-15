from crewai import Agent


def criar_rotas_agent(llm):
    return Agent(
        role="Especialista de Logística e Dados",
        goal=(
            "De acordo com o relatório do sensor_agent, gerar positivamente a iniciação "
            "de rota com o cálculo otimizado, supervisionando os motoristas e passando "
            "o relatório ao supervisor."
        ),
        backstory="Formado em logística e ADM, com vasta experiência em otimização de rotas urbanas.",
        llm=llm,
        verbose=True,
    )