"""
Evaluation prompts for the Research Scout Agent.

The prompts are designed to test different combinations of:
- broad and narrow research topics
- before, after, and exact publication-year constraints
- minimum, high, low, and approximate citation-count constraints
- ambiguous requests
- cases where no valid paper is expected
"""

EVALUATION_PROMPTS = [
    {
        "id": 1,
        "category": "narrow_topic",
        "prompt": (
            "Find a paper about retrieval-augmented generation published after 2022 "
            "with at least 500 citations. Explain why the paper is relevant and "
            "provide the source of the citation count."
        ),
        "expected_behavior": (
            "Should find a relevant RAG paper after 2022 with at least 500 citations."
        ),
    },
    {
        "id": 2,
        "category": "broad_topic",
        "prompt": (
            "Find a paper about large language models published after 2021 "
            "with at least 100 citations."
        ),
        "expected_behavior": (
            "Should find a relevant paper about large language models after 2021 "
            "with at least 100 citations."
        ),
    },
    {
        "id": 3,
        "category": "before_year_constraint",
        "prompt": (
            "Find a paper about retrieval-augmented generation published before 2021 "
            "with more than 500 citations. Summarize its contribution in 5-7 sentences."
        ),
        "expected_behavior": (
            "Should find a relevant RAG-related paper before 2021 with more than "
            "500 citations, or clearly state that no valid paper was found."
        ),
    },
    {
        "id": 4,
        "category": "exact_year_constraint",
        "prompt": (
            "Find a paper about chain-of-thought prompting published in 2022 with "
            "more than 1000 citations. Explain its main contribution."
        ),
        "expected_behavior": (
            "Should find a chain-of-thought paper from exactly 2022 with more than "
            "1000 citations."
        ),
    },
    {
        "id": 5,
        "category": "after_year_constraint",
        "prompt": (
            "Find a recent paper about AI agents using tools published after 2023 "
            "with at least 50 citations. Explain whether it would be useful for "
            "someone building autonomous software agents."
        ),
        "expected_behavior": (
            "Should find a recent paper about tool-using AI agents after 2023 with "
            "at least 50 citations."
        ),
    },
    {
        "id": 6,
        "category": "high_citation_constraint",
        "prompt": (
            "Find a paper about transformer neural networks published before 2018 "
            "with more than 10000 citations."
        ),
        "expected_behavior": (
            "Should find a highly cited transformer-related paper before 2018, "
            "such as a foundational transformer paper, if returned by the tool."
        ),
    },
    {
        "id": 7,
        "category": "low_minimum_citation_constraint",
        "prompt": (
            "Find a paper about software testing with large language models published "
            "after 2023 with at least 10 citations."
        ),
        "expected_behavior": (
            "Should find a recent software testing and LLM paper after 2023 with "
            "at least 10 citations."
        ),
    },
    {
        "id": 8,
        "category": "citation_approximate",
        "prompt": (
            "Find a research paper about LLM agents for software engineering that "
            "was published after 2022 and has approximately 500 citations. Explain why "
            "the paper is relevant."
        ),
        "expected_behavior": (
            "Should find a paper related to LLM agents or agentic AI in software "
            "engineering, published after 2022, with approximately 500 citations."
        ),
    },
    {
        "id": 9,
        "category": "expected_failure",
        "prompt": (
            "Find a paper about AutoGen agents published after 2023 with more than "
            "10000 citations."
        ),
        "expected_behavior": (
            "This is likely unrealistic. The agent should avoid hallucinating and "
            "state that no valid paper was found if no paper satisfies the constraints."
        ),
    },
    {
        "id": 10,
        "category": "ambiguous_request",
        "prompt": (
            "Find a recent paper about AI agents. Explain why it is relevant."
        ),
        "expected_behavior": (
            "The agent should handle the vague request reasonably, use the tool, "
            "and return a relevant recent AI agents paper with a valid source."
        ),
    },
]