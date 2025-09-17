from langchain.text_splitter import RecursiveCharacterTextSplitter
from _2_preprocessing_url import url_to_chunks
from langchain.schema import Document
from custom_tools._0_chromadb_retrieval import (
    retrieve_chromadb_authentic,
    retrieve_chromadb_user,
)
import re
import os


def create_new_embeddings(collection_name, type_of_url, urls):
    # remove duplication
    len_original = len(urls)
    urls = set(urls)
    len_new_urls_set = len(urls)

    if type_of_url == "authentic":
        collection = retrieve_chromadb_authentic(collection_name)
        history_path = (
            f"knowledge_base/embedding_history/authentic/{collection_name}_history.txt"
        )
    elif type_of_url == "user":
        collection = retrieve_chromadb_user(collection_name)
        history_path = (
            f"knowledge_base/embedding_history/user/{collection_name}_history.txt"
        )
    else:
        return "Invalid type_of_url"

    os.makedirs(os.path.dirname(history_path), exist_ok=True)

    # Ensure the history file exists
    if not os.path.exists(history_path):
        open(history_path, "a").close()

    with open(history_path, "r", encoding="utf-8") as file:
        old_embed_history = [line.strip() for line in file.readlines()]

    new_embed_count = 0
    skipped_count = 0
    for url in urls:
        if url not in old_embed_history:
            web_content = url_to_chunks(url)
            web_content = re.sub(r"[>{}\[\]\|\\~`]", "", web_content)
            texts = [Document(page_content=web_content)]

            splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000, chunk_overlap=200
            )
            split_docs = splitter.split_documents(texts)

            documents = [doc.page_content for doc in split_docs]
            ids = [f"{url}_{i}" for i in range(len(split_docs))]
            metadatas = [{"source": url} for _ in range(len(split_docs))]

            collection.add(ids=ids, documents=documents, metadatas=metadatas)

            with open(history_path, "a", encoding="utf-8") as history_file:
                history_file.write(f"{url}\n")

            new_embed_count += 1
        else:
            skipped_count += 1

    message = f"{type_of_url.capitalize()} embeddings stored: {new_embed_count} new."
    if skipped_count > 0 or (len_original - len_new_urls_set > 0):
        message += f" Skipped {skipped_count+(len_original - len_new_urls_set)} already embedded URLs."

    return message


def delete_document_from_collection(collection_name, filename, type_of_url):
    if type_of_url == "authentic":
        collection = retrieve_chromadb_authentic(collection_name)
        history_path = (
            f"knowledge_base/embedding_history/authentic/{collection_name}_history.txt"
        )
    elif type_of_url == "user":
        collection = retrieve_chromadb_user(collection_name)
        history_path = (
            f"knowledge_base/embedding_history/user/{collection_name}_history.txt"
        )

    base_filename = os.path.splitext(filename)[0]

    # Remove chunks from ChromaDB
    try:
        existing_ids = collection.get()["ids"]
        relevant_ids = [
            doc_id for doc_id in existing_ids if doc_id.startswith(base_filename)
        ]
        if relevant_ids:
            collection.delete(ids=relevant_ids)
            print(f"Deleted chunks related to {filename} from VectorDB.")
            if os.path.exists(history_path):
                with open(history_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                with open(history_path, "w", encoding="utf-8") as f:
                    for line in lines:
                        if line.strip() != filename:
                            f.write(line)
                return f"Removed {filename} from embedding history."
    except Exception as e:
        return f"Failed to delete chunks for {filename}: {e}"


if __name__ == "__main__":
    urls = [
        "https://sports.ndtv.com/ipl-2025/ms-dhoni-masterstroke-that-led-csk-to-win-over-lsg-revealed-ravi-bishnoi-8179064",
        "https://sports.ndtv.com/ipl-2025/ms-dhoni-masterstroke-that-led-csk-to-win-over-lsg-revealed-ravi-bishnoi-8179064",
        "https://timesofindia.indiatimes.com/sports/cricket/ipl/top-stories/ipl-when-ms-dhoni-changed-csks-team-hotel-over-food-delivery-watch/articleshow/120370641.cms",
    ]
    print(create_new_embeddings("ms_dhoni", type_of_url="authentic", urls=urls))
    urls = [
        "https://www.india.com/photos/sports/dhonis-csk-announce-replacement-for-ruturaj-gaikwad-not-prithvi-shaw-his-name-is-ayush-mhatre-437714/"
    ]
    print(create_new_embeddings("ms_dhoni", type_of_url="user", urls=urls))
