from flask import Flask, request, send_file
import cairosvg
import os
import tempfile

app = Flask(__name__)

@app.route('/convert-to-eps', methods=['POST'])
def convert_to_eps():
    if 'file' not in request.files:
        return "No file uploaded", 400

    svg_file = request.files['file']

    with tempfile.NamedTemporaryFile(suffix='.svg', delete=False) as tmp_svg:
        svg_path = tmp_svg.name
        svg_file.save(svg_path)

    eps_path = svg_path.replace('.svg', '.eps')

    try:
        cairosvg.svg2eps(url=svg_path, write_to=eps_path)
        return send_file(eps_path, mimetype='application/postscript', as_attachment=True, download_name='converted.eps')
    except Exception as e:
        return f"Conversion error: {e}", 500
    finally:
        # Cleanup
        if os.path.exists(svg_path):
            os.remove(svg_path)
        if os.path.exists(eps_path):
            os.remove(eps_path)

if __name__ == '__main__':
    app.run(port=3000)
