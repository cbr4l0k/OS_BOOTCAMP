"""
Synthesis Adapter

This adapter synthesizes verified data into a structured answer.
It combines information from multiple sources into a coherent response.

TO IMPLEMENT:
1. Use an LLM to synthesize information
2. Create a reasoning chain explaining the answer
3. Combine facts from multiple sources
4. Generate a clear, well-structured conclusion
"""

from src.domain.models import VerifiedData, StructuredAnswer, SynthesisOutput
from src.domain.ports import SynthesisPort
from src.domain.prompts import SYNTHESIS_PROMPT




class Synthesizer(SynthesisPort):
    """
    Synthesizes verified data into a structured answer.

    Example usage:
        synthesizer = Synthesizer(llm_client=llm)
        verified = VerifiedData(facts={...}, confidence=0.8)
        answer = synthesizer.synthesize(verified)
    """

    def __init__(self, llm_client):
        """
        Initialize the Synthesizer.

        Args:
            llm_client: LLM client for generating answers
        """
        self.llm = llm_client

    def synthesize(self, data: VerifiedData) -> StructuredAnswer:
        """
        Synthesize verified data into a structured answer.

        Args:
            data: Verified data with facts and confidence

        Returns:
            StructuredAnswer with reasoning and conclusion
        """
        if not data.facts:
            return StructuredAnswer(
                reasoning="No verified facts available to synthesize.",
                conclusion="Unable to provide an answer due to lack of data.",
                metadata={'confidence': 0.0}
            )

        # Prepare facts for synthesis
        facts_summary = data.to_formatted_string()
        prompt = SYNTHESIS_PROMPT.format(confidence=data.confidence, facts=facts_summary)

        try:
            # Create structured LLM that outputs SynthesisOutput schema
            structured_llm = self.llm.with_structured_output(SynthesisOutput)

            # Configure temperature for more factual responses
            structured_llm_with_config = structured_llm.with_config(configurable={
                "temperature": 0.3,
            })

            # Call LLM to generate synthesis
            response = structured_llm_with_config.invoke(prompt)

            # Generate metadata separately (not from LLM)
            metadata = {
                'confidence': data.confidence,
                'num_sources': len(data.facts),
                'synthesis_method': 'llm_structured',
            }

            return StructuredAnswer(
                reasoning=response.reasoning,
                conclusion=response.conclusion,
                metadata=metadata
            )

        except Exception as e:
            print(f"Error in synthesis: {e}")
            import traceback
            traceback.print_exc()
            # Fallback: simple concatenation
            reasoning = "Facts were collected from multiple sources but synthesis failed."
            conclusion = facts_summary
            metadata = {
                'confidence': data.confidence,
                'num_sources': len(data.facts),
                'synthesis_method': 'fallback',
                'error': str(e)
            }

            return StructuredAnswer(
                reasoning=reasoning,
                conclusion=conclusion,
                metadata=metadata
            )


# HELPFUL RESOURCES:
# - LangChain for LLM orchestration
# - OpenAI API for GPT models
# - Anthropic Claude for longer context
# - Prompt engineering guides
#
# TIPS:
# - Use lower temperature (0.2-0.4) for more factual responses
# - Include source citations in the reasoning
# - Handle cases where facts contradict each other
# - Provide confidence levels in the conclusion
# - Keep the tone appropriate to the domain (technical, casual, etc.)
# - Consider using chain-of-thought prompting
# - For complex topics, break synthesis into sub-steps
