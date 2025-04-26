from langchain.tools import tool


def get_band_information_tool(retriever):
    """
    Create a MANUAL tool that fetches Band-related context from Chroma and outputs a dict.
    """

    @tool
    def get_band_information(query: str) -> dict:
        """Retrieve relevant passages about Bands (songs, albums, history, members, etc)."""
        docs = retriever.invoke(query)
        if not docs:
            return {"context": "No information found related to your query."}

        top_snippets = [doc.page_content for doc in docs]
        snippet_text = "\n\n".join(top_snippets)

        return {"context": snippet_text}

    return get_band_information
