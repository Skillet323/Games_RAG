from langchain.tools.retriever import create_retriever_tool

def get_retriever_tool():
    #TODO
    retriever = ...
    raise NotImplementedError

    retriever_tool = create_retriever_tool(
        retriever,
        "retrieve_celeste_info",
        "Search and return information about Celeste",
    )
    return retriever_tool