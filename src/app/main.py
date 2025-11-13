from adapters.synthesis.synthesizer import Synthesizer
from adapters.retrieval.serp_adapter import TavilySerpAdapter
from domain.models import Query
from app.config import config

def main():
    adapter = TavilySerpAdapter()
    query = Query(content="What is hexagonal architecture?")
    results = adapter.retrieve(query)


    model = ChatOpenAI(
        streaming=config.streaming,
        model_name=config.model_name,
        openai_api_base=base_url,
        openai_api_key=api_key,
    )
    synthesizer = Synthesizer()
