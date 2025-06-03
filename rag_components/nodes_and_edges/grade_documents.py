#rag_components/nodes_and_edges/grade_documents.py
from logic.llm import get_model
from logic.prompts import GRADE_PROMPT
from states.rag_states import GraphState
from typing import Literal
from models.pydantic_models import GradeDocuments


def grade_documents(state: GraphState) -> Literal["generate_answer", "rewrite_question"]:
    """Determine whether the retrieved documents are relevant to the question."""

    grader_model = get_model()
    question = state["messages"][0].content
    context = state["messages"][-1].content

    prompt = GRADE_PROMPT.format(question=question, context=context)
    response = (
        grader_model
        .with_structured_output(GradeDocuments).invoke(
            [{"role": "user", "content": prompt}]
        )
    )
    score = response.binary_score

    if score == "yes":
        return "generate_answer"
    else:
        return "rewrite_question"