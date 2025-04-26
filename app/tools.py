from langchain.tools import tool


def get_band_information_tool(retriever):
    """
    Create a MANUAL tool that fetches Band-related context from Chroma and outputs a dict.
    """

    @tool
    def get_band_information(query: str) -> dict:
        """
        Description:
        - This tool Retrieves relevant passages about Bands (songs, albums, history, members, etc).
        Input:
        - query (string): A natural language question about a music band (e.g., band history, songs, albums, members).
        Output:
        - A dictionary with:
            - 'context' (string): Combined relevant passages retrieved from the knowledge base, labeled with the band name and source.
            - 'snippets' (list of strings): A list of individual passages, each prefixed with [Band: <band name>] [Source: <source>].
        """
        docs = retriever.invoke(query)
        if not docs:
            return {
                "context": "No information found related to your query.",
                "snippets": [],
                "source": None
            }

        # top_snippets = [doc.page_content for doc in docs]
        # snippet_text = "\n\n".join(top_snippets)

        # Build per-snippet text with band name
        snippets = []
        for doc in docs:
            band_name = doc.metadata.get("band", "Unknown Band")
            info_source = doc.metadata.get("source", "Unknown Source")
            snippet_text = f"[Band: {band_name}] [Source:{info_source}] {doc.page_content}"
            snippets.append(snippet_text)

        combined_context = "\n\n".join(snippets)

        return {
            "context": combined_context,
            "snippets": snippets,
        }

    return get_band_information
