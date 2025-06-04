#rag_components/nodes_and_edges/rewrite_question.py
from states.rag_states import GraphState
from logic.llm import get_model
from logic.prompts import REWRITE_PROMPT



def rewrite_question(state: GraphState):
    """Rewrite the original user question."""

    response_model = get_model()

    messages = state["messages"]
    question = messages[0].content
    prompt = REWRITE_PROMPT.format(question=question)
    response = response_model.invoke([{"role": "user", "content": prompt}])
    return {"messages": [{"role": "user", "content": response.content}]}
