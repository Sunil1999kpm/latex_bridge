from flask import Flask, request, jsonify
from gradio_client import Client
import requests
import tempfile
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ LaTeX Compiler API is running. Use /compile (JSON)."

@app.route('/compile', methods=['GET','POST'])
def compile_latex():
    try:
        data = request.get_json()
        latex_code = data.get('latex_code', '')

        if not latex_code.strip():
            return jsonify({"error": "Missing 'latex_code' field"}), 400

        # Connect to your Hugging Face Space
        client = Client("SuHugging123/Latex_Compiler")
        result = client.predict(latex_code=latex_code, api_name="/compile_latex")

        pdf_url = result[0]

        # Verify that the returned URL actually works
        response = requests.get(pdf_url)
        if response.status_code != 200:
            return jsonify({"error": "Failed to retrieve compiled PDF from Hugging Face"}), 502

        # Save to temporary file
        temp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        temp.write(response.content)
        temp.close()

        # Generate a temporary public link (Render doesn’t host files, so we return the Hugging Face URL)
        return jsonify({
            "status": "success",
            "message": "PDF compiled successfully",
            "pdf_url": pdf_url
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7860)
