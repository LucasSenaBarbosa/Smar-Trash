from crewai import Task


def criar_tarefa_motorista(numero: int, agent):
    return Task(
        description=(
            f"Execute a rota atribuída ao Caminhão {numero} e gere relatório da coleta. "
            "Tudo em no máximo 1000 caracteres."
        ),
        expected_output=f"Relatório resumido do Caminhão {numero}",
        agent=agent,
    )


def criar_tarefa_relatorio(agent):
    return Task(
        description="""
Analise os relatórios gerados pelos caminhões de coleta (Caminhão 1, 2 e 3).

Cada relatório contém:
- Lista de caçambas coletadas
- Caçambas não atendidas
- Problemas encontrados durante a rota

Sua tarefa é:
- Consolidar todas as informações em um único relatório geral
- Calcular:
    - Total de caçambas coletadas
    - Total de caçambas não coletadas
- Identificar padrões e problemas recorrentes:
    - Regiões com maior volume de lixo
    - Dificuldades frequentes (acesso, trânsito, etc.)
- Avaliar a eficiência da operação:
    - A divisão entre os caminhões foi equilibrada?
    - Houve sobrecarga em algum caminhão?
- Gerar insights estratégicos:
    - Sugestões para melhorar a coleta
    - Possíveis otimizações de rota
    - Necessidade de mais caminhões ou redistribuição

Ao final, produza um relatório claro, organizado e objetivo em linguagem profissional.
Máximo de 1000 caracteres.
""",
        expected_output="""
Relatório gerencial completo contendo:
- Resumo da operação
- Métricas gerais (coletas realizadas e pendentes)
- Principais problemas identificados
- Análise de eficiência dos caminhões
- Recomendações estratégicas para melhoria
""",
        agent=agent,
    )
