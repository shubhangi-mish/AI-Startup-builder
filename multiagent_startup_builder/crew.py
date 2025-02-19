from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from multiagent_startup_builder.memory import MemoryManager
import yaml
import os
import litellm
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("GEMINI_MODEL")

# ✅ Set up LiteLLM to use Gemini
litellm.model_list.append({
    "model_name": MODEL_NAME,
    "litellm_params": {"api_key": API_KEY, "temperature": 0.7},
    "provider":"google"})

@CrewBase
class MultiagentStartupBuilder():
    """MultiagentStartupBuilder crew with iterative memory & user feedback."""

    def __init__(self):
        with open('multiagent_startup_builder/config/agents.yaml', 'r') as f:
            self.agents_config = yaml.safe_load(f)
        print("Loaded Agents Config:", self.agents_config)

        with open('multiagent_startup_builder/config/tasks.yaml', 'r') as f:
            self.tasks_config = yaml.safe_load(f)
        print("Loaded Tasks Config:", self.tasks_config)

        self.memory = MemoryManager(short_term_rounds=5)

    @agent
    def technologist(self) -> Agent:
        config = self.agents_config["technologist"]
        return Agent(
            name=config["name"],
            role=config["role"],
            goal=config["goal"],
            llm=MODEL_NAME,
            verbose=True,
            memory=self.memory.load("technologist"),
            backstory="An AI-driven expert in modern technology stacks and system architectures."
        )

    @agent
    def marketer(self) -> Agent:
        config = self.agents_config["marketer"]
        return Agent(
            name=config["name"],
            role=config["role"],
            goal=config["goal"],
            llm=MODEL_NAME,
            verbose=True,
            memory=self.memory.load("marketer"),
            backstory="A data-driven marketing strategist specializing in user acquisition and brand positioning."
        )

    @agent
    def designer(self) -> Agent:
        config = self.agents_config["designer"]
        return Agent(
            name=config["name"],
            role=config["role"],
            goal=config["goal"],
            llm=MODEL_NAME,
            verbose=True,
            memory=self.memory.load("designer"),
            backstory="A creative mind focused on delivering intuitive and user-friendly design experiences."
        )

    @agent
    def product_manager(self) -> Agent:
        config = self.agents_config["product_manager"]
        return Agent(
            name=config["name"],
            role=config["role"],
            goal=config["goal"],
            llm=MODEL_NAME,
            verbose=True,
            memory=self.memory.load("product_manager"),
            backstory="A visionary leader ensuring a clear product roadmap from ideation to execution."
        )

    @task
    def tech_stack_analysis(self) -> Task:
        config = self.tasks_config["Tech Stack Analysis"]
        return Task(
            name=config["name"],
            description=config["description"],
            expected_output=config["expected_output"],
            agent=self.technologist(),
            depends_on=[self.business_roadmap()]
            
        )

    @task
    def market_research(self) -> Task:
        config = self.tasks_config["Market Research"]
        return Task(
            name=config["name"],
            description=config["description"],
            expected_output=config["expected_output"],
            agent=self.marketer(),
            depends_on=config.get("dependencies", [])
        )

    @task
    def ui_ux_planning(self) -> Task:
        config = self.tasks_config["UI/UX Planning"]
        return Task(
            name=config["name"],
            description=config["description"],
            expected_output=config["expected_output"],
            agent=self.designer(),
            depends_on=[self.tech_stack_analysis()]
        )

    @task
    def business_roadmap(self) -> Task:
        config = self.tasks_config["Business Roadmap"]
        return Task(
            name=config["name"],
            description=config["description"],
            expected_output=config["expected_output"],
            agent=self.product_manager(),
            depends_on=[self.market_research()]
        )

    @crew
    def tech_crew(self) -> Crew:
        return Crew(
            agents=[self.technologist()],
            tasks=[self.tech_stack_analysis()],
            process=Process.sequential,
            verbose=True
        )

    @crew
    def marketing_crew(self) -> Crew:
        return Crew(
            agents=[self.marketer()],
            tasks=[self.market_research()],
            process=Process.sequential,
            verbose=True
        )

    @crew
    def design_crew(self) -> Crew:
        return Crew(
            agents=[self.designer()],
            tasks=[self.ui_ux_planning()],
            process=Process.sequential,
            verbose=True
        )

    @crew
    def product_crew(self) -> Crew:
        return Crew(
            agents=[self.product_manager()],
            tasks=[self.business_roadmap()],
            process=Process.sequential,
            verbose=True
        )

    def run_all_crews(self):
        """Runs all crews independently and collects feedback separately."""
        crews = {
            "Tech Crew": self.tech_crew(),
            "Marketing Crew": self.marketing_crew(),
            "Design Crew": self.design_crew(),
            "Product Crew": self.product_crew()
        }
        return crews
'''
        for crew_name, crew in crews.items():
            print(f"\n🚀 **Executing {crew_name}**")
            output = crew.kickoff()
            print(type(output))

            print(f"\n📝 **{crew_name} Output:**")
            print(output)

            # Store output in respective memory
            self.memory.update_memory(crew_name, output)

            # Collect feedback for each crew separately
            user_feedback = input(f"\n💡 Enter feedback for {crew_name}: ")
            self.memory.integrate_feedback(user_feedback)
            self.memory.update_memory(crew_name, user_feedback)

        print("\n✅ **All Crews Executed and Feedback Integrated!**")    

'''
