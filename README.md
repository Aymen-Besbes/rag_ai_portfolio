Perfect! Here’s your **final, reordered, polished README** in `.md` format, ready to drop into your repo:

````markdown
# 🧠 AI Portfolio RAG Assistant

A **Retrieval-Augmented Generation (RAG)** application for querying a structured professional portfolio or resume using natural language.  
Powered by **Sentence Transformers**, **FAISS**, and **Google Gemini**, it retrieves relevant resume chunks and generates structured, factual answers.

---

## ⚡ Key Features
- Semantic retrieval of resume/portfolio chunks.
- Structured summarization of projects, experiences, and skills.
- Highlights projects and skills in responses.
- Interactive chat interface via Streamlit.

---

## 🚀 Quick Start
Run the app in under a minute:

```bash
git clone https://github.com/Aymen-Besbes/ai_portfolio_rag.git
cd ai_portfolio_rag

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate     # Linux/Mac
venv\Scripts\activate        # Windows

# Install dependencies
pip install -r requirements.txt

# Launch Streamlit app
streamlit run src/app.py
````

---

## ⚙️ Setup & Configuration

### 1. Configure Environment Variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=<YOUR_GEMINI_API_KEY>
EMBEDDING_MODEL=<YOUR_EMBEDDING_MODEL>
MODEL=<YOUR_MODEL>
INDEX_PATH=embeddings/faiss_index.bin
CHUNKS_PATH=embeddings/chunks.json
RESUME_PATH=data/resume.txt
CHUNK_SIZE=<CHUNK_SIZE>
CHUNK_OVERLAP=<CHUNK_OVERLAP>
TOP_K=<TOP_K_CHUNKS>
```

### 2. Add Your Resume / Portfolio

Place a structured Markdown text file under `data/`:

```markdown
# Summary
[Short professional summary]

# Professional Experiences
## Job Title — Company (Start – End)
### Objective:
[Role description]
### Responsibilities & Achievements:
- Bullet points with measurable results
### Technologies / Skills:
[Skills & tools]

# Projects
## Project 1: Project Name (Month Year)
### Objective:
[Project objective]
### Key Features:
- Feature 1
- Feature 2
### Responsibilities / Role:
- Tasks performed
### Results / Achievements:
- Metrics/outcomes
### Technologies / Skills Used:
[Skills]
### Current Status:
[Completed / Active / Prototype]
```

---

## 🔄 RAG Pipeline & Modules

### Pipeline Flow

```mermaid
flowchart TD
    A[Raw Resume] --> B[Chunking]
    B --> C[Embedding]
    C --> D[FAISS Index & Chunks]
    E[User Query] --> F[Retrieve Top-k Chunks]
    F --> G[Build Prompt (prompt_gen.py)]
    G --> H[Google Gemini API (chat.py)]
    H --> I[Structured Answer]
```

### Pipeline Components

1. **Chunking (`chunking.py`)**

   * Parses Markdown resume into semantic chunks (Summary, Experiences, Projects, Languages).
   * Preserves context and section relationships using a buffer.

2. **Embeddings (`embedding.py`)**

   * Generates embeddings for chunks using **Sentence Transformers**.
   * Creates FAISS index for efficient similarity search.

3. **Retrieval (`retrieval.py`)**

   * Lazy-loads FAISS index and chunk data.
   * Retrieves top-k relevant chunks for user queries.

4. **Prompt Generation (`prompt_gen.py`)**

   * Constructs structured prompts for **Google Gemini**.
   * Includes context, system instructions, and user query.

5. **RAG Chat (`chat.py`)**

   * Combines retrieval and prompt generation.
   * Sends prompt to Gemini API and returns structured answers.

6. **Web App (`app.py`)**

   * Streamlit frontend for interactive queries.

---

## 📁 Project Structure

```plaintext
ai_portfolio_rag/
├── data/                # Raw resume text file
│   └── resume.txt
├── embeddings/ 
│   ├── faiss_index.bin
│   └── chunks.json
├── src/ 
│   ├── app.py           # Streamlit frontend
│   ├── chat.py          # Chat interface & model integration
│   ├── chunking.py      # Resume chunking logic
│   ├── config.py        # Environment variables & constants
│   ├── embedding.py     # Embedding generation + FAISS index builder
│   ├── prompt_gen.py    # Prompt generator for Gemini
│   ├── retrieval.py     # Retrieve relevant chunks via FAISS
│   └── evaluate.py      # Evaluate retrieval and generation
├── requirements.txt     # Python dependencies
├── .env                 # API keys and configuration
└── README.md
```

---

## 📊 Evaluation

Metrics used to evaluate QA performance:

* **Projects Recall** ✅ – Fraction of expected projects correctly retrieved.
* **Faithfulness** 🎯 – Whether answers are grounded in retrieved data.
* **Context Precision** 📌 – Fraction of retrieved chunks actually referenced.

| Query                      | Projects Recall | Faithfulness | Context Precision |
| -------------------------- | --------------- | ------------ | ----------------- |
| Healthcare Projects        | 1.0             | 1.0          | 1.0               |
| Machine Learning Projects  | 0.75            | 1.0          | 1.0               |
| Dashboards / Visualization | 1.0             | 1.0          | 1.0               |

---

## ⚡ Potential Enhancements

* Multi-format resume support (PDF, DOCX, HTML).
* Combine semantic and keyword-based retrieval with re-ranking.
* Multi-user support and session histories.
* Expand to multiple resumes or portfolios.
* Streaming LLM responses for faster interaction.

---

## 📬 Contact

**Author:** Aymen Besbes
**Email:** [Aymen.besbes@outlook.com](mailto:Aymen.besbes@outlook.com) | [Aymen.besbes@ensi-uma.tn](mailto:Aymen.besbes@ensi-uma.tn)
**LinkedIn:** [https://www.linkedin.com/in/aymen-besbes](https://www.linkedin.com/in/aymen-besbes)

```


