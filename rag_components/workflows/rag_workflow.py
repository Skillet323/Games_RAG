from pathlib import Path

# Добавляем корневую папку проекта в sys.path, чтобы можно было импортировать rag_components
import sys
PROJECT_ROOT = Path(__file__).parent.parent.resolve()
sys.path.append(str(PROJECT_ROOT))


#rag_components/workflows/rag_workflow.py
from langgraph.graph import START, END, StateGraph
from states.rag_states import GraphState
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition

from nodes_and_edges.generate_query_or_respond import generate_query_or_respond
from nodes_and_edges.generate_answer import generate_answer
from nodes_and_edges.rewrite_question import rewrite_question
from nodes_and_edges.grade_documents import grade_documents
from logic.retrieval import get_retriever_tool



def create_rag_graph():
    workflow = StateGraph(GraphState)

    # Define the nodes we will cycle between
    workflow.add_node(generate_query_or_respond)
    workflow.add_node("retrieve", ToolNode([get_retriever_tool()]))
    workflow.add_node(rewrite_question)
    workflow.add_node(generate_answer)

    workflow.add_edge(START, "generate_query_or_respond")

    # Decide whether to retrieve
    workflow.add_conditional_edges(
        "generate_query_or_respond",
        # Assess LLM decision (call `retriever_tool` tool or respond to the user)
        tools_condition,
        {
            # Translate the condition outputs to nodes in our graph
            "tools": "retrieve",
            END: END,
        },
    )

    # Edges taken after the `action` node is called.
    workflow.add_conditional_edges(
        "retrieve",
        # Access agent decision
        grade_documents,
    )
    workflow.add_edge("generate_answer", END)
    workflow.add_edge("rewrite_question", "generate_query_or_respond")

    return workflow.compile()