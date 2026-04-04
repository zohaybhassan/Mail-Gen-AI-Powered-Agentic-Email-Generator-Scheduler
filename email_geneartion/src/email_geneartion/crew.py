from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List


@CrewBase
class EmailGeneartion():
    """Crew to generate email content from user topic and uploaded document"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # Agent 1: Extract info from document
    @agent
    def doc_extractor(self) -> Agent:
        return Agent(
            config=self.agents_config['doc_extractor'],  # You must define this in agents.yaml
            verbose=False
        )

    # Agent 2: Generate email
    @agent
    def email_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['email_writer'],  # You must define this in agents.yaml
            verbose=False
        )

    # Task 1: Read and extract important details from document
    @task
    def extract_doc_task(self) -> Task:
        return Task(
            config=self.tasks_config['extract_doc_task'],
            output_key="extracted_info"
        )

    # Task 2: Generate final email using topic + extracted info
    @task
    def generate_email_task(self) -> Task:
        return Task(
            config=self.tasks_config['generate_email_task'],
            context=[self.extract_doc_task()],
            output_file='generated_email.txt'
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=False
        )

