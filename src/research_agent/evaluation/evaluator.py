from pathlib import Path
from src.research_agent.agent import (create_research_agent, create_user_proxy, register_tools)
from src.research_agent.evaluation.test_prompts import EVALUATION_PROMPTS


RESULTS_DIR = Path("results")
RESULTS_FILE = RESULTS_DIR / "evaluation_outputs.md"


def run_evaluation() -> None:
    """
    Run the Research Scout Agent on all evaluation prompts and save the outputs.

    This evaluator is semi-automatic:
    - It runs each test prompt through the AutoGen agent.
    - It stores the full output in a Markdown file.
    """

    RESULTS_DIR.mkdir(exist_ok=True)

    with RESULTS_FILE.open("w", encoding="utf-8") as file:
        file.write("# Evaluation Outputs\n\n")
        file.write(
            "This file contains the final agent outputs from running the "
            "Research Scout Agent on the evaluation prompt set.\n\n"
        )

        for test_case in EVALUATION_PROMPTS:
            prompt_id = test_case["id"]
            category = test_case["category"]
            prompt = test_case["prompt"]
            expected_behavior = test_case["expected_behavior"]

            print(f"Running evaluation prompt {prompt_id}: {category}")

            output = run_single_prompt(prompt)

            file.write(f"## Prompt {prompt_id}: {category}\n\n")

            file.write("### Prompt\n\n")
            file.write(f"{prompt}\n\n")

            file.write("### Expected behavior\n\n")
            file.write(f"{expected_behavior}\n\n")

            file.write("### Agent output\n\n")
            file.write("```text\n")

            file.write(output)
            file.write("\n```\n\n")

    print(f"Evaluation outputs saved to {RESULTS_FILE}")


def run_single_prompt(prompt: str) -> str:
    """
    Run one evaluation prompt through the AutoGen agent.
    """

    research_agent = create_research_agent()
    user_proxy = create_user_proxy()

    register_tools(
        research_agent=research_agent,
        user_proxy=user_proxy,
    )

    chat_result = user_proxy.initiate_chat(
        research_agent,
        message=prompt,
        max_turns=3,
    )

    return chat_result.summary.strip()


if __name__ == "__main__":
    run_evaluation()