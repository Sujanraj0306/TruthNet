from _0_check_internet import is_internet_on
from urllib.parse import unquote

from flask import Flask, render_template, request
from _1_db_functions import (
    get_collections,
    create_collection,
    delete_collection,
    rename_collection,
    get_chat_history,
    get_chat_embed_history_authentic,
    get_chat_embed_history_user,
)
from _3_chunking import create_new_embeddings, delete_document_from_collection
from _5_chat import start_chatbot

# Check internet
internet_status = "Internet On" if is_internet_on() else "Internet Off"


####### ------------ FLASK ROUTERS
# Flask setup
app = Flask(__name__)


# Home route
@app.route("/")
def index():
    collections = get_collections()
    return render_template(
        "index.html",
        collections=collections,
        internet_status=internet_status,
    )


# Create subject
@app.route("/create_collection_route", methods=["POST"])
def create_collection_route():
    new_collection = request.form.get("new_collection")
    message = create_collection(new_collection)
    collections = get_collections()
    return render_template(
        "index.html",
        message=message,
        collections=collections,
        internet_status=internet_status,
    )


# Rename collection
@app.route("/rename_collection_route/")
def rename_collection_route():
    old_name = request.args.get("old_name")
    new_name = request.args.get("new_name")
    rename_status = rename_collection(old_name, new_name)
    collections = get_collections()
    return render_template(
        "index.html",
        message=rename_status,
        collections=collections,
        internet_status=internet_status,
    )


# Delete subject
@app.route("/delete_collection/<collection_name>")
def delete_collection_route(collection_name):
    message = delete_collection(collection_name)
    collections = get_collections()
    return render_template(
        "index.html",
        message=message,
        collections=collections,
        internet_status=internet_status,
    )


# Upload urls
@app.route("/upload_url_authentic", methods=["POST"])
def upload_docs_authentic():
    collection_name = request.form.get("collection_name")
    authentic_urls = request.form.get("authentic_urls")

    url_list = [url.strip() for url in authentic_urls.splitlines() if url.strip()]
    message = create_new_embeddings(
        collection_name,
        type_of_url="authentic",
        urls=url_list,
    )
    chat_embed_history_uploads_user = get_chat_embed_history_user(collection_name)
    chat_embed_history_uploads_authentic = get_chat_embed_history_authentic(
        collection_name
    )

    chat_history = get_chat_history(collection_name)
    return render_template(
        "chat.html",
        message=message,
        internet_status=internet_status,
        chat_data=chat_history,
        collection=collection_name,
        files=chat_embed_history_uploads_authentic,
        urls_user=chat_embed_history_uploads_user,
        home=True,
    )


# delete urls
@app.route("/delete_url_authentic/<collection>/<path:filename>", methods=["GET"])
def delete_uploaded_file_authentic(collection, filename):
    decoded_file = unquote(filename).strip()

    delete_file = delete_document_from_collection(
        collection, decoded_file, type_of_url="authentic"
    )
    chat_history = get_chat_history(collection)
    chat_embed_history_uploads_user = get_chat_embed_history_user(collection)
    chat_embed_history_uploads_authentic = get_chat_embed_history_authentic(collection)

    return render_template(
        "chat.html",
        collection=collection,
        chat_data=chat_history,
        files=chat_embed_history_uploads_authentic,
        urls_user=chat_embed_history_uploads_user,
        internet_status=internet_status,
        message=delete_file,
        home=True,
    )


# Upload urls
@app.route("/upload_url_user", methods=["POST"])
def upload_docs_user():
    collection_name = request.form.get("collection_name")
    authentic_urls = request.form.get("authentic_urls")

    url_list = [url.strip() for url in authentic_urls.splitlines() if url.strip()]
    message = create_new_embeddings(
        collection_name,
        type_of_url="user",
        urls=url_list,
    )
    chat_embed_history_uploads_user = get_chat_embed_history_user(collection_name)
    chat_embed_history_uploads_authentic = get_chat_embed_history_authentic(
        collection_name
    )
    chat_history = get_chat_history(collection_name)
    return render_template(
        "chat.html",
        message=message,
        internet_status=internet_status,
        chat_data=chat_history,
        collection=collection_name,
        files=chat_embed_history_uploads_authentic,
        urls_user=chat_embed_history_uploads_user,
        home=True,
    )


# delete urls
@app.route("/delete_url_user/<collection>/<path:filename>", methods=["GET"])
def delete_uploaded_file_user(collection, filename):
    decoded_file = unquote(filename).strip()

    delete_file = delete_document_from_collection(
        collection, decoded_file, type_of_url="user"
    )
    chat_history = get_chat_history(collection)
    chat_embed_history_uploads_user = get_chat_embed_history_user(collection)
    chat_embed_history_uploads_authentic = get_chat_embed_history_authentic(collection)

    return render_template(
        "chat.html",
        collection=collection,
        chat_data=chat_history,
        files=chat_embed_history_uploads_authentic,
        urls_user=chat_embed_history_uploads_user,
        internet_status=internet_status,
        message=delete_file,
        home=True,
    )


# Chat window
@app.route("/chat/<collection_name>")
def chat(collection_name):
    chat_history = get_chat_history(collection_name)
    chat_embed_history_uploads_user = get_chat_embed_history_user(collection_name)
    chat_embed_history_uploads_authentic = get_chat_embed_history_authentic(
        collection_name
    )

    return render_template(
        "chat.html",
        collection=collection_name,
        chat_data=chat_history,
        internet_status=internet_status,
        files=chat_embed_history_uploads_authentic,
        urls_user=chat_embed_history_uploads_user,
        checkmarksheet=True,
        home=True,
    )


# Chatbot
@app.route("/start_chatbot_truthnet", methods=["POST"])
def start_chatbot_truthnet():
    user_prompt = request.form.get("user_input_prompt")
    collection_name = request.form.get("collection_name")

    chat_embed_history_uploads_user = get_chat_embed_history_user(collection_name)
    chat_embed_history_uploads_authentic = get_chat_embed_history_authentic(
        collection_name
    )
    chat_history = get_chat_history(collection_name)

    print(
        "---",
        len(chat_embed_history_uploads_authentic),
        len(chat_embed_history_uploads_user),
    )
    if len(chat_embed_history_uploads_authentic) == 0:
        return render_template(
            "chat.html",
            collection=collection_name,
            chat_data=chat_history,
            internet_status=internet_status,
            message="No URLs found. Please upload Authentic URLs.",
            user_prompt=user_prompt,
            files=chat_embed_history_uploads_authentic,
            urls_user=chat_embed_history_uploads_user,
            home=True,
        )
    elif len(chat_embed_history_uploads_user) == 0:
        return render_template(
            "chat.html",
            collection=collection_name,
            chat_data=chat_history,
            internet_status=internet_status,
            message="No URLs found. Please upload New URLs.",
            user_prompt=user_prompt,
            files=chat_embed_history_uploads_authentic,
            urls_user=chat_embed_history_uploads_user,
            home=True,
        )
    else:
        llm_response = start_chatbot(user_prompt, collection_name)
        chat_history = get_chat_history(collection_name)

    return render_template(
        "chat.html",
        collection=collection_name,
        chat_data=chat_history,
        internet_status=internet_status,
        message=None,
        user_prompt=user_prompt,
        llm_response=llm_response,
        files=chat_embed_history_uploads_authentic,
        urls_user=chat_embed_history_uploads_user,
        home=True,
    )


# Main
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
