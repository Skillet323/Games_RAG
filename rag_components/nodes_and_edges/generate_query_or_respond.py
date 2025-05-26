from rag_components.logic import retrieval
from states.rag_states import GraphState
from logic.llm import get_model
from logic.retrieval import get_retriever_tool


def generate_query_or_respond(state: GraphState):
    """Call the model to generate a response based on the current state. Given
    the question, it will decide to retrieve using the retriever tool, or simply respond to the user.
    """
    response_model = get_model()
    retriever_tool = get_retriever_tool()


    response = (
        response_model
        # highlight-next-line
        .bind_tools([retriever_tool]).invoke(state["messages"])
    )
    return {"messages": [response]}