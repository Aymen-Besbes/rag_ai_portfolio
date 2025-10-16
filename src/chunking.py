import re
from config import RESUME_PATH

def chunk_resume_data(resume_text):
    """
    Splits a resume into meaningful chunks, preserving sections and context.

    Args:
        resume_text (str): Full text of the resume.

    Returns:
        list[str]: Each string is a logical chunk of the resume.
    """
    chunks = []
    lines = resume_text.split('\n')

    current_section = None
    current_job_title_company = None
    current_project_name = None
    buffer = []

    def flush_buffer(prefix=None):
        """Convert buffer to a chunk if it has content, then clear buffer."""
        if buffer:
            content = "\n".join(buffer).strip()
            if content:
                if prefix:
                    chunks.append(f"{prefix}\n{content}")
                else:
                    chunks.append(content)
            buffer.clear()

    for line in lines:
        line = line.strip()

        # --- Top-level sections ---
        if line.startswith('# Summary'):
            flush_buffer()
            current_section = 'summary'
            chunks.append(line)
        elif line.startswith('# Professional Experiences'):
            flush_buffer()
            current_section = 'professional_experiences'
        elif line.startswith('# Projects'):
            flush_buffer()
            current_section = 'projects'
        elif line.startswith('# Languages'):
            flush_buffer()
            current_section = 'languages'
            chunks.append(line)

        # --- Summary and Languages content ---
        elif current_section in ('summary', 'languages') and line and not line.startswith('#'):
            chunks[-1] += f"\n{line}"

        # --- Professional Experiences ---
        elif current_section == 'professional_experiences':
            job_match = re.match(r'##\s*([^—]+)\s*—\s*([^(\n]+)\s*\(([^)]+)\)', line)
            if job_match:
                flush_buffer(prefix=f"**{current_job_title_company}**" if current_job_title_company else None)
                current_job_title = job_match.group(1).strip()
                current_company = job_match.group(2).strip()
                current_job_title_company = f"{current_job_title} — {current_company}"
                chunks.append(f"**{current_job_title_company}** ({job_match.group(3).strip()})")
                buffer.clear()
            elif line.startswith(('### Objective:', '### Responsibilities & Achievements:', '### Technologies / Skills:')):
                flush_buffer(prefix=f"**{current_job_title_company}**")
                buffer.append(line)
            elif line.startswith('-') and buffer:
                buffer.append(line)
            elif line and buffer and not line.startswith('###'):
                buffer.append(line)

        # --- Projects ---
        elif current_section == 'projects':
            project_match = re.match(r'##\s*Project\s*\d+:\s*(.+)', line)
            if project_match:
                flush_buffer(prefix=f"**{current_project_name}**" if current_project_name else None)
                current_project_name = f"Project {project_match.group(0).split(':')[0].split(' ')[1]}: {project_match.group(1).strip()}"
                chunks.append(f"**{current_project_name}**")
                buffer.clear()
            elif line.startswith(('### Timeline:', '### Objective:', '### Key Features:',
                                  '### Responsibilities / Role:', '### Results / Achievements:',
                                  '### Technologies / Skills Used:', '### Current Status:')):
                flush_buffer(prefix=f"**{current_project_name}**")
                buffer.append(line)
            elif line.startswith('-') and buffer:
                buffer.append(line)
            elif line and buffer and not line.startswith('###'):
                buffer.append(line)

    # Flush any remaining buffer content at the end
    flush_buffer(prefix=f"**{current_job_title_company}**" if current_job_title_company else f"**{current_project_name}**" if current_project_name else None)

    # Remove empty or meaningless chunks
    final_chunks = [chunk.strip() for chunk in chunks if chunk.strip() and not re.match(r'^#+\s*$', chunk.strip())]

    return final_chunks


if __name__ == "__main__":
    with open(RESUME_PATH, 'r', encoding='utf-8') as f:
        resume_text = f.read()
    chunks = chunk_resume_data(resume_text)
    print(f"Generated {len(chunks)} chunks.\n")
    for i, chunk in enumerate(chunks, start=1):
        print(f"--- Chunk {i} ---")
        print(chunk)
        print('-' * 20)
