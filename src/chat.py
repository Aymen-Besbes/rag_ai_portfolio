from retrieval import retrieve
from prompt_gen import build_prompt
from config import GEMINI_API_KEY, MODEL, TOP_K
from google import genai

# Initialize the GenAI client
client = genai.Client(api_key=GEMINI_API_KEY)

def query_portfolio(user_query: str, top_k: int = TOP_K) -> str:
    """
    Queries John's professional portfolio using RAG.

    Args:
        user_query (str): User question.
        top_k (int): Number of top chunks to retrieve.

    Returns:
        str: LLM-generated answer.
    """
    # Retrieve top-k relevant chunks
    chunks = retrieve(user_query, top_k)
    if not chunks:
        return "No relevant information found in the portfolio."

    # Convert to strings if tuples are returned (chunk_text, score)
    string_chunks = [c[0] if isinstance(c, tuple) else c for c in chunks]

    # Build prompt
    prompt = build_prompt(user_query, string_chunks)

    # Generate response
    try:
        response = client.models.generate_content(model=MODEL, contents=prompt)
        return response.text.strip() if response.text else "No response generated."
    except Exception as e:
        return f"Error generating response: {e}"


if __name__ == "__main__":
    print("=== Portfolio RAG Assistant ===\n(Type 'exit' or 'quit' to stop)\n")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting Portfolio Assistant. Goodbye!")
            break
        if not user_input:
            continue

        answer = query_portfolio(user_input)
        print(f"\nAssistant:\n{answer}\n")
