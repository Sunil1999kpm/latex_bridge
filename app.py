from flask import Flask, request, send_file, jsonify
import subprocess, os

app = Flask(__name__)

def compile_latex(latex_code):
    os.makedirs("workspace", exist_ok=True)
    tex_path = "workspace/document.tex"
    pdf_path = "workspace/document.pdf"

    with open(tex_path, "w", encoding="utf-8") as f:
        f.write(latex_code)

    result = subprocess.run(
        ["pdflatex", "-interaction=nonstopmode", "document.tex"],
        cwd="workspace",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=30
    )

    if result.returncode != 0 or not os.path.exists(pdf_path):
        return None, result.stdout.decode(errors="ignore")

    return pdf_path, "✅ PDF compiled successfully."

# ======================
# JSON endpoint (for API)
# ======================
@app.route("/compile", methods=["POST"])
def compile_json():
    data = request.get_json()
    latex_code = data.get("latex_code", "")
    pdf_path, status = compile_latex(latex_code)
    if pdf_path:
        return send_file(pdf_path, as_attachment=True, download_name="compiled.pdf")
    return jsonify({"error": status}), 400

# ======================
# Plain-text endpoint (for Make.com)
# ======================
@app.route("/plain_compile", methods=["POST"])
def compile_plain():
    latex_code = request.data.decode("utf-8").strip()
    pdf_path, status = compile_latex(latex_code)
    if pdf_path:
        return send_file(pdf_path, as_attachment=True, download_name="compiled.pdf")
    return jsonify({"error": status}), 400

@app.route("/", methods=["GET"])
def home():
    return "✅ LaTeX Compiler API is running. Use /compile (JSON) or /plain_compile (text/plain)."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
