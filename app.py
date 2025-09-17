from flask import Flask, render_template, request
import re
import fitz  # PyMuPDF for PDFs

app = Flask(__name__)

# Knowledge base of equations
EQUATION_KB = {
    "E=mc^2": {
        "author": "Albert Einstein",
        "description": "Mass-energy equivalence formula from the theory of relativity.",
        "variables": {"E": "Energy", "m": "Mass", "c": "Speed of light"}
    },
    "F=ma": {
        "author": "Isaac Newton",
        "description": "Newton's Second Law of Motion.",
        "variables": {"F": "Force", "m": "Mass", "a": "Acceleration"}
    },
    "V=IR": {
        "author": "Georg Ohm",
        "description": "Ohm's Law relating voltage, current, and resistance.",
        "variables": {"V": "Voltage", "I": "Current", "R": "Resistance"}
    }
}

def extract_text_from_pdf(file_path):
    """Extract text from PDF using PyMuPDF"""
    text = ""
    doc = fitz.open(file_path)
    for page in doc:
        text += page.get_text()
    return text

def find_equations(text):
    """Find equations by simple regex"""
    return re.findall(r"[A-Za-z]+\s*=\s*[^ \n]+", text)

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    unrecognized = []
    query = ""

    if request.method == "POST":
        query = request.form.get("question", "")
        uploaded_file = request.files.get("file")

        text_content = ""
        if uploaded_file and uploaded_file.filename != "":
            if uploaded_file.filename.endswith(".pdf"):
                uploaded_file.save("temp.pdf")
                text_content = extract_text_from_pdf("temp.pdf")
            elif uploaded_file.filename.endswith(".txt"):
                text_content = uploaded_file.read().decode("utf-8")

        # Prioritize user question
        equations = find_equations(query) if query else find_equations(text_content)

        for eq in equations:
            eq_clean = eq.split("|")[0].replace(" ", "").strip()
            if eq_clean in EQUATION_KB:
                # Ensure 'variables' exists
                eq_info = EQUATION_KB[eq_clean]
                if "variables" not in eq_info:
                    eq_info["variables"] = {}
                results.append({"equation": eq_clean, "info": eq_info})
            else:
                unrecognized.append(eq)

    return render_template("index.html", results=results, unrecognized=unrecognized, query=query)

if __name__ == "__main__":
    app.run(debug=True)
