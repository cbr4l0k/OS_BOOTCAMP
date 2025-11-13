Research Pro Mode is an advanced search assistant that not only finds answers but understands context, compares sources, and verifies facts. Participants create two modes of the assistant:

1. Simple Mode — a fast search like ChatGPT or Perplexity Lite.

2. Pro Mode — an intelligent "researcher" that performs several reasoning steps, collects data from various sites, verifies accuracy, and provides a final conclusion with references.

The goal is to demonstrate how to transform a regular chatbot into a tool capable of reasoning, citing, and trusting only verified facts.

Implementation stages:

- Basic search (Simple Mode)
  - Uses SERP (web search) for quick results
  - Minimal processing overhead
  - Ideal for simple single-address queries
  - Fast response time
  - Well-suited for basic information retrieval

- Deep analysis (Pro Mode)
  - Includes comprehensive web scraping
  - Implements semantic re-evaluation of results
  - Includes advanced data post-processing
  - Slightly longer processing time
  - Excels at:
    i. Complex search requirements
    ii. Detailed data collection
    iii. Questions requiring cross-verification
  - Optional extended modes:
    - Pro: Social — opinion analysis (Reddit, X, VK, Habr)
    - Pro: Academic — search in arXiv / Semantic Scholar
    - Pro: Finance — data from Yahoo Finance / TradingView

Evaluation criteria:

- Quality assessment is conducted via open benchmarks:
  - SimpleQA Bench — checks basic accuracy for simple single-step questions (single-hop factual QA).
    - Metric: Accuracy (%)
  - FRAMES Bench — evaluates complex queries requiring multi-step reasoning and multi-source retrieval.
    - Metrics: Factuality, Reasoning Depth, Source Diversity

Tips and hints:

- Use open APIs for search and scraping — https://github.com/vakovalskii/searxng-docker-tavily-adapter
- Multi-hop reasoning can be implemented via LangChain / LangGraph or a custom loop.
- Include “Explain your reasoning”: let the assistant explain why a particular conclusion was made.
- Show the difference between Simple Mode and Pro Mode — this is the main visual effect in the demo.
- Test the pipeline on open-source models.

This task intends to develop an advanced assistant able to reason and verify facts with a clear distinction between a simple fast search mode and a deeper research mode.[1]

[1](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/124418491/be1bd0ef-2d36-4130-b3ab-51cf3769aa96/sber_task.pdf)
