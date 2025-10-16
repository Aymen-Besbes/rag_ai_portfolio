from collections import defaultdict

def build_prompt(query, retrieved_chunks):
    """
    Builds a RAG prompt with clear instructions and context.
    """
    merged_chunks = defaultdict(list)
    for chunk in retrieved_chunks:
        key = chunk  
        merged_chunks[key].append(chunk)

    context = ""
    for i, (title, contents) in enumerate(merged_chunks.items()):
        context += f"\n### Context {i+1}:\n" + "\n".join(contents) + "\n"

    system_prompt = """You are an AI assistant summarizing Aymen Besbes' professional portfolio.
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

    examples = """
### Example 1: Android Experience
Q: What is Aymen's experience with Android?
A:
- Developed an AI-assisted desktop application for Automotive Android log analysis.
- Implemented anomaly detection using NLP and unsupervised ML models.
- Automated log analysis workflows, reducing manual review time by 60%.

"""

    full_prompt = f"""{system_prompt}

{examples}

### CONTEXTS:
{context}

### USER QUESTION:
{query}

### FINAL ANSWER:"""

    return full_prompt
