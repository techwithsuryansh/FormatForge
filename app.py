from flask import Flask, request, send_file, render_template
from PIL import Image
from fpdf import FPDF
import os, io, tempfile

app = Flask(__name__, static_folder="public", static_url_path="")

UPLOAD_FOLDER = tempfile.gettempdir()
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/convert", methods=["POST"])
def convert():
    # ── Validate input ──────────────────────────
    if "file" not in request.files:
        return "No file uploaded.", 400

    file       = request.files["file"]
    conversion = request.form.get("conversion", "")

    if file.filename == "":
        return "No file selected.", 400

    # ── Save uploaded file to /tmp ───────────────
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(filepath)

    output = io.BytesIO()

    try:
        # ── Image → PDF ──────────────────────────
        if conversion == "img_to_pdf":
            img = Image.open(filepath).convert("RGB")
            img.save(output, format="PDF")
            output.seek(0)
            return send_file(
                output,
                mimetype="application/pdf",
                download_name="converted.pdf",
                as_attachment=True,
            )

        # ── PDF → Image (first page) ─────────────
        elif conversion == "pdf_to_img":
            try:
                from pdf2image import convert_from_path
                pages = convert_from_path(filepath, dpi=150)
                pages[0].save(output, format="PNG")
                output.seek(0)
                return send_file(
                    output,
                    mimetype="image/png",
                    download_name="converted.png",
                    as_attachment=True,
                )
            except Exception:
                return "PDF to image conversion failed. Poppler may not be available on this server.", 500

        # ── Any Image → PNG ──────────────────────
        elif conversion == "to_png":
            img = Image.open(filepath).convert("RGBA")
            img.save(output, format="PNG")
            output.seek(0)
            return send_file(
                output,
                mimetype="image/png",
                download_name="converted.png",
                as_attachment=True,
            )

        # ── Any Image → JPG ──────────────────────
        elif conversion == "to_jpg":
            img = Image.open(filepath).convert("RGB")
            img.save(output, format="JPEG", quality=90)
            output.seek(0)
            return send_file(
                output,
                mimetype="image/jpeg",
                download_name="converted.jpg",
                as_attachment=True,
            )

        else:
            return "Unsupported conversion type.", 400

    except Exception as e:
        return f"Conversion failed: {str(e)}", 500

    finally:
        # ── Clean up temp file ───────────────────
        if os.path.exists(filepath):
            os.remove(filepath)


if __name__ == "__main__":
    app.run(debug=True)