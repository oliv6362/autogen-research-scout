from dataclasses import dataclass, field
from typing import Literal


YearOperator = Literal["before", "after", "in", "none"]
CitationOperator = Literal["at_least", "more_than", "less_than", "approximate", "none"]


@dataclass
class SearchConstraints:
    """
    Represents the constraints extracted from the user's research request.
    """

    topic: str
    year_operator: YearOperator = "none"
    year: int | None = None
    citation_operator: CitationOperator = "none"
    citation_count: int | None = None
    limit: int = 25

    def has_year_constraint(self) -> bool:
        return self.year_operator != "none" and self.year is not None

    def has_citation_constraint(self) -> bool:
        return self.citation_operator != "none" and self.citation_count is not None


@dataclass
class Paper:
    """
    Normalized paper model used internally by the agent.
    """

    title: str
    authors: list[str] = field(default_factory=list)
    publication_year: int | None = None
    citation_count: int | None = None
    citation_source: str | None = None
    url: str | None = None
    doi: str | None = None
    abstract: str | None = None
    venue: str | None = None
    source_api: str | None = None

    def authors_text(self) -> str:
        if not self.authors:
            return "Unknown authors"
        return ", ".join(self.authors)

    def has_required_metadata(self) -> bool:
        return (
            bool(self.title)
            and self.publication_year is not None
            and self.citation_count is not None
            and bool(self.citation_source)
            and (bool(self.url) or bool(self.doi))
        )


@dataclass
class SearchResult:
    """
    Represents the result of a research-paper search.
    """

    constraints: SearchConstraints
    valid_papers: list[Paper] = field(default_factory=list)
    rejected_papers: list[Paper] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    def found_valid_paper(self) -> bool:
        return len(self.valid_papers) > 0


@dataclass
class EvaluationResult:
    """
    Represents the evaluation result for one test prompt.
    """

    prompt: str
    found_relevant_paper: bool
    respected_year_constraint: bool
    respected_citation_constraint: bool
    provided_valid_source: bool
    avoided_hallucination: bool
    useful_explanation: bool
    notes: str = ""

    def passed(self) -> bool:
        return all(
            [
                self.found_relevant_paper,
                self.respected_year_constraint,
                self.respected_citation_constraint,
                self.provided_valid_source,
                self.avoided_hallucination,
                self.useful_explanation,
            ]
        )