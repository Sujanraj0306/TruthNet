import os
import shutil
from custom_tools._1_custom_embedding import SemanticEmbeddingFunction


# Initializations
hf_embedding_model = SemanticEmbeddingFunction()
base = os.getcwd()
folder_path = os.path.join(base, "knowledge_base", "chroma_db")


# Save files
def save_file(file, upload_folder):
    file.save(os.path.join(upload_folder, file.filename))


# Get subjects
def get_collections():
    subfolders = [f.name for f in os.scandir(folder_path) if f.is_dir()]
    return [col for col in sorted(subfolders)]


# Create subjects
def create_collection(name):
    list_all_collections = get_collections()

    if name not in list_all_collections:
        subfolder_path = os.path.join(folder_path, name)
        os.makedirs(subfolder_path, exist_ok=True)
        os.makedirs("knowledge_base/embedding_history/authentic", exist_ok=True)
        os.makedirs("knowledge_base/embedding_history/user", exist_ok=True)
        os.makedirs("knowledge_base/chat_history", exist_ok=True)
        with open(
            f"knowledge_base/embedding_history/authentic/{name}_history.txt",
            "w",
            encoding="utf-8",
        ) as f:
            f.write("")
        with open(
            f"knowledge_base/embedding_history/user/{name}_history.txt",
            "w",
            encoding="utf-8",
        ) as f:
            f.write("")
        with open(
            f"knowledge_base/chat_history/{name}_chat_history.txt",
            "w",
            encoding="utf-8",
        ) as f:
            f.write("Hi, I am TruthNet. I can help you in finding misinformation...")
            return f"Topic {name} created successfully"
    else:
        return f"Topic {name} already exists"


# Delete subjects
def delete_collection(name):
    subfolder_path = os.path.join(folder_path, name)

    embed_history_path = (
        f"knowledge_base/embedding_history/authentic/{name}_history.txt"
    )
    chat_history_path = f"knowledge_base/chat_history/{name}_chat_history.txt"
    user_embed_history_path = (
        f"knowledge_base/embedding_history/user/{name}_history.txt"
    )

    if os.path.isdir(subfolder_path):
        shutil.rmtree(subfolder_path)
    if os.path.exists(embed_history_path):
        os.remove(embed_history_path)
    if os.path.exists(chat_history_path):
        os.remove(chat_history_path)
    if os.path.exists(user_embed_history_path):
        os.remove(user_embed_history_path)
    return f"Topic {name} deleted successfully"


# Rename collection
def rename_collection(old_name, new_name):
    list_all_collections = get_collections()

    if new_name not in list_all_collections:
        old_path = os.path.join(folder_path, old_name)
        new_path = os.path.join(folder_path, new_name)
        os.rename(old_path, new_path)
        new_embed_history_path = (
            f"knowledge_base/embedding_history/authentic/{new_name}_history.txt"
        )
        new_chat_history_path = (
            f"knowledge_base/chat_history/{new_name}_chat_history.txt"
        )
        user_embed_history = (
            f"knowledge_base/embedding_history/user/{new_name}_history.txt"
        )
        old_embed_history_path = (
            f"knowledge_base/embedding_history/authentic/{old_name}_history.txt"
        )
        old_chat_history_path = (
            f"knowledge_base/chat_history/{old_name}_chat_history.txt"
        )
        old_user_embed_history = (
            f"knowledge_base/embedding_history/user/{old_name}_history.txt"
        )
        os.rename(old_embed_history_path, new_embed_history_path)
        os.rename(old_chat_history_path, new_chat_history_path)
        os.rename(old_user_embed_history, user_embed_history)
        return f"{old_name} renamed to {new_name} successful"
    else:
        return f"{new_name} already exists"


# Get chat history
def get_chat_history(collection_name):
    chat_history_path = (
        f"knowledge_base/chat_history/{collection_name}_chat_history.txt"
    )
    with open(chat_history_path, "r", encoding="utf-8") as f:
        temp_chat_history = [line.strip() for line in f.readlines()]

    return temp_chat_history


# Get embedding history
def get_chat_embed_history_authentic(collection_name):
    k_history_path = (
        f"knowledge_base/embedding_history/authentic/{collection_name}_history.txt"
    )
    with open(k_history_path, "r", encoding="utf-8") as f:
        temp_embed_history = [line for line in f.readlines()]
    return temp_embed_history


# Get embedding history
def get_chat_embed_history_user(collection_name):
    k_history_path = (
        f"knowledge_base/embedding_history/user/{collection_name}_history.txt"
    )
    with open(k_history_path, "r", encoding="utf-8") as f:
        temp_embed_history = [line for line in f.readlines()]
    return temp_embed_history


if __name__ == "__main__":
    print(create_collection("agniveer  dsfd"))
