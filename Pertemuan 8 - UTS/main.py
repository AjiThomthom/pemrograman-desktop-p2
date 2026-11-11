import sys
import datetime
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QHeaderView, QMessageBox, QGroupBox, QGridLayout, QDialog, QTextEdit,
    QCompleter
)
from PySide6.QtCore import Qt, QRegularExpression, QStringListModel
from PySide6.QtGui import QFont, QRegularExpressionValidator, QIntValidator

class AplikasiKasir(QMainWindow):
    def __init__(self):
        super().__init__()
        self.is_dark_mode = True
        self.riwayat_transaksi = []
        
        # Database Master Harga Barang (Default Preset)
        self.master_harga = {
            "Sabun Mandi": 15000,
            "Minyak Goreng": 40000,
            "Beras 5kg": 75000,
            "Gula Pasir": 17000,
            "Kopi Saset": 3000
        }
        
        self.subtotal = 0.0
        self.diskon_persen = 0
        self.nominal_diskon = 0.0
        self.total_akhir = 0.0
        self.kembalian = 0.0
        
        self.setWindowTitle("Aplikasi Kasir Mini")
        self.resize(940, 820)
        self.setMinimumSize(900, 780)
        
        # --- DEFINISI PALET TEMA (QSS) ---
        self.theme_dark = """
            QMainWindow, QDialog, QMessageBox { background-color: #121212; color: #FFFFFF; }
            QGroupBox {
                color: #E0E0E0; font-size: 14px; font-weight: bold;
                border: 1px solid #333333; border-radius: 8px;
                margin-top: 15px; padding: 15px 10px 10px 10px; background-color: #1E1E1E;
            }
            QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top left; padding: 0 10px; color: #4DA8DA; }
            QLabel { color: #CCCCCC; font-size: 13px; }
            QLineEdit, QTextEdit {
                background-color: #2D2D2D; color: #FFFFFF; border: 1px solid #444444;
                border-radius: 5px; padding: 8px 12px; font-size: 13px;
            }
            QLineEdit:focus, QTextEdit:focus { border: 1px solid #4DA8DA; background-color: #333333; }
            QLineEdit:read-only { background-color: #222222; color: #888888; border: 1px solid #333333; }
            QTableWidget {
                background-color: #252525; color: #FFFFFF; gridline-color: #383838;
                border: 1px solid #333333; border-radius: 5px;
            }
            QHeaderView::section {
                background-color: #1A1A1A; color: #4DA8DA; padding: 8px; font-weight: bold; border: none; border-right: 1px solid #383838;
            }
            QTableWidget::item:selected { background-color: #205B7A; color: white; }
            QMessageBox QPushButton {
                background-color: #2980B9; color: white; border-radius: 4px; padding: 6px 15px; min-width: 65px;
            }
        """
        
        self.theme_light = """
            QMainWindow, QDialog, QMessageBox { background-color: #F8F9FA; color: #2C3E50; }
            QGroupBox {
                color: #2C3E50; font-size: 14px; font-weight: bold;
                border: 1px solid #DCDFE6; border-radius: 8px;
                margin-top: 15px; padding: 15px 10px 10px 10px; background-color: #FFFFFF;
            }
            QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top left; padding: 0 10px; color: #2980B9; }
            QLabel { color: #333333; font-size: 13px; }
            QLineEdit, QTextEdit {
                background-color: #F2F4F8; color: #2C3E50; border: 1px solid #DCDFE6;
                border-radius: 5px; padding: 8px 12px; font-size: 13px;
            }
            QLineEdit:focus, QTextEdit:focus { border: 1px solid #2980B9; background-color: #FFFFFF; }
            QLineEdit:read-only { background-color: #EAEDED; color: #7F8C8D; border: 1px solid #DCDFE6; }
            QTableWidget {
                background-color: #FFFFFF; color: #2C3E50; gridline-color: #E4E7ED;
                border: 1px solid #DCDFE6; border-radius: 5px;
            }
            QHeaderView::section {
                background-color: #EDF2F7; color: #2980B9; padding: 8px; font-weight: bold; border: none; border-right: 1px solid #E4E7ED;
            }
            QTableWidget::item:selected { background-color: #3498DB; color: white; }
            QMessageBox QPushButton {
                background-color: #2980B9; color: white; border-radius: 4px; padding: 6px 15px; min-width: 65px;
            }
        """

        # Setup Layout Utama
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(25, 20, 25, 25)
        main_layout.setSpacing(15)
        
        # --- 1. HEADER & TOMBOL (Urutan Kanan ke Kiri: Setting -> Tema -> Riwayat) ---
        layout_header = QHBoxLayout()
        
        lbl_header = QLabel("Aplikasi Kasir Mini dengan PySide6")
        lbl_header.setFont(QFont("Segoe UI", 22, QFont.Weight.Bold))
        
        self.btn_riwayat = QPushButton("📜 Riwayat")
        self.btn_riwayat.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_riwayat.setFixedSize(110, 35)
        self.btn_riwayat.clicked.connect(self.tampilkan_riwayat)
        
        self.btn_theme = QPushButton("🌙 Mode Gelap")
        self.btn_theme.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_theme.setFixedSize(130, 35)
        self.btn_theme.clicked.connect(self.toggle_theme)
        
        self.btn_setting = QPushButton("⚙️ Setting Harga")
        self.btn_setting.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_setting.setFixedSize(135, 35)
        self.btn_setting.clicked.connect(self.buka_setting_harga)
        
        layout_header.addWidget(lbl_header)
        layout_header.addStretch()
        layout_header.addWidget(self.btn_riwayat)
        layout_header.addWidget(self.btn_theme)
        layout_header.addWidget(self.btn_setting)
        main_layout.addLayout(layout_header)

        # --- 2. FORM INPUT DATA BARANG ---
        group_input = QGroupBox("Input Data Barang")
        layout_input = QGridLayout(group_input)
        layout_input.setContentsMargins(20, 20, 20, 20)
        layout_input.setHorizontalSpacing(20)
        layout_input.setVerticalSpacing(15)
        
        regex_huruf = QRegularExpression("^[a-zA-Z0-9\\s]*$")
        regex_angka = QRegularExpression("^[0-9]*$")
        
        layout_input.addWidget(QLabel("Nama Barang:"), 0, 0)
        self.entry_nama = QLineEdit()
        self.entry_nama.setPlaceholderText("Masukkan Nama Barang...")
        self.entry_nama.setValidator(QRegularExpressionValidator(regex_huruf, self))
        self.entry_nama.textChanged.connect(self.cek_auto_harga)
        layout_input.addWidget(self.entry_nama, 0, 1)
        
        # Auto-complete setup
        self.completer_model = QStringListModel()
        self.completer = QCompleter(self.completer_model, self)
        self.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.entry_nama.setCompleter(self.completer)
        self.update_completer_data()

        layout_input.addWidget(QLabel("Harga Satuan (Rp):"), 0, 2)
        self.entry_harga = QLineEdit()
        self.entry_harga.setPlaceholderText("Masukkan Harga Satuan...")
        self.entry_harga.setValidator(QRegularExpressionValidator(regex_angka, self))
        layout_input.addWidget(self.entry_harga, 0, 3)
        
        layout_input.addWidget(QLabel("Jumlah:"), 1, 0)
        self.entry_jumlah = QLineEdit()
        self.entry_jumlah.setPlaceholderText("Masukkan Jumlah...")
        self.entry_jumlah.setValidator(QIntValidator(1, 999999, self))
        layout_input.addWidget(self.entry_jumlah, 1, 1)
        
        self.btn_tambah = QPushButton("Tambah Barang")
        self.btn_tambah.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_tambah.setFixedHeight(35)
        self.btn_tambah.setStyleSheet("""
            QPushButton { background-color: #2980B9; color: white; font-weight: bold; border-radius: 5px; }
            QPushButton:hover { background-color: #3498DB; }
        """)
        self.btn_tambah.clicked.connect(self.tambah_barang)
        layout_input.addWidget(self.btn_tambah, 1, 2, 1, 2)
        
        layout_input.setColumnStretch(1, 2)
        layout_input.setColumnStretch(3, 2)
        main_layout.addWidget(group_input)

        # --- 3. AREA DAFTAR TRANSAKSI ---
        group_tabel = QGroupBox("Daftar Transaksi")
        layout_tabel = QVBoxLayout(group_tabel)
        layout_tabel.setContentsMargins(15, 20, 15, 15)
        layout_tabel.setSpacing(10)
        
        self.tabel_transaksi = QTableWidget(0, 4)
        self.tabel_transaksi.setHorizontalHeaderLabels(["Nama Barang", "Harga Satuan", "Jumlah", "Total Harga"])
        self.tabel_transaksi.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabel_transaksi.verticalHeader().setVisible(False)
        self.tabel_transaksi.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tabel_transaksi.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout_tabel.addWidget(self.tabel_transaksi)
        
        self.btn_hapus = QPushButton("Hapus Barang Terpilih")
        self.btn_hapus.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_hapus.setFixedSize(170, 32)
        self.btn_hapus.setStyleSheet("""
            QPushButton { background-color: #C0392B; color: white; border-radius: 4px; font-weight: bold;}
            QPushButton:hover { background-color: #E74C3C; }
        """)
        self.btn_hapus.clicked.connect(self.hapus_barang)
        layout_tabel.addWidget(self.btn_hapus, alignment=Qt.AlignmentFlag.AlignRight)
        
        main_layout.addWidget(group_tabel)

        # --- 4. RINGKASAN PEMBAYARAN & KALKULATOR TUNAI ---
        group_ringkasan = QGroupBox("Ringkasan Pembayaran & Pembayaran Tunai")
        layout_ringkasan = QHBoxLayout(group_ringkasan)
        layout_ringkasan.setContentsMargins(20, 15, 20, 15)
        
        grid_bayar = QGridLayout()
        grid_bayar.setVerticalSpacing(10)
        grid_bayar.setHorizontalSpacing(15)
        
        grid_bayar.addWidget(QLabel("Uang Diterima (Rp):"), 0, 0)
        self.entry_bayar = QLineEdit()
        self.entry_bayar.setPlaceholderText("Masukkan nominal tunai...")
        self.entry_bayar.setValidator(QRegularExpressionValidator(regex_angka, self))
        self.entry_bayar.textChanged.connect(self.hitung_kembalian)
        grid_bayar.addWidget(self.entry_bayar, 0, 1)
        
        grid_bayar.addWidget(QLabel("Kembalian:"), 1, 0)
        self.lbl_kembalian = QLabel("Rp 0")
        self.lbl_kembalian.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        self.lbl_kembalian.setStyleSheet("color: #3498DB;")
        grid_bayar.addWidget(self.lbl_kembalian, 1, 1)
        
        layout_ringkasan.addLayout(grid_bayar, stretch=1)
        
        divider = QLabel()
        divider.setFixedWidth(1)
        divider.setStyleSheet("background-color: #444444;")
        layout_ringkasan.addWidget(divider)

        grid_total = QGridLayout()
        grid_total.setVerticalSpacing(8)
        grid_total.setHorizontalSpacing(15)
        
        lbl_title_subtotal = QLabel("Subtotal:")
        lbl_title_subtotal.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        self.lbl_subtotal = QLabel("Rp 0")
        self.lbl_subtotal.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        self.lbl_subtotal.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        grid_total.addWidget(lbl_title_subtotal, 0, 0)
        grid_total.addWidget(self.lbl_subtotal, 0, 1)
        
        lbl_title_diskon = QLabel("Diskon:")
        lbl_title_diskon.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        self.lbl_diskon = QLabel("0% (Rp 0)")
        self.lbl_diskon.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        self.lbl_diskon.setStyleSheet("color: #F39C12;")
        self.lbl_diskon.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        grid_total.addWidget(lbl_title_diskon, 1, 0)
        grid_total.addWidget(self.lbl_diskon, 1, 1)
        
        lbl_title_total = QLabel("Total Pembayaran:")
        lbl_title_total.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        self.lbl_total_bayar = QLabel("Rp 0")
        self.lbl_total_bayar.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        self.lbl_total_bayar.setStyleSheet("color: #2ECC71;")
        self.lbl_total_bayar.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        grid_total.addWidget(lbl_title_total, 2, 0)
        grid_total.addWidget(self.lbl_total_bayar, 2, 1)
        
        grid_total.setColumnMinimumWidth(0, 140)
        grid_total.setColumnMinimumWidth(1, 160)
        
        layout_ringkasan.addLayout(grid_total, stretch=1)
        main_layout.addWidget(group_ringkasan)

        # --- 5. TOMBOL AKSI BAWAH ---
        layout_aksi = QHBoxLayout()
        layout_aksi.setSpacing(12)
        
        self.btn_hitung = QPushButton("Hitung Total")
        self.btn_hitung.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_hitung.setFixedHeight(45)
        self.btn_hitung.setStyleSheet("""
            QPushButton { background-color: #2980B9; color: white; font-size: 14px; font-weight: bold; border-radius: 6px; }
            QPushButton:hover { background-color: #3498DB; }
        """)
        self.btn_hitung.clicked.connect(self.hitung_total)
        layout_aksi.addWidget(self.btn_hitung, stretch=1)
        
        self.btn_selesai = QPushButton("Selesaikan Transaksi")
        self.btn_selesai.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_selesai.setFixedHeight(45)
        self.btn_selesai.setStyleSheet("""
            QPushButton { background-color: #27AE60; color: white; font-size: 14px; font-weight: bold; border-radius: 6px; }
            QPushButton:hover { background-color: #2ECC71; }
        """)
        self.btn_selesai.clicked.connect(self.simpan_transaksi)
        layout_aksi.addWidget(self.btn_selesai, stretch=1)
        
        self.btn_reset = QPushButton("Reset Form")
        self.btn_reset.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_reset.setFixedHeight(45)
        self.btn_reset.setStyleSheet("""
            QPushButton { background-color: #7F8C8D; color: white; font-size: 14px; font-weight: bold; border-radius: 6px; }
            QPushButton:hover { background-color: #95A5A6; }
        """)
        self.btn_reset.clicked.connect(self.konfirmasi_reset)
        layout_aksi.addWidget(self.btn_reset, stretch=1)
        
        self.btn_keluar = QPushButton("Keluar")
        self.btn_keluar.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_keluar.setFixedHeight(45)
        self.btn_keluar.setStyleSheet("""
            QPushButton { background-color: transparent; border: 2px solid #C0392B; color: #E74C3C; font-size: 14px; font-weight: bold; border-radius: 6px; }
            QPushButton:hover { background-color: #C0392B; color: white; }
        """)
        self.btn_keluar.clicked.connect(self.konfirmasi_keluar)
        layout_aksi.addWidget(self.btn_keluar, stretch=1)
        
        main_layout.addLayout(layout_aksi)

        self.apply_theme()

    # --- AUTO HARGA LOGIC ---
    def update_completer_data(self):
        nama_list = list(self.master_harga.keys())
        self.completer_model.setStringList(nama_list)

    def cek_auto_harga(self, text):
        nama_input = text.strip()
        # Mencari match persis tanpa membedakan huruf besar-kecil
        match_key = next((k for k in self.master_harga.keys() if k.lower() == nama_input.lower()), None)
        
        if match_key:
            harga_satuan = self.master_harga[match_key]
            self.entry_harga.setText(str(harga_satuan))
            self.entry_harga.setReadOnly(True) # Kunci harga agar tidak bisa diedit sembarangan
        else:
            self.entry_harga.setReadOnly(False) # Lepas kunci jika nama kustom

    def buka_setting_harga(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("⚙️ Setting Harga Master Produk")
        dialog.resize(500, 420)
        dialog_layout = QVBoxLayout(dialog)
        
        # Form Tambah/Edit Master
        group_setting = QGroupBox("Tambah / Update Barang Master")
        grid_setting = QGridLayout(group_setting)
        
        entry_set_nama = QLineEdit()
        entry_set_nama.setPlaceholderText("Nama Barang...")
        entry_set_harga = QLineEdit()
        entry_set_harga.setPlaceholderText("Harga Satuan...")
        regex_angka = QRegularExpression("^[0-9]*$")
        entry_set_harga.setValidator(QRegularExpressionValidator(regex_angka, self))
        
        grid_setting.addWidget(QLabel("Nama:"), 0, 0)
        grid_setting.addWidget(entry_set_nama, 0, 1)
        grid_setting.addWidget(QLabel("Harga:"), 1, 0)
        grid_setting.addWidget(entry_set_harga, 1, 1)
        
        btn_simpan_master = QPushButton("Simpan Ke Master")
        btn_simpan_master.setStyleSheet("background-color: #27AE60; color: white; font-weight: bold; padding: 6px;")
        grid_setting.addWidget(btn_simpan_master, 2, 0, 1, 2)
        
        dialog_layout.addWidget(group_setting)
        
        # Tabel Daftar Master Produk
        tabel_master = QTableWidget(0, 2)
        tabel_master.setHorizontalHeaderLabels(["Nama Barang Master", "Harga Satuan"])
        tabel_master.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        def refresh_tabel_master():
            tabel_master.setRowCount(0)
            for nama, harga in self.master_harga.items():
                r = tabel_master.rowCount()
                tabel_master.insertRow(r)
                item_n = QTableWidgetItem(nama)
                item_h = QTableWidgetItem(f"Rp {harga:,.0f}")
                item_n.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                item_h.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                tabel_master.setItem(r, 0, item_n)
                tabel_master.setItem(r, 1, item_h)
        
        refresh_tabel_master()
        dialog_layout.addWidget(tabel_master)
        
        def aksi_simpan_master():
            n = entry_set_nama.text().strip()
            h = entry_set_harga.text().strip()
            if not n or not h or float(h) <= 0:
                QMessageBox.warning(dialog, "Input Salah", "Nama dan harga master harus valid!")
                return
            self.master_harga[n] = int(h)
            self.update_completer_data()
            refresh_tabel_master()
            entry_set_nama.clear()
            entry_set_harga.clear()
            QMessageBox.information(dialog, "Sukses", f"Barang '{n}' berhasil disimpan di master!")
            
        btn_simpan_master.clicked.connect(aksi_simpan_master)
        
        btn_tutup = QPushButton("Selesai")
        btn_tutup.setFixedHeight(35)
        btn_tutup.clicked.connect(dialog.close)
        dialog_layout.addWidget(btn_tutup)
        
        dialog.exec()

    def buat_item_tengah(self, teks):
        item = QTableWidgetItem(teks)
        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        return item

    def toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        self.apply_theme()

    def apply_theme(self):
        if self.is_dark_mode:
            self.setStyleSheet(self.theme_dark)
            self.btn_theme.setText("🌙 Mode Gelap")
            self.btn_theme.setStyleSheet("QPushButton { background-color: #2C2C2C; color: #F1C40F; border: 1px solid #3D3D3D; font-weight: bold; border-radius: 5px; } QPushButton:hover { background-color: #3D3D3D; }")
            self.btn_riwayat.setStyleSheet("QPushButton { background-color: #2C2C2C; color: #FFFFFF; border: 1px solid #3D3D3D; font-weight: bold; border-radius: 5px; } QPushButton:hover { background-color: #3D3D3D; }")
            self.btn_setting.setStyleSheet("QPushButton { background-color: #2C2C2C; color: #4DA8DA; border: 1px solid #3D3D3D; font-weight: bold; border-radius: 5px; } QPushButton:hover { background-color: #3D3D3D; }")
            lbl_header_color = "#FFFFFF"
        else:
            self.setStyleSheet(self.theme_light)
            self.btn_theme.setText("☀️ Mode Terang")
            self.btn_theme.setStyleSheet("QPushButton { background-color: #EAEDED; color: #D35400; border: 1px solid #DCDFE6; font-weight: bold; border-radius: 5px; } QPushButton:hover { background-color: #D5DBDB; }")
            self.btn_riwayat.setStyleSheet("QPushButton { background-color: #EAEDED; color: #2C3E50; border: 1px solid #DCDFE6; font-weight: bold; border-radius: 5px; } QPushButton:hover { background-color: #D5DBDB; }")
            self.btn_setting.setStyleSheet("QPushButton { background-color: #EAEDED; color: #2980B9; border: 1px solid #DCDFE6; font-weight: bold; border-radius: 5px; } QPushButton:hover { background-color: #D5DBDB; }")
            lbl_header_color = "#2C3E50"
            
        self.centralWidget().layout().itemAt(0).layout().itemAt(0).widget().setStyleSheet(f"color: {lbl_header_color};")

    def validasi_input(self, nama, harga, jumlah):
        if not nama.strip():
            QMessageBox.warning(self, "Peringatan", "Nama barang tidak boleh kosong!")
            return False
        try:
            if float(harga) <= 0:
                QMessageBox.warning(self, "Peringatan", "Harga satuan harus lebih besar dari 0!")
                return False
        except ValueError:
            QMessageBox.warning(self, "Peringatan", "Harga satuan harus berupa angka!")
            return False
        try:
            if int(jumlah) <= 0:
                QMessageBox.warning(self, "Peringatan", "Jumlah harus bilangan bulat lebih dari 0!")
                return False
        except ValueError:
            QMessageBox.warning(self, "Peringatan", "Jumlah harus berupa bilangan bulat!")
            return False
        return True

    def tambah_barang(self):
        nama = self.entry_nama.text()
        harga = self.entry_harga.text()
        jumlah = self.entry_jumlah.text()

        if self.validasi_input(nama, harga, jumlah):
            harga_satuan = float(harga)
            jumlah_barang = int(jumlah)
            total_per_barang = harga_satuan * jumlah_barang

            row_count = self.tabel_transaksi.rowCount()
            self.tabel_transaksi.insertRow(row_count)
            
            self.tabel_transaksi.setItem(row_count, 0, self.buat_item_tengah(nama))
            self.tabel_transaksi.setItem(row_count, 1, self.buat_item_tengah(f"Rp {harga_satuan:,.0f}"))
            self.tabel_transaksi.setItem(row_count, 2, self.buat_item_tengah(str(jumlah_barang)))
            self.tabel_transaksi.setItem(row_count, 3, self.buat_item_tengah(f"Rp {total_per_barang:,.0f}"))

            self.entry_nama.clear()
            self.entry_harga.clear()
            self.entry_jumlah.clear()
            self.entry_harga.setReadOnly(False)
            self.entry_nama.setFocus()
            
            self.hitung_total()

    def hapus_barang(self):
        selected_row = self.tabel_transaksi.currentRow()
        if selected_row >= 0:
            jawaban = QMessageBox.question(self, "Konfirmasi Hapus", "Yakin ingin menghapus barang terpilih?", 
                                           QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if jawaban == QMessageBox.StandardButton.Yes:
                self.tabel_transaksi.removeRow(selected_row)
                self.hitung_total()
        else:
            QMessageBox.information(self, "Info", "Pilih baris pada tabel yang ingin dihapus terlebih dahulu.")

    def hitung_total(self):
        subtotal = 0.0
        for row in range(self.tabel_transaksi.rowCount()):
            item_total = self.tabel_transaksi.item(row, 3).text()
            total_clean = float(item_total.replace("Rp ", "").replace(",", ""))
            subtotal += total_clean

        diskon_persen = 0
        if subtotal < 100000:
            diskon_persen = 0
        elif 100000 <= subtotal < 200000:
            diskon_persen = 5
        elif subtotal >= 200000:
            diskon_persen = 10

        self.subtotal = subtotal
        self.diskon_persen = diskon_persen
        self.nominal_diskon = subtotal * (diskon_persen / 100)
        self.total_akhir = subtotal - self.nominal_diskon

        self.lbl_subtotal.setText(f"Rp {subtotal:,.0f}")
        self.lbl_diskon.setText(f"{diskon_persen}% (Rp {self.nominal_diskon:,.0f})")
        self.lbl_total_bayar.setText(f"Rp {self.total_akhir:,.0f}")
        
        self.hitung_kembalian()

    def hitung_kembalian(self):
        teks_bayar = self.entry_bayar.text()
        if teks_bayar and self.total_akhir > 0:
            try:
                bayar = float(teks_bayar)
                self.kembalian = bayar - self.total_akhir
                if self.kembalian >= 0:
                    self.lbl_kembalian.setText(f"Rp {self.kembalian:,.0f}")
                    self.lbl_kembalian.setStyleSheet("color: #2ECC71; font-weight: bold;")
                else:
                    self.lbl_kembalian.setText(f"Kurang Rp {abs(self.kembalian):,.0f}")
                    self.lbl_kembalian.setStyleSheet("color: #E74C3C; font-weight: bold;")
            except ValueError:
                self.lbl_kembalian.setText("Rp 0")
        else:
            self.lbl_kembalian.setText("Rp 0")
            self.lbl_kembalian.setStyleSheet("color: #3498DB; font-weight: bold;")

    def simpan_transaksi(self):
        if self.tabel_transaksi.rowCount() == 0:
            QMessageBox.warning(self, "Peringatan", "Daftar belanja masih kosong!")
            return
            
        teks_bayar = self.entry_bayar.text()
        if not teks_bayar or float(teks_bayar) < self.total_akhir:
            QMessageBox.warning(self, "Pembayaran Kurang", "Nominal uang diterima masih kurang dari Total Pembayaran!")
            return

        konfirmasi = QMessageBox.question(
            self, "Selesaikan Transaksi", 
            f"Total Pembayaran: Rp {self.total_akhir:,.0f}\nUang Diterima: Rp {float(teks_bayar):,.0f}\nKembalian: Rp {self.kembalian:,.0f}\n\nLanjutkan transaksi?", 
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if konfirmasi == QMessageBox.StandardButton.Yes:
            waktu = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            
            daftar_item = []
            for row in range(self.tabel_transaksi.rowCount()):
                nama = self.tabel_transaksi.item(row, 0).text()
                harga = self.tabel_transaksi.item(row, 1).text()
                jumlah = self.tabel_transaksi.item(row, 2).text()
                total = self.tabel_transaksi.item(row, 3).text()
                daftar_item.append({
                    "nama": nama,
                    "harga": harga,
                    "jumlah": jumlah,
                    "total": total
                })

            data_transaksi = {
                "waktu": waktu,
                "items": daftar_item,
                "subtotal": f"Rp {self.subtotal:,.0f}",
                "diskon": f"{self.diskon_persen}% (Rp {self.nominal_diskon:,.0f})",
                "total_bayar": f"Rp {self.total_akhir:,.0f}",
                "uang_diterima": f"Rp {float(teks_bayar):,.0f}",
                "kembalian": f"Rp {self.kembalian:,.0f}"
            }
            
            self.riwayat_transaksi.append(data_transaksi)
            QMessageBox.information(self, "Sukses", "Transaksi berhasil diselesaikan dan disimpan ke riwayat!")
            self.reset_form()

    def tampilkan_riwayat(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Riwayat Transaksi Pembelian")
        dialog.resize(580, 480)
        dialog_layout = QVBoxLayout(dialog)
        
        teks_box = QTextEdit()
        teks_box.setReadOnly(True)
        teks_box.setFont(QFont("Consolas", 10))
        
        if len(self.riwayat_transaksi) == 0:
            teks_box.setText("Belum ada transaksi yang diselesaikan hari ini.")
        else:
            struk_text = ""
            for i, tx in enumerate(self.riwayat_transaksi, 1):
                struk_text += f"==========================================================\n"
                struk_text += f"               STRUK PEMBELIAN KASIR #{i}\n"
                struk_text += f" Waktu: {tx['waktu']}\n"
                struk_text += f"----------------------------------------------------------\n"
                struk_text += f" {'Nama Barang':<20} | {'Harga':<10} | {'Qty':<4} | {'Total':<10}\n"
                struk_text += f"----------------------------------------------------------\n"
                
                for item in tx['items']:
                    struk_text += f" {item['nama']:<20} | {item['harga']:<10} | {item['jumlah']:<4} | {item['total']:<10}\n"
                
                struk_text += f"----------------------------------------------------------\n"
                struk_text += f" Subtotal         : {tx['subtotal']}\n"
                struk_text += f" Diskon           : {tx['diskon']}\n"
                struk_text += f" Total Pembayaran : {tx['total_bayar']}\n"
                struk_text += f" Uang Diterima    : {tx['uang_diterima']}\n"
                struk_text += f" Kembalian        : {tx['kembalian']}\n"
                struk_text += f"==========================================================\n\n"
                
            teks_box.setText(struk_text)
            
        dialog_layout.addWidget(teks_box)
        btn_tutup = QPushButton("Tutup")
        btn_tutup.setFixedHeight(35)
        btn_tutup.clicked.connect(dialog.close)
        dialog_layout.addWidget(btn_tutup)
        
        dialog.exec()

    def konfirmasi_reset(self):
        jawaban = QMessageBox.question(self, "Konfirmasi Reset", "Yakin ingin mereset seluruh data belanja saat ini?", 
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if jawaban == QMessageBox.StandardButton.Yes:
            self.reset_form()
            
    def konfirmasi_keluar(self):
        jawaban = QMessageBox.question(self, "Konfirmasi Keluar", "Yakin ingin keluar dari aplikasi kasir?", 
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if jawaban == QMessageBox.StandardButton.Yes:
            self.close()

    def reset_form(self):
        self.tabel_transaksi.setRowCount(0)
        self.entry_bayar.clear()
        self.lbl_subtotal.setText("Rp 0")
        self.lbl_diskon.setText("0% (Rp 0)")
        self.lbl_total_bayar.setText("Rp 0")
        self.lbl_kembalian.setText("Rp 0")
        self.entry_harga.setReadOnly(False)
        self.subtotal = 0.0
        self.diskon_persen = 0
        self.nominal_diskon = 0.0
        self.total_akhir = 0.0
        self.kembalian = 0.0

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AplikasiKasir()
    window.show()
    sys.exit(app.exec())