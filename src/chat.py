from retrieval import retrieve
from prompt_gen import build_prompt
from config import GEMINI_API_KEY, MODEL
from google import genai

client = genai.Client(api_key=GEMINI_API_KEY)

def query_portfolio(user_query, top_k=20):
    chunks = retrieve(user_query, top_k)
    if not chunks:
        return "No relevant information found in the portfolio."
    prompt = build_prompt(user_query, chunks)
    response = client.models.generate_content(model=MODEL, contents=prompt)
    return response.text.strip()

if __name__ == "__main__":
    print("=== Portfolio RAG Assistant ===")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        answer = query_portfolio(user_input)
        print(f"Assistant:\n{answer}\n")
