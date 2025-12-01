from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from config import GOOGLE_MODEL, retry_config
from google.adk.agents import Agent, SequentialAgent, ParallelAgent, LoopAgent


def create_root_agent(agent_list: list[Agent]) -> Agent:
    """
    Creates an AggregatorAgent that synthesizes outputs from multiple agents.

    Args:
        agent_list (list[Agent]): List of agents whose outputs need to be aggregated."""
    
    parallel_support_agent = ParallelAgent(
        name="ParallelSupportAgents",
        sub_agents=agent_list)

    # The AggregatorAgent runs *after* the parallel step to synthesize the results.
    # Build the agent references dynamically
    agent_references = "\n        ".join([f"- {agent.name}: ${{{agent.output_key}}}" for agent in agent_list])
    print("✅ agent references created.", agent_references)
    
    aggregator_agent = Agent(
        name="AggregatorAgent",
        model=Gemini(
            model=GOOGLE_MODEL,
            retry_options=retry_config
        ),
        # It uses placeholders to inject the outputs from the parallel agents, which are now in the session state.
        instruction=f"""
        You are the Aggregator Agent. Your task is to compile a concise executive summary
        based on the findings from the following agents:
        {agent_references}
        
        Focus on the key points from each department's response and
        present them in a clear and structured manner.""",
        output_key="executive_support_summary",  # This will be the final output of the entire system.
        tools=[],
    )

    root_agent = SequentialAgent(
        name="RootAgent",
        sub_agents=[parallel_support_agent, aggregator_agent]
    )

    print("✅ root_agent created.")
    return root_agent
