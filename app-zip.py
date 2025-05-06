from flask import Flask, request, send_file
from flask_cors import CORS
import cairosvg
import os
import tempfile
import zipfile

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return '<h2>EPS Converter API — /convert-to-eps or /convert-zip</h2>'

@app.route('/convert-to-eps', methods=['POST'])
def convert_to_eps():
    # versi single file (tetap bisa dipakai)
    ...

@app.route('/convert-zip', methods=['POST'])
def convert_zip():
    if 'files' not in request.files:
        return "No SVG files uploaded.", 400

    files = request.files.getlist('files')
    zip_path = tempfile.NamedTemporaryFile(delete=False, suffix='.zip').name

    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for svg_file in files:
            with tempfile.NamedTemporaryFile(suffix='.svg', delete=False) as tmp_svg:
                svg_path = tmp_svg.name
                svg_file.save(svg_path)

            eps_path = svg_path.replace('.svg', '.eps')

            try:
                cairosvg.svg2eps(url=svg_path, write_to=eps_path)
                eps_name = os.path.basename(svg_file.filename).replace('.svg', '.eps')
                zipf.write(eps_path, eps_name)
            except Exception as e:
                return f"Conversion error for {svg_file.filename}: {str(e)}", 500
            finally:
                os.remove(svg_path)
                if os.path.exists(eps_path):
                    os.remove(eps_path)

    return send_file(zip_path, mimetype='application/zip', as_attachment=True, download_name='converted_eps.zip')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 3000))
    app.run(host='0.0.0.0', port=port)
