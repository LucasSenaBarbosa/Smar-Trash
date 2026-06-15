from crewai import Agent


def criar_sensor_vida_agent(llm):
    return Agent(
        role="Especialista em Sensores Biológicos",
        goal=(
            "Analisar sinais térmicos, sonoros e ambientais "
            "detectando humanos e animais."
        ),
        backstory=(
            "Você é um sistema avançado de detecção biológica, especializado em "
            "interpretar dados de sensores para identificar a presença de vida. "
            "Sua experiência reside em distinguir padrões térmicos e sonoros de "
            "humanos e animais em diversos ambientes."
        ),
        llm=llm,
        verbose=True,
    )


def criar_visao_agent(llm):
    return Agent(
        role="Especialista em Visão Computacional",
        goal="Processar imagens IR e detectar silhuetas, temperatura corporal e movimentos.",
        backstory=(
            "Você é um especialista em visão computacional, treinado para analisar "
            "imagens infravermelhas. Sua função é identificar e interpretar silhuetas, "
            "medir temperaturas corporais e detectar padrões de movimento em ambientes diversos."
        ),
        llm=llm,
        verbose=True,
    )


def criar_seguranca_vida_agent(llm):
    return Agent(
        role="Supervisor de Segurança Humana",
        goal=(
            "Bloquear compactação quando houver risco biológico ou presença de seres vivos "
            "e emitir alerta para o motorista e a central."
        ),
        backstory=(
            "Você é o supervisor de segurança humana, responsável por monitorar as caçambas "
            "de lixo em tempo real para detectar qualquer sinal de vida. Sua principal missão "
            "é impedir a compactação se houver risco biológico ou presença de seres vivos, "
            "emitindo alertas imediatos aos motoristas e à central de operações."
        ),
        llm=llm,
        verbose=True,
    )


def criar_relatorio_emergencia_agent(llm):
    return Agent(
        role="Analista de Incidentes Operacionais",
        goal="Gerar relatórios detalhados dos eventos de segurança detectados no caminhão.",
        backstory=(
            "Especialista em auditoria operacional, segurança biológica e "
            "rastreabilidade de incidentes."
        ),
        llm=llm,
        verbose=True,
    )