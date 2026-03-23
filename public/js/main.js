/* ============================================
   FormatFlux — main.js
   Handles: theme toggle, drag/drop, form submit
   ============================================ */

(function () {
  "use strict";

  /* ══════════════════════════════════════
     THEME TOGGLE
  ══════════════════════════════════════ */
  const html      = document.documentElement;
  const themeBtn  = document.getElementById("themeBtn");
  const themeIcon = document.getElementById("themeIcon");

  const STORAGE_KEY = "formatflux-theme";

  function applyTheme(theme) {
    html.setAttribute("data-theme", theme);
    themeIcon.textContent = theme === "dark" ? "☀️" : "🌙";
    localStorage.setItem(STORAGE_KEY, theme);
  }

  // Load saved preference, else respect OS preference
  const saved = localStorage.getItem(STORAGE_KEY);
  const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
  applyTheme(saved ?? (prefersDark ? "dark" : "light"));

  themeBtn.addEventListener("click", () => {
    const current = html.getAttribute("data-theme");
    applyTheme(current === "dark" ? "light" : "dark");
  });

  /* ── DOM References ── */
  const fileInput    = document.getElementById("fileInput");
  const fileChosen   = document.getElementById("fileChosen");
  const dropZone     = document.getElementById("dropZone");
  const form         = document.getElementById("converterForm");
  const convertBtn   = document.getElementById("convertBtn");
  const statusEl     = document.getElementById("statusMsg");
  const progressWrap = document.getElementById("progressWrap");
  const progressFill = document.getElementById("progressFill");

  /* ── Helpers ── */
  function setStatus(type, icon, text) {
    statusEl.className = "status " + type + " visible";
    statusEl.innerHTML = icon + "<span>" + text + "</span>";
  }

  function clearStatus() {
    statusEl.className = "status";
    statusEl.innerHTML = "";
  }

  function showProgress() {
    progressWrap.classList.add("visible");
    // Trigger reflow then animate
    requestAnimationFrame(() => {
      requestAnimationFrame(() => { progressFill.style.width = "85%"; });
    });
  }

  function hideProgress() {
    progressFill.style.width = "100%";
    setTimeout(() => {
      progressWrap.classList.remove("visible");
      progressFill.style.width = "0%";
    }, 400);
  }

  const iconLoading = `<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>`;
  const iconSuccess = `<svg viewBox="0 0 24 24"><path d="M20 6L9 17l-5-5"/></svg>`;
  const iconError   = `<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path d="M12 8v4m0 4h.01"/></svg>`;

  /* ── File Selection ── */
  function handleFile(file) {
    if (!file) return;
    fileChosen.textContent = file.name + "  (" + formatBytes(file.size) + ")";
    fileChosen.classList.add("visible");
    convertBtn.disabled = false;
    clearStatus();
  }

  function formatBytes(bytes) {
    if (bytes < 1024)       return bytes + " B";
    if (bytes < 1048576)    return (bytes / 1024).toFixed(1) + " KB";
    return (bytes / 1048576).toFixed(1) + " MB";
  }

  fileInput.addEventListener("change", () => {
    if (fileInput.files.length) handleFile(fileInput.files[0]);
  });

  /* ── Drag & Drop ── */
  ["dragenter", "dragover"].forEach(evt =>
    dropZone.addEventListener(evt, e => {
      e.preventDefault();
      dropZone.classList.add("drag-over");
    })
  );

  ["dragleave", "dragend"].forEach(evt =>
    dropZone.addEventListener(evt, () => dropZone.classList.remove("drag-over"))
  );

  dropZone.addEventListener("drop", e => {
    e.preventDefault();
    dropZone.classList.remove("drag-over");
    const file = e.dataTransfer.files[0];
    if (file) {
      // Assign to the hidden input via DataTransfer trick
      const dt = new DataTransfer();
      dt.items.add(file);
      fileInput.files = dt.files;
      handleFile(file);
    }
  });

  /* ── Form Submit ── */
  form.addEventListener("submit", async e => {
    e.preventDefault();

    convertBtn.disabled = true;
    clearStatus();
    showProgress();
    setStatus("loading", iconLoading, "Converting your file — please wait…");

    try {
      const formData = new FormData(form);
      const response = await fetch("/convert", { method: "POST", body: formData });

      hideProgress();

      if (!response.ok) {
        const msg = await response.text();
        throw new Error(msg || "Server returned an error.");
      }

      /* ── Trigger download ── */
      const blob = await response.blob();
      const url  = URL.createObjectURL(blob);
      const anchor = document.createElement("a");
      const cd   = response.headers.get("Content-Disposition") || "";
      const name = cd.match(/filename="(.+?)"/)?.[1] ?? "converted_file";
      anchor.href     = url;
      anchor.download = name;
      document.body.appendChild(anchor);
      anchor.click();
      anchor.remove();
      URL.revokeObjectURL(url);

      setStatus("success", iconSuccess, "Done! Your file has been converted and downloaded.");

    } catch (err) {
      hideProgress();
      setStatus("error", iconError, "Error: " + err.message);
    } finally {
      convertBtn.disabled = false;
    }
  });


  
})();