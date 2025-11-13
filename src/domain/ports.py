from typing import Protocol
from .models import (
    Query,
    RetrievedData,
    VerifiedData,
    StructuredAnswer,
    AgentState,
)
from .models import SourceProvider


class RetrievalPort(Protocol):
    """
    Retrieves domain-relevant information from ANY external source.
    """
    @property
    def provider(self) -> SourceProvider:
        ...

    def retrieve(self, query: Query) -> RetrievedData:
        ...


class VerificationPort(Protocol):
    """
    Validates correctness, reliability, and consistency of retrieved data.
    """
    def verify(self, data: RetrievedData) -> VerifiedData:
        ...


class SynthesisPort(Protocol):
    """
    Produces a structured answer from verified data.
    """
    def synthesize(self, data: VerifiedData) -> StructuredAnswer:
        ...


class FormattingPort(Protocol):
    """
    Converts a structured answer into final user-facing output (markdown, json…).
    """
    def format(self, answer: StructuredAnswer) -> str:
        ...


class LoopControlPort(Protocol):
    """
    Controls multi-step reasoning in Pro Mode.
    """
    def continue_loop(self, state: AgentState) -> bool:
        ...


class TaskDecompositionPort(Protocol):
    """
    Breaks a complex query into sub-queries.
    """
    def decompose(self, query: Query) -> list[Query]:
        ...


class ConversationPort(Protocol):
    """
    Handles back-and-forth natural-language interaction with the user
    before decomposition and deep reasoning.
    """
    def chat(self, message: str, context: AgentState) -> str:
        ...
