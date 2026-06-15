from crewai import Agent


def criar_sensor_agent(llm):
    return Agent(
        role="Supervisor de Sensores",
        goal=(
            "Observar os dados dos sensores nas caçambas de lixo "
            "e gerar um relatório de quais caçambas devem ser coletadas."
        ),
        backstory="Formado em logística e ADM, especialista em monitoramento de sensores urbanos.",
        llm=llm,
        verbose=True,
    )