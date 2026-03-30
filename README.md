<div align="center">

<h1>FormatForge</h1>

<p>A clean, fast, multi-format file converter built with Python & Flask.<br/>Convert images, PDFs and more — instantly, in your browser.</p>

<p>
  <img src="https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Flask-3.x-000000?style=for-the-badge&logo=flask&logoColor=white"/>
  <img src="https://img.shields.io/badge/Pillow-imaging-blue?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge"/>
</p>

<p>
  <a href="https://formatforge-live.vercel.app">
    <img src="https://img.shields.io/badge/Live_Demo-formatforge--live.vercel.app-orange?style=for-the-badge"/>
</a>
</p>

</div>

---

##  Overview

**FormatForge** is a web-based file conversion tool that lets you convert between image and document formats without any sign-up, no cloud uploads, and no third-party services. Everything runs locally on your own machine or server.

>  Supports **dark & light theme** with preference saved in `localStorage`

---

##  Features

| Feature | Description |
|---|---|
|  Image → PDF | Convert JPG, PNG, WEBP files into a PDF document |
|  PDF → Image | Extract the first page of any PDF as a PNG |
|  Format swap | Re-encode any image between PNG and JPG |
|  Theme toggle | Dark / light mode, persisted across sessions |
|  Drag & Drop | Drop files directly onto the upload zone |
|  No reload | Fetch API handles upload + download in the background |
|  Responsive | Works on mobile, tablet, and desktop |

---

##  Project Structure

```
/
├── app.py                
├── requirements.txt       
├── Procfile                 
├── .gitignore
├── README.md
│
├── templates/
│   └── index.html      
│
└── static/
    ├── css/
    │   └── style.css    
    └── js/
        └── main.js       
```

---
## 🔧 Supported Conversions

| Input format | Output format | Status |
|---|---|---|
| JPG, PNG, WEBP | PDF | ✅ Available |
| PDF | PNG | ✅ Available |
| Any image | PNG | ✅ Available |
| Any image | JPG | ✅ Available |
| DOCX | PDF | 🔜 Coming soon |
| CSV | JSON | 🔜 Coming soon |

---

##  Dependencies

```txt
flask
pillow
fpdf2
pdf2image
gunicorn
```

---
---

##  Roadmap

- [x] Image → PDF conversion
- [x] PDF → Image conversion
- [x] Dark / light theme toggle
- [x] Drag & drop file upload
- [ ] DOCX → PDF
- [ ] CSV → JSON / JSON → CSV
- [ ] Batch file conversion (multiple files at once)
- [ ] Conversion history with download links
- [ ] File size validation with user feedback
- [ ] Custom domain support

---

##  Contributing

Contributions are welcome! Here's how to get started:

```bash
# 1. Fork the repository on GitHub

# 2. Clone your fork
git clone https://github.com/yourusername/formatforge.git

# 3. Create a feature branch
git checkout -b feature/your-feature-name

# 4. Make your changes and commit
git add .
git commit -m "feat: add your feature"

# 5. Push and open a Pull Request
git push origin feature/your-feature-name
```

Please open an **issue** first for major changes so we can discuss the approach.

---

## 📄 License

Distributed under the **MIT License**. See [`LICENSE`](LICENSE) for more information.

---

<div align="center">
  <p>Built with ❤️ by <a href="https://github.com/techwithsuryansh">Suryansh</a></p>
  <p>
    <a href="https://github.com/techwithsuryansh/formatforge/issues">Report a Bug</a> •
    <a href="https://github.com/techwithsuryansh/formatforge/issues">Request a Feature</a>
  </p>
</div>
