from nodes_and_edges.generate_answer import generate_answer
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
                {
                    "role": "tool", 
                    "content": "Theo is a major character in Celeste. He climbs the mountain alongside Madeline throughout the earlier chapters. His primary justification for climbing the mountain is to take pictures to increase his number of followers on InstaPix, a social media platform. He additionally supports Madeline on various occasions, especially between the end of Golden Ridge to Reflection. He can be found in all chapters except Prologue, The Summit, and Core.", 
                    "tool_call_id": "1"
                },
            ]
        )
    }
    response = generate_answer(input)
    response["messages"][-1].pretty_print()