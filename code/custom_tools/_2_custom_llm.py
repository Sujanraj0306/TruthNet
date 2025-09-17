from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM


def custom_llm_function(prompt_template, user_prompt):

    prompt = ChatPromptTemplate.from_template(prompt_template)
    model = OllamaLLM(model="gemma3:4b")
    chain = prompt | model
    result = chain.invoke({"question": user_prompt})

    return result


if __name__ == "__main__":
    user_prompt = "what is langchain"
    prompt_template = """
    You are an expert academic chatbot give answer
    Question: {question}
    Answer: """
    print(custom_llm_function(prompt_template, user_prompt))
