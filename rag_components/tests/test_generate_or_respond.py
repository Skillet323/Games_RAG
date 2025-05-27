from nodes_and_edges.generate_query_or_respond import generate_query_or_respond


def test_irrelevant_question():
    """checks how model would respond to non-Celeste question"""

    input = {"messages": [{"role": "user", "content": "hello!"}]}
    return generate_query_or_respond(input)["messages"][-1].pretty_print()


def test_relevant_question():
    """Shows how model would respond to Celeste question"""

    input = {
        "messages": [
            {
                "role": "user",
                "content": "Who is Theo from Celeste?",
            }
        ]
    }
    generate_query_or_respond(input)["messages"][-1].pretty_print()



if __name__ == "__main__":
    test_irrelevant_question()
    test_relevant_question()