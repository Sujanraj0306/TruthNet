from _4_chromadb_retrieval import retrieve_context_from_chroma_db
from custom_tools._2_custom_llm import custom_llm_function
import re
import os

base = os.getcwd()
folder_path = os.path.join(base, "knowledge_base", "chroma_db")


def llm_generation(user_prompt, rag_content_authentic, rag_content_user):
    # Define persona and instruction
    system_message = """
    You're TruthNet, an AI trained to verify factual accuracy and detect misinformation
    in news or claims. Your expertise includes source validation, fact-checking against 
    authoritative sources, and semantic comparison to detect discrepancies.
    
    Your Role: Compare the unverified Information against the 
    Verified information with respect to user query. 
    Your analysis must be strictly based on the provided content—do not assume or speculate.

    Instructions:
    1. You will receive:
        - Authentic Source Information (trusted source)
        - New Source Information (to be checked)
    2. Compare the Verified Information with the unverified information Information. 
        Identify any factual error, distortion, or mismatch.
    3. If misinformation is found:
        - Respond with: MISINFORMATION, "[quote the exact sentence from the New Source where misinformation appears in unverified source]"
    4. If no discrepancy is found:
        - Output nothing. NO MISINFORMATION.


    Strict Rules:
    - Do not speculate or use external knowledge.
    - Only compare what's given.
    - Be precise, neutral, and factual.
    - Do not summarize or offer opinions."
    """

    # Final prompt structure
    final_prompt = f"""
    {system_message}

    ---
    User Query:
    {user_prompt}

    Verified Information:
    {rag_content_authentic}

    Unverified Information:
    {rag_content_user}

    Answer:
    (Respond answer within 50 words according to the user question with respect to User Query)
    """
    return custom_llm_function(final_prompt, user_prompt)


def start_chatbot(user_prompt, collection_name):
    if user_prompt.strip().lower() in ["exit", "quit"]:
        return "👋 Goodbye!"

    rag_content_authentic_sources, rag_content_authentic_content, rag_scores = (
        retrieve_context_from_chroma_db(user_prompt, collection_name, authentic=True)
    )
    rag_content_user_sources, rag_content_user_content, rag_scores = (
        retrieve_context_from_chroma_db(user_prompt, collection_name, authentic=False)
    )
    # rag_content_authentic_content = "ms dhoni is the new captian of csk in ipl 2025. hardik is the captian for mumbai indians"
    # rag_content_user_content = "rutraj is the new captian of csk in ipl 2025. hardik is the captian for mumbai indians"
    print("Documents loaded.")

    llm_answer = llm_generation(
        user_prompt, rag_content_authentic_content, rag_content_user_content
    )

    # Update history
    with open(
        f"knowledge_base/chat_history/{collection_name}_chat_history.txt",
        "a",
        encoding="utf-8",
    ) as file:
        file.write("\n")
        cleaned_user_prompt = re.sub(r"[\s*]+", " ", user_prompt.strip())
        file.write(cleaned_user_prompt)
        file.write("\n")
        cleaned_llm_answer = re.sub(r"[\s*]+", " ", llm_answer.strip())
        file.write(cleaned_llm_answer)

    return llm_answer


if __name__ == "__main__":
    collection_name = "ms_dhoni"
    user_prompt = "disceipency wrt captiancy of csk"
    start_chatbot(user_prompt, collection_name)
