from logic.retrieval import get_retriever_tool


if __name__ == "__main__":
    retriever_tool = get_retriever_tool()
    print(retriever_tool.invoke({"query": "types of reward hacking"}))

