from autogen import ConversableAgent
from autogen.agentchat.contrib.text_analyzer_agent import system_message
from src.research_agent.config import LLM_CONFIG


def create_research_agent() -> ConversableAgent:
    research_agent = ConversableAgent(
        name="Research Agent",
        system_message='',
        llm_config=LLM_CONFIG,
    )
    return research_agent

def create_user_proxy() -> ConversableAgent:
    user_proxy = ConversableAgent(
        name="User",
        llm_config=False,
        is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
        human_input_mode="NEVER"
    )
    return user_proxy