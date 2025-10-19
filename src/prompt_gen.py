def build_prompt(query, retrieved_chunks):
    """
    Builds a RAG prompt with categorized context for an LLM.
    - Categorizes chunks by headers: Experience vs Projects.
    - Preserves order and removes duplicates.
    - Includes short examples for guidance.
    """
    # Remove duplicates, preserve order
    unique_chunks = list(dict.fromkeys(retrieved_chunks))

    # Categorize chunks
    categorized = {"Experience": [], "Projects": [], "Other": []}
    for chunk in unique_chunks:
        header_line = chunk.split("\n", 1)[0].strip()
        if header_line.startswith("## Project") or header_line.startswith("## Projects"):
            categorized["Projects"].append(chunk)
        elif header_line.startswith("##") or header_line.startswith("# Professional Experiences"):
            categorized["Experience"].append(chunk)
        else:
            categorized["Other"].append(chunk)

    # Build context section
    context = ""
    for category, chunks in categorized.items():
        if not chunks:
            continue
        context += f"\n### {category} Contexts:\n"
        for chunk in chunks:
            context += f"{chunk}\n"

    # System prompt instructions
    system_prompt = """You are an expert AI assistant specializing in summarizing professional portfolios and resumes. 
Your goal is to provide accurate, concise, and structured answers based solely on the provided context. 
Always ensure factual correctness and clarity.

Guidelines:
1. Base your answers strictly on the retrieved context. Do NOT hallucinate or assume information.
2. Highlight **project names, company names, skills, and technologies** in bold where appropriate.
3. Use bullet points for achievements, skills, or lists.
4. When describing skills, use the phrasing: "Applied [Skill] in [Project/Experience]."
5. For project lists:
   - Include the title and objective as the main description.
   - Ignore Key Features, Results, or Technologies unless explicitly asked.
   - Format each project as: "**[Project Name]:** [Short Description]".
6. For experience summaries:
   - Focus on responsibilities,dates, achievements, and skills applied.
   - Organize answers in chronological or logical order.
7. Resolve pronouns and ambiguous references using the context.
8. If multiple relevant contexts exist, summarize and merge concisely without losing details.
9. Maintain a professional, neutral tone.

"""

    # Short example queries
    examples = """
### Example 1: List Projects
Q: List all projects John worked on.
A:
- **Enterprise Knowledge Assistant:** Build an internal RAG-based chatbot using LLMs to answer employee queries.
- **RAG Document Summarizer:** Automate summarization of internal knowledge and research documents using LLMs.
- **Chatbot for Customer Support:** Deploy a GPT-based chatbot for enterprise customer support.

### Example 2: Experience Summary
Q: Summarize John's experience as an AI Engineer.
A:
- Architected and deployed multilingual LLM and RAG pipelines.
- Integrated AI solutions into enterprise platforms, improving efficiency by 30%.
- Mentored junior engineers on prompt engineering and model optimization.

### Example 3: Skills Inquiry
Q: What skills did John apply in his projects?
A:
- Applied **Python, FAISS, and HuggingFace Transformers** in building RAG pipelines.
- Applied **Docker and Kubernetes** for scalable deployment.
- Applied **Streamlit and SQL** for data analysis dashboards.
"""

    full_prompt = f"""{system_prompt}

{examples}

### CONTEXTS:
{context}

### USER QUESTION:
{query}

### FINAL ANSWER:"""

    return full_prompt
