from custom_tools._0_chromadb_retrieval import (
    retrieve_chromadb_authentic,
    retrieve_chromadb_user,
)


def retrieve_context_from_chroma_db(user_prompt, collection_name, authentic=True):
    if authentic:
        collection = retrieve_chromadb_authentic(collection_name)
    else:
        collection = retrieve_chromadb_user(collection_name)

    rag_content = collection.query(
        query_texts=[user_prompt],
        n_results=10,
        include=["documents", "metadatas", "distances"],
    )
    rag_content_doc = rag_content["documents"][0]
    rag_content_source = rag_content["metadatas"][0]
    rag_content_score = rag_content["distances"][0]

    filtered_docs = []
    filtered_metas = []
    filtered_scores = []

    for doc, meta, dist in zip(rag_content_doc, rag_content_source, rag_content_score):

        if dist >= 0.75:
            filtered_docs.append(doc)
            filtered_metas.append(meta)
            filtered_scores.append(dist)

    if not filtered_docs:
        return False, "No relevant documents found", "Simliarity metric percentage = 75"
    return filtered_metas, filtered_docs, filtered_scores


if __name__ == "__main__":
    sources, content, scores = retrieve_context_from_chroma_db(
        user_prompt="ms dhoni captenciy",
        collection_name="ms_dhoni",
        authentic=True,
    )
    print(sources, content, scores)
