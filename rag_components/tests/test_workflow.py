from workflows.rag_workflow import create_rag_graph

def draw_graph():
    #TODO
    raise NotImplementedError


def test_graph():

    graph = create_rag_graph()
    for chunk in graph.stream(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "Who is Theo from Celeste",
                }
            ]
        }
    ):
        for node, update in chunk.items():
            print("Update from node", node)
            update["messages"][-1].pretty_print()
            print("\n\n")


if __name__ == "__main__":
    draw_graph()
    test_graph()

