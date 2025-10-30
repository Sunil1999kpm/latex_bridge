from flask import Flask, request, send_file, jsonify
from gradio_client import Client
import tempfile
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ LaTeX Compiler API is running. Use /compile (JSON)."

@app.route('/compile', methods=['POST'])
def compile_latex():
    try:
        data = request.get_json()
        latex_code = data.get('latex_code', '')

        # Call Hugging Face Space
        client = Client("SuHugging123/Latex_Compiler")
        result = client.predict(latex_code=latex_code, api_name="/compile_latex")

        pdf_url = result[0]  # should be a URL to the compiled PDF
        response = requests.get(pdf_url)

        temp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        temp.write(response.content)
        temp.close()

        return send_file(temp.name, as_attachment=True, download_name="compiled.pdf")

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7860)
