from src.adapters.synthesis.synthesizer import Synthesizer
from src.domain.models import VerifiedData
from langchain_openai import ChatOpenAI
from src.app.config import AppConfig
import asyncio

def main():
    config = AppConfig()
    model = ChatOpenAI(
        model_name=config.model_name,
        openai_api_base=config.openai_api_base,
        openai_api_key=config.openai_api_key,
    )

    vd1 = VerifiedData(
        facts={
            "premises": [
                "All professional drivers always obey traffic laws.",
                "Tom is a professional driver.",
                "Tom was fined today for running a red light."
            ],
            "context_notes": "Is 'running a red light' always a violation? Might an emergency exempt a driver?"
        },
        confidence=0.76
    )

    vd2 = VerifiedData(
        facts={
            "premises": [
                "If the meeting is scheduled for 10 AM then all members must attend.",
                "The meeting was scheduled for 10 AM.",
                "John did not attend the meeting."
            ],
            "conclusion": "John is not a member of the group.",
            "context_notes": "The conclusion depends on assuming 'must attend' means 'will attend'; perhaps John had a valid excuse."
        },
        confidence=0.82
    )

    vd3 = VerifiedData(
        facts={
            "statements": [
                "No fruits are vegetables.",
                "Some items labelled as ‘vegetables’ are botanically fruits (e.g., tomato, cucumber).",
                "Therefore, some vegetables are not vegetables."
            ],
            "analysis_hint": "Here the equivocation on ‘vegetable’ (culinary vs botanical) introduces a conflict with the simple universal 'no fruits are vegetables'."
        },
        confidence=0.68
    )
    synthesizer = Synthesizer(llm_client=model)

    for idx, vd in enumerate([vd1, vd2, vd3]):
        print(f"\n--- Synthesizing VerifiedData #{idx+1} ---")
        res = synthesizer.synthesize(data=vd)
        print(f"{res=}")



