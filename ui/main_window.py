from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QComboBox, QLineEdit, QCompleter
)
from PyQt5.QtCore import Qt
from services.exchanger import get_rates
from core.converter import convert

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Конвертер валют")
        self.setFixedSize(400, 300)
        self.is_dark = False  # начальная тема
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.amount_edit = QLineEdit()
        self.from_combo = QComboBox()
        self.to_combo = QComboBox()
        self.result_label = QLabel("Результат: ")
        self.convert_btn = QPushButton("Конвертировать")
        self.theme_btn = QPushButton("🌞 Тема: Светлая")

        layout.addWidget(QLabel("Сумма:"))
        layout.addWidget(self.amount_edit)

        hlayout = QHBoxLayout()
        hlayout.addWidget(QLabel("Из:"))
        hlayout.addWidget(self.from_combo)
        hlayout.addWidget(QLabel("В:"))
        hlayout.addWidget(self.to_combo)
        layout.addLayout(hlayout)

        layout.addWidget(self.convert_btn)
        layout.addWidget(self.result_label)
        layout.addWidget(self.theme_btn, alignment=Qt.AlignRight)

        self.setLayout(layout)

        self.convert_btn.clicked.connect(self.perform_conversion)
        self.theme_btn.clicked.connect(self.toggle_theme)

        self.load_rates()
        self.apply_theme()

    def load_rates(self):
        self.rates = get_rates()
        currencies = sorted(self.rates.keys())
        self.setup_searchable_combo(self.from_combo, currencies)
        self.setup_searchable_combo(self.to_combo, currencies)

    def setup_searchable_combo(self, combo, items):
        combo.setEditable(True)
        combo.setInsertPolicy(QComboBox.NoInsert)
        completer = QCompleter(items)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        combo.setCompleter(completer)
        combo.addItems(items)

    def perform_conversion(self):
        try:
            amount = float(self.amount_edit.text())
            from_curr = self.from_combo.currentText()
            to_curr = self.to_combo.currentText()
            result = convert(amount, from_curr, to_curr, self.rates)
            self.result_label.setText(f"Результат: {result:.2f}")
        except Exception:
            self.result_label.setText("Ошибка ввода")

    def toggle_theme(self):
        self.is_dark = not self.is_dark
        self.theme_btn.setText("🌙 Тема: Тёмная" if self.is_dark else "🌞 Тема: Светлая")
        self.apply_theme()

    def apply_theme(self):
        if self.is_dark:
            self.setStyleSheet("""
                QWidget { background-color: #2b2b2b; color: #f0f0f0; }
                QPushButton, QLineEdit, QComboBox { background-color: #3c3c3c; color: #f0f0f0; border: 1px solid #666; }
                QLabel { color: #f0f0f0; }
            """)
        else:
            self.setStyleSheet("")  # стандартная светлая
