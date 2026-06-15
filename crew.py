import os
from crewai import Crew, LLM, Process

from agents.sensor_agent import criar_sensor_agent
from agents.seguranca_agent import (
    criar_sensor_vida_agent,
    criar_visao_agent,
    criar_seguranca_vida_agent,
    criar_relatorio_emergencia_agent,
)
from agents.rotas_agent import criar_rotas_agent
from agents.motoristas_agents import criar_motorista, criar_relatorio_agent

from tasks.tarefa_sensor import criar_tarefa_sensor
from tasks.tarefa_seguranca import criar_tarefa_sensor_vida, criar_tarefa_relatorio_emergencia
from tasks.tarefa_rotas import criar_tarefa_rotas
from tasks.tarefas_motoristas import criar_tarefa_motorista, criar_tarefa_relatorio


def criar_crew() -> Crew:
    # ── LLM via Groq ──────────────────────────────────────────────────────────
    # O CrewAI aceita o formato "groq/<modelo>" nativamente via LiteLLM.
    # A GROQ_API_KEY é lida automaticamente da variável de ambiente.
    llm = LLM(
        model="groq/llama-3.3-70b-versatile",
        temperature=0.7,
    )

    # ── Agentes ───────────────────────────────────────────────────────────────
    sensor_ag       = criar_sensor_agent(llm)
    sensor_vida_ag  = criar_sensor_vida_agent(llm)
    visao_ag        = criar_visao_agent(llm)
    seguranca_ag    = criar_seguranca_vida_agent(llm)
    relat_emerg_ag  = criar_relatorio_emergencia_agent(llm)
    rotas_ag        = criar_rotas_agent(llm)
    motorista_1_ag  = criar_motorista(1, llm)
    motorista_2_ag  = criar_motorista(2, llm)
    motorista_3_ag  = criar_motorista(3, llm)
    relatorio_ag    = criar_relatorio_agent(llm)

    # ── Tarefas ───────────────────────────────────────────────────────────────
    t_sensor        = criar_tarefa_sensor(sensor_ag)
    t_sensor_vida   = criar_tarefa_sensor_vida(seguranca_ag)
    t_rotas         = criar_tarefa_rotas(rotas_ag)
    t_motorista_1   = criar_tarefa_motorista(1, motorista_1_ag)
    t_motorista_2   = criar_tarefa_motorista(2, motorista_2_ag)
    t_motorista_3   = criar_tarefa_motorista(3, motorista_3_ag)
    t_relatorio     = criar_tarefa_relatorio(relatorio_ag)
    t_relat_emerg   = criar_tarefa_relatorio_emergencia(relat_emerg_ag)

    # ── Crew ──────────────────────────────────────────────────────────────────
    crew = Crew(
        agents=[
            sensor_ag,
            sensor_vida_ag,
            visao_ag,
            seguranca_ag,
            relat_emerg_ag,
            rotas_ag,
            motorista_1_ag,
            motorista_2_ag,
            motorista_3_ag,
            relatorio_ag,
        ],
        tasks=[
            t_sensor,
            t_sensor_vida,
            t_rotas,
            t_motorista_1,
            t_motorista_2,
            t_motorista_3,
            t_relatorio,
            t_relat_emerg,
        ],
        process=Process.sequential,
        verbose=True,
    )

    return crew