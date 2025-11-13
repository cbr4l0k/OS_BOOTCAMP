# TeraFinder - Feature Implementation Plan

-[ ] Answer synthesizer - Implement LLM-based answer generation from sources - `feature/answer-synthesizer`
-[ ] Markdown formatter - Implement citation-rich markdown output - `feature/markdown-formatter`
-[ ] Retrieval node - Implement graph node for data retrieval orchestration - `feature/retrieval-node`
-[ ] Synthesis node - Implement graph node for answer generation - `feature/synthesis-node`
-[ ] Graph definition - Wire up basic LangGraph workflow (retrieval→synthesis→format) - `feature/graph-definition`
-[ ] UI integration - Connect agent graph to Chainlit replacing historian bot - `feature/ui-integration`
-[ ] Verification engine - Add cross-source fact checking with confidence scores - `feature/verification-engine`
-[ ] Verification node - Add validation graph node between retrieval and synthesis - `feature/verification-node`
-[ ] Task decomposer - Implement complex query breakdown into sub-tasks - `feature/task-decomposer`
-[ ] Loop controller - Implement multi-step reasoning iteration control - `feature/loop-controller`
-[ ] Decomposition node - Add task breakdown graph node for Pro Mode - `feature/decomposition-node`
-[ ] Loop control node - Add iteration decision node with routing logic - `feature/loop-control-node`
-[ ] Pro mode flow - Integrate full pipeline with decomposition and loops - `feature/pro-mode`
-[ ] Web scraper - Add detailed page content extraction via BeautifulSoup - `feature/web-scraper`
-[ ] Reddit adapter - Add Reddit post/comment retrieval for opinion analysis - `feature/reddit-adapter`
-[ ] Twitter adapter - Add Twitter/X post retrieval for social insights - `feature/twitter-adapter`
-[ ] Academic adapter - Add arXiv and Semantic Scholar for research papers - `feature/academic-adapter`
-[ ] Finance adapter - Add Yahoo Finance for stock and market data - `feature/finance-adapter`
-[ ] VK/Habr adapter - Add Russian social media integration - `feature/social-adapter`
-[ ] Conversation agent - Add interactive query clarification - `feature/conversation-agent`
-[ ] Conversation node - Add user interaction graph node - `feature/conversation-node`
-[ ] Domain service - Implement domain service layer for business logic - `feature/domain-service`
-[ ] Simple mode flow - Add fast search path bypassing decomposition - `feature/simple-mode`
-[ ] Mode comparison UI - Add side-by-side Simple vs Pro Mode view - `feature/mode-comparison`
-[ ] SimpleQA benchmark - Add accuracy testing for simple questions - `feature/simpleqa-bench`
-[ ] FRAMES benchmark - Add factuality and reasoning depth evaluation - `feature/frames-bench`

# Done

-[x] SERP adapter - Implement Google/Bing search API for basic web queries - `feature/serp-adapter`
