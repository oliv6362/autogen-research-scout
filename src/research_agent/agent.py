from autogen import ConversableAgent
from src.research_agent.config import LLM_CONFIG


def create_research_agent() -> ConversableAgent:
    research_agent = ConversableAgent(
        name="research_agent",
        system_message=(
            "You are an AI research assistant for finding academic research papers. "
            "Your task is to understand the user's request, identify research-paper constraints, "
            "use the available tools to search for candidate papers, and return a structured, "
            "evidence-based answer. "
            "\n\n"
            "You must not invent paper metadata, citation counts, URLs, DOIs, authors, or publication years. "
            "Citation counts must come from an external tool result. "
            "\n\n"
            "When answering, include: "
            "paper title, authors, publication year, citation count, source of the citation count, "
            "paper URL or DOI, and a short explanation of why the paper matches the request. "
            "\n\n"
            "If no paper satisfies the user's constraints, say that no valid paper was found and explain which "
            "constraints could not be satisfied. "
            "\n\n"
            "When the task is complete, end your response with TERMINATE."
        ),
        llm_config=LLM_CONFIG,
    )
    return research_agent

def create_user_proxy() -> ConversableAgent:
    user_proxy = ConversableAgent(
        name="user_proxy",
        llm_config=False,
        is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
        human_input_mode="NEVER"
    )
    return user_proxy