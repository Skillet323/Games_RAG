#rag_components/nodes_and_edges/generate_answer.py
from states.rag_states import GraphState
from logic.llm import get_model
from logic.prompts import GENERATE_PROMPT


def generate_answer(state: GraphState):
    """Generate an answer."""
    response_model = get_model()

    question = state["messages"][0].content
    context = state["messages"][-1].content
    prompt = GENERATE_PROMPT.format(question=question, context=context)
    response = response_model.invoke([{"role": "user", "content": prompt}])
    return {"messages": [response]}