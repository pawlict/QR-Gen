#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QR Gen  — prosty GUI do generowania kodów QR dla ciągów znaków (np. adresów portfeli)
Autor: pawlict
Licencja: MIT ("AS IS")

Zależności:
  pip install PyQt5 segno

Uruchomienie:
  python3 qr.py
"""

import io
import sys
from datetime import datetime

import segno
from PyQt5 import QtCore, QtGui, QtWidgets


APP_TITLE = "QR Gen — by pawlict"


class QRWalletMaker(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_TITLE)
        self.resize(900, 620)
        self._build_ui()

    # --------------------------- UI ---------------------------
    def _build_ui(self):
        tabs = QtWidgets.QTabWidget()
        tabs.setTabPosition(QtWidgets.QTabWidget.North)
        tabs.addTab(self._build_generate_tab(), "Generowanie kodu")
        tabs.addTab(self._build_info_tab(), "Info")
        self.setCentralWidget(tabs)

    def _build_generate_tab(self):
        w = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(w)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(12)

        # Wejście tekstowe
        in_box = QtWidgets.QGroupBox("Dane wejściowe")
        in_layout = QtWidgets.QGridLayout(in_box)
        self.input_edit = QtWidgets.QLineEdit()
        self.input_edit.setPlaceholderText("Wklej ciąg znaków, np. adres portfela...")
        self.input_edit.textChanged.connect(self._schedule_preview)
        in_layout.addWidget(QtWidgets.QLabel("Ciąg znaków:"), 0, 0)
        in_layout.addWidget(self.input_edit, 0, 1, 1, 3)
        layout.addWidget(in_box)

        # Opcje i przyciski
        opts_box = QtWidgets.QGroupBox("Opcje kodu QR")
        opts_layout = QtWidgets.QGridLayout(opts_box)

        self.format_combo = QtWidgets.QComboBox()
        self.format_combo.addItems(["PNG", "SVG", "PDF"])  # wspierane bezpośrednio przez segno
        self.format_combo.currentIndexChanged.connect(self._schedule_preview)

        self.ecc_combo = QtWidgets.QComboBox()
        self.ecc_combo.addItems(["L", "M", "Q", "H"])  # poziomy korekcji błędów
        self.ecc_combo.setCurrentText("M")
        self.ecc_combo.currentIndexChanged.connect(self._schedule_preview)

        self.scale_spin = QtWidgets.QSpinBox()
        self.scale_spin.setRange(1, 100)
        self.scale_spin.setValue(8)
        self.scale_spin.setToolTip("Skala pikseli modułu (1-100)")
        self.scale_spin.valueChanged.connect(self._schedule_preview)

        self.border_spin = QtWidgets.QSpinBox()
        self.border_spin.setRange(0, 50)
        self.border_spin.setValue(4)
        self.border_spin.setToolTip("Szerokość ramki w modułach (0-50)")
        self.border_spin.valueChanged.connect(self._schedule_preview)

        # Rozmieszczenie
        row = 0
        opts_layout.addWidget(QtWidgets.QLabel("Format pliku:"), row, 0)
        opts_layout.addWidget(self.format_combo, row, 1)
        opts_layout.addWidget(QtWidgets.QLabel("Poziom ECC:"), row, 2)
        opts_layout.addWidget(self.ecc_combo, row, 3)
        row += 1
        opts_layout.addWidget(QtWidgets.QLabel("Skala:"), row, 0)
        opts_layout.addWidget(self.scale_spin, row, 1)
        opts_layout.addWidget(QtWidgets.QLabel("Ramka:"), row, 2)
        opts_layout.addWidget(self.border_spin, row, 3)

        layout.addWidget(opts_box)

        # Podgląd
        preview_box = QtWidgets.QGroupBox("Podgląd")
        preview_v = QtWidgets.QVBoxLayout(preview_box)
        self.preview_label = QtWidgets.QLabel()
        self.preview_label.setAlignment(QtCore.Qt.AlignCenter)
        self.preview_label.setMinimumHeight(320)
        self.preview_label.setStyleSheet(
            "QLabel { background: #fafafa; border: 1px solid #ddd; }"
        )
        preview_v.addWidget(self.preview_label)
        layout.addWidget(preview_box, 1)

        # Przyciski akcji
        btns = QtWidgets.QHBoxLayout()
        self.preview_btn = QtWidgets.QPushButton("Generuj podgląd")
        self.preview_btn.clicked.connect(self._update_preview)
        self.save_btn = QtWidgets.QPushButton("Zapisz jako…")
        self.save_btn.clicked.connect(self._save_dialog)
        btns.addStretch(1)
        btns.addWidget(self.preview_btn)
        btns.addWidget(self.save_btn)
        layout.addLayout(btns)

        # Timer do odroczonego podglądu
        self._preview_timer = QtCore.QTimer(self)
        self._preview_timer.setInterval(400)
        self._preview_timer.setSingleShot(True)
        self._preview_timer.timeout.connect(self._update_preview)

        return w

    def _build_info_tab(self):
        w = QtWidgets.QWidget()
        v = QtWidgets.QVBoxLayout(w)
        v.setContentsMargins(20, 20, 20, 20)

        info = QtWidgets.QTextBrowser()
        info.setOpenExternalLinks(True)
        info.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        info.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        info.setStyleSheet("QTextBrowser { font-size: 14px; }")

        html = (
            """
            <h2>QR Gen</h2>
            <p><b>Prawa autorskie:</b><br>
            © 2025 pawlict - program  QR Genr objęty licencją <b> MIT </b> (do użytku komercyjnego, z zachowaniem informacji o autorze i klauzulą „AS IS”).</p>
            <pre style="white-space: pre-wrap; background: rgba(0,0,0,0.35); padding: 12px; border-radius: 8px; overflow: hidden;">
MIT License

Copyright (c) 2025 pawlict

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
            </pre>
            <p><b>AS IS</b>: Korzystasz na własną odpowiedzialność; autor nie udziela żadnych gwarancji ani nie ponosi odpowiedzialności za szkody wynikłe z używania programu.</p>
            """
        )
        info.setHtml(html)

        v.addWidget(info, 1)
        return w

    # ------------------------ Logika QR ------------------------
    def _schedule_preview(self):
        self._preview_timer.start()

    def _make_qr(self):
        data = (self.input_edit.text() or "").strip()
        if not data:
            return None
        ecc = self.ecc_combo.currentText().lower()  # 'l','m','q','h'
        try:
            qr = segno.make(data, error=ecc)
            return qr
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Błąd", f"Nie udało się utworzyć kodu QR:\n{e}")
            return None

    def _update_preview(self):
        qr = self._make_qr()
        if qr is None:
            self.preview_label.setPixmap(QtGui.QPixmap())
            self.preview_label.setText("Brak danych do podglądu")
            return

        scale = self.scale_spin.value()
        border = self.border_spin.value()

        # Wygeneruj PNG do pamięci, aby pokazać podgląd w QLabel
        try:
            buff = io.BytesIO()
            qr.save(buff, kind='png', scale=scale, border=border)
            qimg = QtGui.QImage.fromData(buff.getvalue(), 'PNG')
            if qimg.isNull():
                raise ValueError("Nie można odczytać obrazu podglądu")
            pix = QtGui.QPixmap.fromImage(qimg)
            # dopasuj do ramki podglądu z zachowaniem proporcji
            target = self.preview_label.size() - QtCore.QSize(12, 12)
            self.preview_label.setPixmap(pix.scaled(target, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
            self.preview_label.setText("")
        except Exception as e:
            self.preview_label.setPixmap(QtGui.QPixmap())
            self.preview_label.setText(f"Błąd podglądu: {e}")

    def _save_dialog(self):
        qr = self._make_qr()
        if qr is None:
            QtWidgets.QMessageBox.warning(self, "Uwaga", "Podaj najpierw ciąg znaków do zakodowania.")
            return

        fmt = self.format_combo.currentText().lower()  # png/svg/pdf
        suffix = fmt
        # Proponowana nazwa pliku
        base = self._suggest_base_name()
        filters = {
            'png': "Obraz PNG (*.png)",
            'svg': "Obraz wektorowy SVG (*.svg)",
            'pdf': "Dokument PDF (*.pdf)",
        }
        caption = "Zapisz plik"
        default_name = f"{base}.{suffix}"
        path, _ = QtWidgets.QFileDialog.getSaveFileName(self, caption, default_name, filters.get(fmt, "Wszystkie pliki (*.*)"))
        if not path:
            return

        try:
            qr.save(path, kind=fmt, scale=self.scale_spin.value(), border=self.border_spin.value())
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Błąd zapisu", f"Nie udało się zapisać pliku:\n{e}")
            return

        QtWidgets.QMessageBox.information(self, "Sukces", f"Zapisano plik:\n{path}")

    def _suggest_base_name(self) -> str:
        data = (self.input_edit.text() or "").strip()
        if not data:
            stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            return f"qr_{stamp}"
        clean = ''.join(ch for ch in data if ch.isalnum())
        if not clean:
            stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            return f"qr_{stamp}"
        return (clean[:16] + ("_" if len(clean) > 16 else ""))


def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName(APP_TITLE)
    win = QRWalletMaker()
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
