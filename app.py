from flask import Flask, request, send_file, render_template
from PIL import Image
from fpdf import FPDF
import os, io

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/convert", methods=["POST"])
def convert():
    file = request.files["file"]
    conversion = request.form["conversion"]
    filename = file.filename
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    output = io.BytesIO()

    # IMAGE → PDF
    if conversion == "img_to_pdf":
        img = Image.open(filepath).convert("RGB")
        img.save(output, format="PDF")
        output.seek(0)
        return send_file(output, mimetype="application/pdf",
                         download_name="converted.pdf", as_attachment=True)

    # PDF → IMAGE (first page)
    elif conversion == "pdf_to_img":
        from pdf2image import convert_from_path
        pages = convert_from_path(filepath, dpi=150)
        pages[0].save(output, format="PNG")
        output.seek(0)
        return send_file(output, mimetype="image/png",
                         download_name="converted.png", as_attachment=True)

    # IMAGE → PNG / JPG
    elif conversion in ("to_png", "to_jpg"):
        fmt = "PNG" if conversion == "to_png" else "JPEG"
        img = Image.open(filepath).convert("RGB")
        img.save(output, format=fmt)
        output.seek(0)
        mime = "image/png" if fmt == "PNG" else "image/jpeg"
        ext  = "png" if fmt == "PNG" else "jpg"
        return send_file(output, mimetype=mime,
                         download_name=f"converted.{ext}", as_attachment=True)

    return "Unsupported conversion", 400

if __name__ == "__main__":
    
    
    app.run(debug=True)