from nodes_and_edges.rewrite_question import rewrite_question
from langchain_core.messages import convert_to_messages


if __name__ == "__main__":
    input = {
        "messages": convert_to_messages(
            [
                {
                    "role": "user",
                    "content": "Who is Theo from Celeste?",
                },
                {
                    "role": "assistant",
                    "content": "",
                    "tool_calls": [
                        {
                            "id": "1",
                            "name": "retrieve_celeste_info",
                            "args": {"query": "Theo from Celeste"},
                        }
                    ],
                },
                {"role": "tool", "content": "meow", "tool_call_id": "1"},
            ]
        )
    }
    response = rewrite_question(input)
    print(response["messages"][-1]["content"])


