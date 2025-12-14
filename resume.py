import fitz  # PyMuPDF
import re

def parse_resume(file_path):
    with fitz.open(file_path) as doc:
        text = "".join([page.get_text() for page in doc])

    skills = re.findall(r'\b(Python|ML|AI|Data|React|AWS|Java|C\+\+)\b', text, re.I)
    experience = re.findall(r'(internship|project|worked at .*?)\.', text, re.I)

    return {
        "text": text,
        "skills": list(set(skills)),
        "experience": list(set(experience))
    }
