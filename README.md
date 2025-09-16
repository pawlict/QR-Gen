# QR Gen

Desktop QR code generator with a simple PyQt5 GUI. Paste any string (e.g., a crypto wallet address) and export (off-line) QR codes to **PNG**, **SVG**, or **PDF**. MIT licensed (commercial use allowed with author attribution and “AS IS” clause).

> **aka**: _QR Gen — main script: `qr-gen.py`

---

## ✨ Features

- **GUI-first workflow** — paste text, tweak options, preview instantly, save.
- **Multiple formats** — export **PNG**, crisp **SVG**, or print-ready **PDF**.
- **Error correction** — choose ECC level **L / M / Q / H** for robustness.
- **Custom sizing** — control **scale** (module size) and **quiet zone** (**border**) thickness.
- **Info tab** — author credits (**pawlict**) and full **MIT** license with “AS IS” clause (2025).
- **Offline & private** — no network calls, no telemetry.
- **Cross‑platform** — Linux, Windows, macOS (Python 3.10+).

---

## 📦 Requirements

- Python **3.10+**
- `PyQt5`, `segno`

Optional (Linux):
- `libxcb-xinerama0`, `libegl1` (see Troubleshooting)

---

## Quick Start
1) System update && upgrade
```bash 
sudo apt-get update && sudo apt-get upgrade -y
```
2) System packages
```bash 
sudo apt install -y python3-segno
```

3) Get the code
```bash 
sudo apt install -y git
git clone https://github.com/pawlict/QR-Gen.git
```
3) Start program
```bash 
cd QR-Gen
python3 qr-gen.py
```
**requirements.txt**
```txt
PyQt5>=5.15
segno>=1.6
```

---

**Alternative with system packages (if available):**
```bash
sudo apt update
sudo apt install -y python3-pyqt5
# segno may or may not be packaged; if not, use venv+pip for segno
```

---

If you prefer Homebrew Python:
```bash
brew install python@3.12
```

---

## 🖥️ Usage

1. Open **QR Gen** (`qr-gen.py`).
2. Go to **Generate** tab:
   - Paste your string (e.g., wallet address, URL, Wi‑Fi pass).
   - Choose **Format**: PNG / SVG / PDF.
   - Pick **ECC** level (L/M/Q/H), **Scale**, and **Border**.
   - Click **Generate preview** → **Save as…**.
3. **Info** tab contains author info and full MIT license (with “AS IS”).

> **Tip:** Do **not** name your script like a dependency (e.g., `segno.py`) to avoid import conflicts.

---

## ⚙️ CLI Snippets (optional)

Check installs:
```bash
python -c "import segno, PyQt5; print('OK', segno.__version__)"
```

Force X11 on Wayland (Linux):
```bash
QT_QPA_PLATFORM=xcb python3 qr.py
```

---

## 🧩 Troubleshooting

- **`ModuleNotFoundError: No module named 'segno'`**  
  Activate the venv where you installed packages:
  ```bash
  source ~/.venvs/qrwallet/bin/activate   # Linux/macOS
  .\.venv\Scripts\activate               # Windows
  ```

- **Qt “platform plugin xcb” error (Linux)**  
  Install missing libs:
  ```bash
  sudo apt install -y libxcb-xinerama0 libegl1
  ```

- **PEP 668: externally-managed-environment**  
  Always use `python3 -m venv ...` and install with `pip` inside that venv.

- **No window shows / black screen**  
  Try:
  ```bash
  QT_QPA_PLATFORM=xcb python3 qr.py
  ```

---

## 🔒 Security & Privacy

- The app runs fully **offline**.
- No data leaves your machine.
- No analytics/telemetry.

---

## 🗺️ Roadmap

- Dark/Light theme toggle.
- JPG export.
- Custom header/label above the QR in PDF.
- Batch generation from a CSV.

Have ideas? Open an Issue!

---

## 🤝 Contributing

1. Fork the repo
2. Create your feature branch: `git checkout -b feature/awesome`
3. Commit changes: `git commit -m "Add awesome feature"`
4. Push branch: `git push origin feature/awesome`
5. Open a Pull Request

Please keep UI strings clear and avoid adding heavy dependencies.

---

## 🧾 License

**Copyright © 2025 pawlict**
  
This project is licensed under the **MIT License** (commercial use permitted with author attribution and **“AS IS”** clause).  
The full license text is embedded in the app’s **Info** tab and should be included in a `LICENSE` file in this repository.

---

## 🙌 Credits

Built by **pawlict**. Powered by **Python**, **PyQt5**, and **segno**.

---

## 🏷️ Suggested GitHub Topics

`python`, `qt`, `pyqt5`, `qrcode`, `qr-code`, `desktop-app`, `offline`, `wallet`, `crypto`, `svg`, `pdf`, `mit-license`
