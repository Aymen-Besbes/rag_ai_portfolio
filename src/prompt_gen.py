from collections import defaultdict

def build_prompt(query, retrieved_chunks):
    """
    Builds a RAG prompt with clear instructions and context.
    
    Args:
        query (str): The user query.
        retrieved_chunks (list[tuple[str, float]] or list[str]): Retrieved chunks from retrieval.
        
    Returns:
        str: A full prompt string to send to the LLM.
    """
    # Extract chunk text if tuples are provided
    chunk_texts = []
    for c in retrieved_chunks:
        if isinstance(c, tuple):
            chunk_texts.append(c[0])  # take only text, ignore score
        else:
            chunk_texts.append(c)

    # Remove exact duplicates while preserving order
    seen = set()
    unique_chunks = []
    for chunk in chunk_texts:
        if chunk not in seen:
            unique_chunks.append(chunk)
            seen.add(chunk)

    # Categorize chunks roughly by headings
    categorized = {"Experience": [], "Projects": [], "Other": []}
    for chunk in unique_chunks:
        header_line = chunk.split("\n", 1)[0].strip()
        if header_line.startswith("## Project") or header_line.startswith("## P"):
            categorized["Projects"].append(chunk)
        elif header_line.startswith("##") or header_line.startswith("# Professional Experiences"):
            categorized["Experience"].append(chunk)
        else:
            categorized["Other"].append(chunk)

    # Merge chunks per category
    context = ""
    for cat_name, chunks_list in categorized.items():
        if not chunks_list:
            continue
        context += f"\n### {cat_name} Context:\n"
        for i, c in enumerate(chunks_list, 1):
            context += f"- {c}\n"

    # System instructions
    system_prompt = """You are an AI-powered portfolio assistant for John. Your sole role is to respond to user queries about John’s professional experience, skills, and projects.
Rules:
- Provide structured, factual answers ONLY from context.
- For project lists, include all projects using their titles and objectives.
- Use bullet points for achievements.
- Highlight project names and skills in bold where appropriate.
- Resolve pronouns in follow-ups using context.
- If the user asks to **list projects**, include all retrieved chunks under the "Projects" category.
  - For each project, use the available Objective or title as the short description.
  - Ignore Key Features, Results, or Technologies unless explicitly asked.
  - Format each as: "**[Project Name]:** [Short Description]".
- When multiple relevant contexts exist, summarize or merge them concisely.
- Use bullet points for achievements or lists.
- If the question concerns skills or technologies, specify the related project or experience.
- Use the phrasing: "Applied [Skill] in …" when referring to skills used in projects.
"""

    # Short example
    examples = """
### Example 1: AI/ML Experience
Q: What is John's experience with AI?
A:
- Designed and deployed LLM-based knowledge assistants.
- Built RAG pipelines for document summarization.
- Implemented microservices for scalable AI inference.
"""

    # Combine everything into the full prompt
    full_prompt = f"""{system_prompt}

{examples}

### CONTEXTS:
{context}

### USER QUESTION:
{query}

### FINAL ANSWER:"""

    return full_prompt
