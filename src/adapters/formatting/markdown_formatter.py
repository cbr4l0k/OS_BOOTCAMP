"""
Markdown Formatter Adapter

This adapter formats structured answers into markdown reports.
Creates user-friendly output with citations, headers, and formatting.
"""

from src.domain.ports import FormattingPort
from src.domain.models import StructuredAnswer


class MarkdownFormatter(FormattingPort):
    """
    Formats structured answers as markdown.

    Example usage:
        formatter = MarkdownFormatter()
        answer = StructuredAnswer(reasoning="...", conclusion="...")
        markdown = formatter.format(answer)
    """

    def __init__(self, include_metadata: bool = True):
        """
        Initialize the Markdown Formatter.

        Args:
            include_metadata: Whether to include metadata in output
        """
        self.include_metadata = include_metadata

    def format(self, answer: StructuredAnswer) -> str:
        """
        Format a structured answer as markdown.

        Args:
            answer: The structured answer to format

        Returns:
            Markdown-formatted string
        """
        sections = []

        # Header
        sections.append("# Research Answer\n")

        # Confidence indicator
        if self.include_metadata and 'confidence' in answer.metadata:
            sections.append(self._format_confidence(answer.metadata['confidence']))

        # Main conclusion
        sections.append(self._format_summary(answer.conclusion))

        # Reasoning/analysis
        if answer.reasoning:
            sections.append(self._format_reasoning(answer.reasoning))

        # Citations
        if self.include_metadata and 'sources' in answer.metadata:
            sections.append(self._format_citations(answer.metadata['sources']))

        # Additional metadata
        if self.include_metadata:
            metadata_section = self._format_metadata(answer.metadata)
            if metadata_section:
                sections.append(metadata_section)

        # Footer
        sections.append(self._format_footer())

        return "\n".join(sections)

    def _format_confidence(self, confidence: float) -> str:
        """
        Format confidence score with visual indicator.

        Args:
            confidence: Confidence score between 0 and 1

        Returns:
            Formatted confidence section
        """
        confidence_pct = f"{confidence * 100:.0f}%"

        # Visual confidence indicator
        if confidence > 0.8:
            confidence_bar = "████████░░"
            confidence_label = "High"
        elif confidence > 0.6:
            confidence_bar = "██████░░░░"
            confidence_label = "Medium"
        elif confidence > 0.4:
            confidence_bar = "████░░░░░░"
            confidence_label = "Low"
        else:
            confidence_bar = "██░░░░░░░░"
            confidence_label = "Very Low"

        return f"**Confidence**: `{confidence_bar}` {confidence_label} ({confidence_pct})\n\n---\n"

    def _format_summary(self, conclusion: str) -> str:
        """
        Format the main conclusion/summary.

        Args:
            conclusion: The conclusion text

        Returns:
            Formatted summary section
        """
        return f"## Summary\n\n{conclusion}\n"

    def _format_reasoning(self, reasoning: str) -> str:
        """
        Format the detailed reasoning/analysis section.

        Args:
            reasoning: The reasoning text

        Returns:
            Formatted reasoning section
        """
        output = "## Detailed Analysis\n\n"
        reasoning_text = reasoning.strip()

        # If reasoning has multiple paragraphs or steps, format appropriately
        if '\n' in reasoning_text:
            # Split into paragraphs and format
            paragraphs = [p.strip() for p in reasoning_text.split('\n\n') if p.strip()]

            # If it looks like a list (starts with numbers or bullets)
            if any(p.strip().startswith(('1.', '2.', '-', '*', '•')) for p in paragraphs):
                output += f"{reasoning_text}\n"
            else:
                # Format as numbered steps if multiple paragraphs
                for i, para in enumerate(paragraphs, 1):
                    if len(paragraphs) > 1:
                        output += f"{i}. {para}\n\n"
                    else:
                        output += f"{para}\n"
        else:
            output += f"{reasoning_text}\n"

        return output

    def _format_citations(self, sources: list) -> str:
        """
        Format the citations/sources section.

        Args:
            sources: List of source objects or dictionaries

        Returns:
            Formatted citations section
        """
        output = "## Citations\n\n"

        for i, source in enumerate(sources, 1):
            if isinstance(source, dict):
                title = source.get('title', f'Source {i}')
                url = source.get('url', '')
                provider = source.get('provider', 'Unknown')
                excerpt = source.get('excerpt', '')

                if url:
                    output += f"{i}. **[{title}]({url})** *via {provider}*\n"
                else:
                    output += f"{i}. **{title}** *via {provider}*\n"

                if excerpt:
                    output += f"   > {excerpt[:150]}{'...' if len(excerpt) > 150 else ''}\n"
                output += "\n"
            else:
                output += f"{i}. {source}\n"

        return output

    def _format_metadata(self, metadata: dict) -> str:
        """
        Format additional metadata section.

        Args:
            metadata: Metadata dictionary

        Returns:
            Formatted metadata section or empty string if no metadata to show
        """
        metadata_to_show = {
            k: v for k, v in metadata.items()
            if k not in ['sources', 'confidence'] and v is not None
        }

        if not metadata_to_show:
            return ""

        output = "---\n\n"
        output += "<details>\n<summary>Additional Information</summary>\n\n"
        for key, value in metadata_to_show.items():
            formatted_key = key.replace('_', ' ').title()
            output += f"- **{formatted_key}**: `{value}`\n"
        output += "\n</details>\n"

        return output

    def _format_footer(self) -> str:
        """
        Format the footer section.

        Returns:
            Formatted footer
        """
        return "---\n\n*Generated by TeraFinder Research Engine*\n"


# HELPFUL RESOURCES:
# - Markdown Guide: https://www.markdownguide.org/
# - GitHub Flavored Markdown: https://github.github.com/gfm/
# - Markdown cheat sheet: https://www.markdownguide.org/cheat-sheet/
#
# TIPS:
# - Use proper heading hierarchy (# ## ###)
# - Add horizontal rules (---) for visual separation
# - Use blockquotes (>) for important callouts
# - Format code with backticks or code blocks
# - Make links descriptive, not just URLs
# - Use tables for structured data
# - Add emojis sparingly for visual cues
# - Test rendering in different markdown viewers
# - Consider accessibility (screen readers)
# - Keep line lengths reasonable for readability
