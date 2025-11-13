# TeraFinder - Feature Implementation Plan


---

## 🧠 PHASE 2: Pro Mode Core (Intelligence Layer)
**Goal**: Add verification and task decomposition for deep research

- [x] **Verification engine** - Add cross-source fact checking with confidence scores - `feature/verification-engine`
- [x] **Verification node** - Add validation graph node between retrieval and synthesis - `feature/verification-node`
- [x] **Task decomposer** - Implement complex query breakdown into sub-tasks - `feature/task-decomposer`
- [ ] **Decomposition node** - Add task breakdown graph node for Pro Mode - `feature/decomposition-node`

**✅ Milestone**: System can break down complex queries and verify facts across sources

---

## 🔁 PHASE 3: Multi-Step Reasoning (Iteration)
**Goal**: Enable iterative refinement and Pro Mode completion

- [ ] **Loop controller** - Implement multi-step reasoning iteration control - `feature/loop-controller`
- [ ] **Loop control node** - Add iteration decision node with routing logic - `feature/loop-control-node`
- [ ] **Pro mode flow** - Integrate full pipeline with decomposition and loops - `feature/pro-mode`

**✅ Milestone**: Pro Mode fully functional with multi-hop reasoning

---

## 📚 PHASE 4: Extended Data Sources (Optional)
**Goal**: Add specialized adapters for Pro Mode variants

### Core Enhancement
- [ ] **Web scraper** - Add detailed page content extraction via BeautifulSoup - `feature/web-scraper`

### Pro: Social Mode
- [ ] **Reddit adapter** - Add Reddit post/comment retrieval for opinion analysis - `feature/reddit-adapter`
- [ ] **Twitter adapter** - Add Twitter/X post retrieval for social insights - `feature/twitter-adapter`
- [ ] **VK/Habr adapter** - Add Russian social media integration - `feature/social-adapter`

### Pro: Academic Mode
- [ ] **Academic adapter** - Add arXiv and Semantic Scholar for research papers - `feature/academic-adapter`

### Pro: Finance Mode
- [ ] **Finance adapter** - Add Yahoo Finance for stock and market data - `feature/finance-adapter`

**✅ Milestone**: Extended Pro Mode capabilities (Social/Academic/Finance)

---

## 💬 PHASE 5: User Experience Polish
**Goal**: Improve interaction and mode comparison

- [ ] **Conversation agent** - Add interactive query clarification - `feature/conversation-agent`
- [ ] **Conversation node** - Add user interaction graph node - `feature/conversation-node`
- [ ] **Mode comparison UI** - Add side-by-side Simple vs Pro Mode view - `feature/mode-comparison`

**✅ Milestone**: Enhanced UX with query refinement and mode comparison

---

## 🧪 PHASE 6: Validation & Benchmarking
**Goal**: Measure and validate system performance

- [ ] **SimpleQA benchmark** - Add accuracy testing for simple questions - `feature/simpleqa-bench`
- [ ] **FRAMES benchmark** - Add factuality and reasoning depth evaluation - `feature/frames-bench`

**✅ Milestone**: Quantitative evaluation of Simple and Pro Mode performance


# Done

- [x] SERP adapter - Implement Google/Bing search API for basic web queries - `feature/serp-adapter`

- [x] Answer synthesizer - Implement LLM-based answer generation from sources - `feature/answer-synthesizer`
- [x] Markdown formatter - Implement citation-rich markdown output - `feature/markdown-formatter`
- [x] Retrieval node - Implement graph node for data retrieval orchestration - `feature/retrieval-node`

## ~🎯 PHASE 1: Minimum Viable Product (Simple Mode)~
**Goal**: Get a working end-to-end Simple Mode demo

- [x] **Graph definition** - Wire up basic LangGraph workflow (retrieval->synthesis->format) - `feature/graph-definition`
- [x] **Synthesis node** - Implement graph node for answer generation - `feature/synthesis-node`
- [x] **Simple mode flow** - Add fast search path bypassing decomposition - `feature/simple-mode`
- [x] **UI integration** - Connect agent graph to Chainlit replacing historian bot - `feature/ui-integration`

**✅ Milestone**: User can ask a question -> get a quick answer with citations (Simple Mode working)

