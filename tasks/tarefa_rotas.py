from crewai import Task


def criar_tarefa_rotas(agent):
    return Task(
        description="""
Com base no relatório do sensor_agent, divida as caçambas entre 3 caminhões.

Sua tarefa é:
- Distribuir as caçambas entre os 3 caminhões
- Garantir equilíbrio de carga (quantidade e prioridade)
- Minimizar distância total percorrida por cada caminhão

Para cada caminhão, gere:
- Lista de caçambas atribuídas
- Ordem de coleta (rota)

Ao final:
- Apresente rota separada para Caminhão 1, 2 e 3
- Justifique a divisão feita
- Tudo em no máximo 1000 caracteres
""",
        expected_output="""
Plano de rotas resumido e dividido em 3 partes:
- Rota do Caminhão 1
- Rota do Caminhão 2
- Rota do Caminhão 3
- Justificativa da divisão
""",
        agent=agent,
    )