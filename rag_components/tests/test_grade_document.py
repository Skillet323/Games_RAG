from nodes_and_edges.grade_documents import grade_documents
from langchain_core.messages import convert_to_messages


def test_irrelevant_doc():
    """Shows how model would grade info irrelevant to Celeste question"""

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
    return grade_documents(input)


def test_relevant_doc():
    """Shows how model would grade info relevant to Celeste question"""

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
    return grade_documents(input)


if __name__ == "__main__":
    print(test_irrelevant_doc()) # Should be 'rewrite_question'
    print(test_relevant_doc()) # Should be 'generate_answer'