from crewai import Task


def criar_tarefa_sensor_vida(agent):
    return Task(
        description="""
Analise os sensores do sistema de segurança biológica.

Entradas:

Temperatura IR: 38.4 C
Sensor térmico: presença detectada
Som: latido identificado
Movimento: positivo
Status caminhão: 72% ocupado

Objetivo:
1. Verificar risco biológico
2. Determinar classe:
   - humano
   - animal
   - falso positivo
3. Acionar medidas:
   - bloquear compactação
   - emitir alerta
   - registrar evento
4. Gerar relatório operacional completo.
""",
        expected_output="RELATÓRIO DE EMERGÊNCIA COMPLETO",
        agent=agent,
    )


def criar_tarefa_relatorio_emergencia(agent):
    return Task(
        description="""
Com base no alerta do sensor de vida, gere relatório completo contendo:
- horário
- localização
- sensores acionados
- temperatura detectada
- presença térmica
- som detectado
- classificação do evento
- ação tomada
- impacto operacional
- status compactador
- recomendação

Formato técnico.
""",
        expected_output="""
RELATÓRIO DE INCIDENTE

ID: INC-001
Horário:
Local:
Sensores:
Temperatura:
Evento:
Classificação:
Ação executada:
Compactador:
Recomendações:
""",
        agent=agent,
    )