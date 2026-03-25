from flask import Flask, request, send_file, render_template
from PIL import Image
import os, io, tempfile, gc

app = Flask(__name__, static_folder="public", static_url_path="")

UPLOAD_FOLDER = tempfile.gettempdir()
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# ── Allowed input formats per conversion ────────
CONVERSION_RULES = {
    "img_to_pdf": [".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff"],
    "pdf_to_img": [".pdf"],
    "to_png":     [".jpg", ".jpeg", ".webp", ".bmp", ".tiff", ".gif"],
    "to_jpg":     [".png", ".webp", ".bmp", ".tiff", ".gif"],
}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/convert", methods=["POST"])
def convert():
    # ── Validate input ───────────────────────────
    if "file" not in request.files:
        return "No file uploaded.", 400

    file       = request.files["file"]
    conversion = request.form.get("conversion", "")

    if file.filename == "":
        return "No file selected.", 400

    if conversion not in CONVERSION_RULES:
        return "Unsupported conversion type.", 400

    # ── Validate file extension ──────────────────
    ext     = os.path.splitext(file.filename)[-1].lower()
    allowed = CONVERSION_RULES[conversion]
    if ext not in allowed:
        return (
            f"Wrong file type '{ext}' for this conversion. "
            f"Expected one of: {', '.join(allowed)}"
        ), 400

    # ── Save to /tmp with unique name ────────────
    tmpfile  = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=ext,
        dir=app.config["UPLOAD_FOLDER"]
    )
    filepath = tmpfile.name
    tmpfile.close()
    file.save(filepath)

    output   = io.BytesIO()
    img      = None   # track open objects so we can close before delete
    pdf      = None

    try:
        # ── Image → PDF ──────────────────────────
        if conversion == "img_to_pdf":
            img = Image.open(filepath).convert("RGB")
            img.save(output, format="PDF")
            img.close()
            img = None
            output.seek(0)
            return send_file(
                output,
                mimetype="application/pdf",
                download_name="converted.pdf",
                as_attachment=True,
            )

        # ── PDF → Image (first page) ─────────────
        elif conversion == "pdf_to_img":
            import pypdfium2 as pdfium
            pdf     = pdfium.PdfDocument(filepath)
            page    = pdf[0]
            bitmap  = page.render(scale=2)
            pil_img = bitmap.to_pil()
            bitmap  = None
            page    = None
            pdf.close()
            pdf = None
            pil_img.save(output, format="PNG")
            pil_img.close()
            output.seek(0)
            return send_file(
                output,
                mimetype="image/png",
                download_name="converted.png",
                as_attachment=True,
            )

        # ── Any Image → PNG ──────────────────────
        elif conversion == "to_png":
            img = Image.open(filepath).convert("RGBA")
            img.save(output, format="PNG")
            img.close()
            img = None
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
            img.close()
            img = None
            output.seek(0)
            return send_file(
                output,
                mimetype="image/jpeg",
                download_name="converted.jpg",
                as_attachment=True,
            )

    except Exception as e:
        return f"Conversion failed: {str(e)}", 500

    finally:
        # ── Close any open handles before deleting ─
        try:
            if img is not None:
                img.close()
            if pdf is not None:
                pdf.close()
        except Exception:
            pass

        # ── Force garbage collection (Windows needs this) ──
        gc.collect()

        # ── Delete temp file ─────────────────────
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
        except PermissionError:
            pass   # Windows sometimes holds the lock briefly — skip silently


if __name__ == "__main__":
    app.run(debug=True)