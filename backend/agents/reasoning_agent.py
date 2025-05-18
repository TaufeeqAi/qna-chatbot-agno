from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.models.groq import Groq

class ReasoningAgent:
    """
    Orchestrates different reasoning strategies:
      - chain_of_thought
      - tree_of_thought
      - graph_of_thought
    """

    @staticmethod
    def reason(message: str, context: list, docs: list, mode: str):
        # Choose model (ChatGPT or Grok)
        model = OpenAIChat(id="gpt-4o")  # or Grok(id="grok-beta")
        # Base configuration
        agent = Agent(
            model=model,
            description="Research assistant with deep reasoning",
            knowledge=docs,
            show_tool_calls=True,
            markdown=False
        )
        # Inject context as preamble
        prompt = "\n".join([f"Context: {c}" for c in context]) + f"\nQuestion: {message}"

        # Dispatch reasoning modes
        if mode == "chain_of_thought":
            response = agent.run_chain_of_thought(prompt)
            trace = agent.tool_calls
        elif mode == "tree_of_thought":
            response = agent.run_tree_of_thought(prompt)
            trace = agent.tool_calls
        else:  # graph_of_thought
            response = agent.run_graph_of_thought(prompt)
            trace = agent.tool_calls

        return response, trace
