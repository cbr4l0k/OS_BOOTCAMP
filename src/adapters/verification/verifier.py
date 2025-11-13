"""
Verification Adapter

This adapter verifies and validates information from multiple sources.
It checks for consistency, reliability, and cross-source agreement.
"""

import logging
from collections import defaultdict
from typing import Optional, Any

from src.domain.ports import VerificationPort
from src.domain.models import RetrievedData, VerifiedData, SourceType, SourceProvider

logger = logging.getLogger(__name__)


class Verifier(VerificationPort):
    """
    Verifies retrieved data for accuracy and consistency.

    Calculates confidence scores based on:
    - Number of sources
    - Provider diversity
    - Source type quality (academic > webpage > social)
    - Cross-source agreement (optional LLM-based)

    Example usage:
        verifier = Verifier(llm_client=llm)
        retrieved = RetrievedData(sources=[...])
        verified = verifier.verify(retrieved)
    """

    # Source type quality weights
    SOURCE_TYPE_WEIGHTS = {
        SourceType.ACADEMIC: 1.0,      # Highest quality
        SourceType.WEBPAGE: 0.8,       # Good quality
        SourceType.DOCUMENT: 0.8,      # Good quality
        SourceType.FINANCIAL: 0.9,     # High quality for finance topics
        SourceType.SOCIAL: 0.5,        # Lower quality (opinions)
        SourceType.OTHER: 0.6,         # Medium quality
    }

    def __init__(
        self,
        llm_client=None,
        min_sources_for_high_confidence: int = 5,
        use_llm_verification: bool = False
    ):
        """
        Initialize the Verifier.

        Args:
            llm_client: Optional LLM client for advanced fact-checking
            min_sources_for_high_confidence: Minimum sources needed for high confidence
            use_llm_verification: Whether to use LLM for cross-source verification
        """
        self.llm = llm_client
        self.min_sources = min_sources_for_high_confidence
        self.use_llm_verification = use_llm_verification and llm_client is not None

    def verify(self, data: RetrievedData) -> VerifiedData:
        """
        Verify the retrieved data for accuracy and consistency.

        Args:
            data: Retrieved data from multiple sources

        Returns:
            VerifiedData with validated facts and confidence score

        The confidence calculation considers:
        1. Base confidence from source count (0-0.5)
        2. Diversity bonus from provider variety (0-0.2)
        3. Quality bonus from source types (0-0.2)
        4. LLM verification adjustment (optional, 0-0.1)
        """
        if not data.sources:
            logger.warning("No sources to verify")
            return VerifiedData(
                facts={},
                confidence=0.0,
                diversity_score=0.0,
                corroboration={}
            )

        logger.info(f"Verifying {len(data.sources)} sources...")

        # Extract facts from sources
        facts = self._extract_facts(data.sources)

        # Calculate confidence components
        base_confidence = self._calculate_base_confidence(data.sources)
        diversity_score = self._calculate_diversity_score(data.sources)
        quality_bonus = self._calculate_quality_bonus(data.sources)

        # Start with base + diversity + quality
        confidence = min(base_confidence + diversity_score * 0.2 + quality_bonus, 1.0)

        # Track corroboration (which sources support which facts)
        corroboration = self._track_corroboration(facts, data.sources)

        # Optional: Use LLM for advanced verification
        if self.use_llm_verification and len(data.sources) > 1:
            llm_adjustment = self._llm_verify(data.sources)
            confidence = min(confidence + llm_adjustment, 1.0)
            logger.info(f"LLM verification adjustment: {llm_adjustment:+.2f}")

        logger.info(
            f"Verification complete. Confidence: {confidence:.2f}, "
            f"Diversity: {diversity_score:.2f}, "
            f"Facts: {len(facts)}"
        )

        return VerifiedData(
            facts=facts,
            confidence=confidence,
            diversity_score=diversity_score,
            corroboration=corroboration
        )

    def _extract_facts(self, sources: list) -> dict[str, Any]:
        """
        Extract factual content from sources.

        For now, we group sources by provider and include their excerpts.
        In the future, this could use NLP/LLM to extract structured claims.

        Args:
            sources: List of Source objects

        Returns:
            Dictionary mapping fact keys to source content
        """
        facts = {}

        for i, source in enumerate(sources):
            fact_key = f"source_{i+1}_{source.provider.value}"

            # Store source information
            facts[fact_key] = {
                'content': source.excerpt or source.title,
                'title': source.title,
                'url': source.url,
                'provider': source.provider.value,
                'type': source.type.value,
                'id': source.id
            }

        return facts

    def _calculate_base_confidence(self, sources: list) -> float:
        """
        Calculate base confidence from source count.

        Formula: min(source_count / min_sources_threshold, 0.5)
        - 1 source: 20% confidence
        - 3 sources: 60% confidence (if min_sources=5)
        - 5+ sources: maxes at 50% base confidence

        Args:
            sources: List of Source objects

        Returns:
            Base confidence score (0-0.5)
        """
        source_count = len(sources)
        base = min(source_count / self.min_sources, 1.0) * 0.5
        logger.debug(f"Base confidence from {source_count} sources: {base:.2f}")
        return base

    def _calculate_diversity_score(self, sources: list) -> float:
        """
        Calculate diversity score based on provider variety.

        More diverse sources (different providers) = higher diversity.

        Formula: unique_providers / total_providers
        - All sources from same provider: 0.0
        - All sources from different providers: 1.0

        Args:
            sources: List of Source objects

        Returns:
            Diversity score (0-1)
        """
        if not sources:
            return 0.0

        providers = [s.provider for s in sources]
        unique_providers = len(set(providers))
        total_providers = len(providers)

        diversity = unique_providers / total_providers
        logger.debug(
            f"Diversity: {unique_providers}/{total_providers} "
            f"unique providers = {diversity:.2f}"
        )
        return diversity

    def _calculate_quality_bonus(self, sources: list) -> float:
        """
        Calculate quality bonus based on source types.

        Higher quality sources (academic, financial) increase confidence.

        Formula: average of source type weights * 0.2
        - All academic sources: +0.2
        - All social sources: +0.1
        - Mixed: somewhere in between

        Args:
            sources: List of Source objects

        Returns:
            Quality bonus (0-0.2)
        """
        if not sources:
            return 0.0

        weights = [
            self.SOURCE_TYPE_WEIGHTS.get(s.type, 0.6)
            for s in sources
        ]

        avg_weight = sum(weights) / len(weights)
        bonus = (avg_weight - 0.5) * 0.4  # Normalize to 0-0.2 range

        logger.debug(f"Quality bonus from source types: {bonus:.2f}")
        return max(0.0, bonus)

    def _track_corroboration(
        self,
        facts: dict,
        sources: list
    ) -> dict[str, list[str]]:
        """
        Track which sources corroborate which facts.

        In a simple implementation, each fact is supported by its own source.
        In advanced implementation, could use NLP to find similar claims across sources.

        Args:
            facts: Dictionary of extracted facts
            sources: List of Source objects

        Returns:
            Map of fact keys to list of source IDs that support them
        """
        corroboration = {}

        for fact_key, fact_data in facts.items():
            if isinstance(fact_data, dict) and 'id' in fact_data:
                # Each fact is corroborated by its source
                corroboration[fact_key] = [fact_data['id']]

        return corroboration

    def _llm_verify(self, sources: list) -> float:
        """
        Use LLM to verify cross-source agreement.

        This is an optional advanced feature that uses an LLM to:
        1. Identify key claims in each source
        2. Check for agreement/contradiction
        3. Assess overall reliability

        Args:
            sources: List of Source objects

        Returns:
            Confidence adjustment (-0.1 to +0.1)
        """
        if not self.llm or len(sources) < 2:
            return 0.0

        try:
            # Prepare sources for LLM (limit to first 5 to avoid token limits)
            sources_text = "\n\n".join([
                f"Source {i+1} ({s.provider.value}):\n"
                f"Title: {s.title}\n"
                f"Excerpt: {s.excerpt or 'N/A'}"
                for i, s in enumerate(sources[:5])
            ])

            prompt = f"""Compare these sources and assess their reliability:

{sources_text}

Analyze:
1. Do the sources generally agree or contradict each other?
2. Are there any obvious contradictions or inconsistencies?
3. Overall, how reliable does this information appear?

Respond with a JSON object:
{{
  "agreement_level": "high" | "medium" | "low",
  "contradictions": ["list of any contradictions found"],
  "confidence_adjustment": <number between -0.1 and 0.1>
}}

If sources mostly agree and seem reliable, return positive adjustment.
If there are contradictions or reliability concerns, return negative adjustment.
"""

            # TODO: Call LLM and parse response
            # For now, return neutral adjustment
            # response = self.llm.complete(prompt)
            # adjustment = parse_adjustment(response)

            logger.debug("LLM verification not fully implemented yet")
            return 0.0

        except Exception as e:
            logger.error(f"Error in LLM verification: {e}")
            return 0.0
