from crewai import Task


def criar_tarefa_sensor(agent):
    return Task(
        description="""
Analise os dados recebidos dos sensores instalados nas 20 caçambas de lixo.

Cada caçamba possui:
- ID da caçamba
- Localização
- Nível de ocupação (%)

Sua tarefa é:
- Identificar quais caçambas precisam de coleta (acima de 70% de capacidade)
- Classificar as caçambas por prioridade:
    - Alta (acima de 90%)
    - Média (70% a 90%)
    - Baixa (abaixo de 70%)
- Gerar uma lista organizada contendo:
    - ID da caçamba
    - Localização
    - Nível de ocupação
    - Prioridade
    - Tudo em no máximo 1000 caracteres
""",
        expected_output="""
Relatório estruturado contendo:
- Classificação por prioridade (alta, média, baixa)
- Destaque para caçambas críticas
- Recomendação de coleta imediata
""",
        agent=agent,
    )