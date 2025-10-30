from flask import Flask, request, send_file, jsonify
from gradio_client import Client
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Flask Bridge is running."

@app.route('/compile', methods=['POST'])
def compile_latex():
    try:
        # Ensure JSON input
        if not request.is_json:
            return jsonify({"error": "Content-Type must be application/json"}), 400

        data = request.get_json()
        latex_code = data.get('latex_code', '')

        if not latex_code.strip():
            return jsonify({"error": "Missing or empty 'latex_code'"}), 400

        # Connect to Hugging Face LaTeX compiler
        client = Client("SuHugging123/Latex_Compiler")
        result = client.predict(latex_code=latex_code, api_name="/compile_latex")

        pdf_path = result[0]  # Hugging Face returns (file_path, message)

        if not os.path.exists(pdf_path):
            return jsonify({"error": "Compiled PDF not found"}), 404

        return send_file(pdf_path, as_attachment=True, download_name="compiled.pdf")

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7860)
