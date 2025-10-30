from flask import Flask, request, jsonify, send_file
from gradio_client import Client
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Flask Bridge is running."

@app.route('/compile', methods=['GET', 'POST'])
def compile_latex():
    # If GET -> simple test message
    if request.method == 'GET':
        return jsonify({
            "message": "✅ LaTeX Bridge API is active. Send a POST request with 'latex_code'."
        })

    try:
        latex_code = ""

        # Handle JSON POST
        if request.is_json:
            data = request.get_json(silent=True) or {}
            latex_code = data.get("latex_code", "")
        else:
            latex_code = request.data.decode("utf-8").strip()

        if not latex_code:
            return jsonify({"error": "No LaTeX code provided"}), 400

        client = Client("SuHugging123/Latex_Compiler")
        result = client.predict(latex_code=latex_code, api_name="/compile_latex")
        pdf_path = result[0]

        if not os.path.exists(pdf_path):
            return jsonify({"error": "PDF not found"}), 404

        return send_file(pdf_path, as_attachment=True, download_name="compiled.pdf")

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860)
