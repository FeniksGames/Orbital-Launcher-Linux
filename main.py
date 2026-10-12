#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import stat
import shutil
from pathlib import Path

from PySide6.QtCore import Qt, QProcess, QProcessEnvironment
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QStackedWidget,
    QScrollArea,
    QFrame,
    QMessageBox,
    QComboBox,
    QCheckBox,
    QSizePolicy,
)


APP_NAME = "ORBITAL APP MANAGER"
PROGRAMS_DIR = Path.home() / "mine"
JAVA_PATH = Path("/usr/lib/jvm/liberica-jdk-8-full/bin/java")

BACKGROUND = "#050811"
CARD_BACKGROUND = "#090F1C"
BLUE = "#3B82F6"
PURPLE = "#7C3AED"
GREEN = "#39D98A"
TEXT = "#F1F5F9"
MUTED = "#94A3B8"
BORDER = "#1E293B"


STYLESHEET = f"""
QWidget {{
    background-color: {BACKGROUND};
    color: {TEXT};
    font-family: "Inter", "Noto Sans", sans-serif;
    font-size: 14px;
}}

QLabel {{
    background: transparent;
}}

QLabel#title {{
    font-size: 30px;
    font-weight: 800;
    color: {TEXT};
}}

QLabel#subtitle {{
    font-size: 13px;
    color: {MUTED};
}}

QLabel#sectionTitle {{
    font-size: 22px;
    font-weight: 700;
}}

QLabel#programName {{
    font-size: 15px;
    font-weight: 600;
    color: {TEXT};
}}

QLabel#empty {{
    font-size: 15px;
    color: {MUTED};
    padding: 24px;
}}

QFrame#programCard {{
    background-color: {CARD_BACKGROUND};
    border: 1px solid {BORDER};
    border-radius: 14px;
}}

QPushButton {{
    background-color: {CARD_BACKGROUND};
    color: {TEXT};
    border: 1px solid {BORDER};
    border-radius: 10px;
    padding: 11px 18px;
    font-weight: 600;
}}

QPushButton:hover {{
    border-color: {BLUE};
    background-color: #101B30;
}}

QPushButton:pressed {{
    background-color: #172554;
}}

QPushButton#primary {{
    background-color: {BLUE};
    border: 1px solid {BLUE};
    color: white;
}}

QPushButton#primary:hover {{
    background-color: #2563EB;
}}

QPushButton#launch {{
    background-color: #10291F;
    color: {GREEN};
    border: 1px solid #20523A;
    min-width: 100px;
}}

QPushButton#launch:hover {{
    background-color: #163B2A;
    border-color: {GREEN};
}}

QPushButton#back {{
    background-color: transparent;
    border: 1px solid {BORDER};
}}

QComboBox {{
    background-color: {CARD_BACKGROUND};
    border: 1px solid {BORDER};
    border-radius: 8px;
    padding: 8px 12px;
    min-width: 180px;
}}

QComboBox QAbstractItemView {{
    background-color: {CARD_BACKGROUND};
    color: {TEXT};
    selection-background-color: {BLUE};
}}

QCheckBox {{
    spacing: 8px;
    color: {MUTED};
}}

QScrollArea {{
    border: none;
    background: transparent;
}}

QScrollBar:vertical {{
    background: {BACKGROUND};
    width: 9px;
    margin: 0;
}}

QScrollBar::handle:vertical {{
    background: #26364D;
    border-radius: 4px;
    min-height: 25px;
}}

QScrollBar::handle:vertical:hover {{
    background: {BLUE};
}}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {{
    height: 0;
}}

QStatusBar {{
    background-color: {BACKGROUND};
    color: {MUTED};
    border-top: 1px solid {BORDER};
}}
"""


class OrbitalAppManager(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(APP_NAME)
        self.setMinimumSize(700, 520)
        self.resize(1000, 720)

        # QProcess instances are retained while their processes are running.
        self.processes = []

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.home_page = self.create_home_page()
        self.programs_page = self.create_list_page("app")
        self.java_page = self.create_list_page("jar")

        # Exactly three main pages.
        self.stack.addWidget(self.home_page)
        self.stack.addWidget(self.programs_page)
        self.stack.addWidget(self.java_page)

        self.statusBar().showMessage(
            f"Папка программ: {PROGRAMS_DIR}", 6000
        )

    def create_home_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 35, 30, 30)
        layout.setSpacing(18)

        layout.addStretch(1)

        logo = QLabel("◉ ORBITAL")
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo.setStyleSheet(
            f"font-size: 15px; font-weight: 800; color: {BLUE};"
            " letter-spacing: 4px;"
        )
        layout.addWidget(logo)

        title = QLabel(APP_NAME)
        title.setObjectName("title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        subtitle = QLabel(
            "Центр запуска приложений Linux · X11 / Xorg"
        )
        subtitle.setObjectName("subtitle")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)

        layout.addSpacing(30)

        app_button = QPushButton("Программы .AppImage / .run")
        app_button.setObjectName("primary")
        app_button.setMinimumHeight(68)
        app_button.setMaximumWidth(470)
        app_button.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )
        app_button.clicked.connect(
            lambda: self.open_list_page("app")
        )

        java_button = QPushButton("Java-программы .jar")
        java_button.setMinimumHeight(68)
        java_button.setMaximumWidth(470)
        java_button.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )
        java_button.clicked.connect(
            lambda: self.open_list_page("jar")
        )

        for button in (app_button, java_button):
            layout.addWidget(button, alignment=Qt.AlignmentFlag.AlignHCenter)

        folder_label = QLabel(f"Каталог программ: {PROGRAMS_DIR}")
        folder_label.setObjectName("subtitle")
        folder_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        folder_label.setWordWrap(True)
        layout.addSpacing(18)
        layout.addWidget(folder_label)

        layout.addStretch(1)

        footer = QLabel("ORBITAL PROJECT  ·  LINUX APP MANAGER")
        footer.setObjectName("subtitle")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(footer)

        return page

    def create_list_page(self, kind):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(22, 20, 22, 16)
        layout.setSpacing(14)

        top_row = QHBoxLayout()

        back_button = QPushButton("← Назад")
        back_button.setObjectName("back")
        back_button.clicked.connect(
            lambda: self.stack.setCurrentWidget(self.home_page)
        )
        top_row.addWidget(back_button)

        top_row.addStretch()

        refresh_button = QPushButton("↻ Обновить список")
        refresh_button.clicked.connect(
            lambda k=kind: self.scan_programs(k)
        )
        top_row.addWidget(refresh_button)

        layout.addLayout(top_row)

        if kind == "app":
            heading_text = "Программы AppImage / RUN"
            description_text = "Исполняемые приложения из ~/mine/"
        else:
            heading_text = "Java-программы"
            description_text = "JAR-файлы из ~/mine/ · Java 8"

        heading = QLabel(heading_text)
        heading.setObjectName("sectionTitle")
        layout.addWidget(heading)

        description = QLabel(description_text)
        description.setObjectName("subtitle")
        layout.addWidget(description)

        settings = QHBoxLayout()
        settings.addWidget(QLabel("Режим графики:"))

        mode_combo = QComboBox()
        mode_combo.addItem("X11 / Xorg (рекомендуется)", "x11")
        mode_combo.addItem("Обычный запуск", "normal")
        settings.addWidget(mode_combo)
        settings.addStretch()

        electron_checkbox = QCheckBox(
            "Electron: --ozone-platform=x11"
        )
        electron_checkbox.setToolTip(
            "Включайте только для Electron-приложений, "
            "которым нужен этот параметр."
        )
        electron_checkbox.setVisible(kind == "app")
        settings.addWidget(electron_checkbox)

        layout.addLayout(settings)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        container = QWidget()
        cards_layout = QVBoxLayout(container)
        cards_layout.setContentsMargins(2, 2, 8, 2)
        cards_layout.setSpacing(10)
        cards_layout.addStretch()

        scroll.setWidget(container)
        layout.addWidget(scroll, 1)

        # Store page-specific widgets without introducing more pages.
        page.kind = kind
        page.cards_layout = cards_layout
        page.scroll = scroll
        page.mode_combo = mode_combo
        page.electron_checkbox = electron_checkbox

        return page

    def open_list_page(self, kind):
        page = (
            self.programs_page if kind == "app"
            else self.java_page
        )

        self.stack.setCurrentWidget(page)
        self.scan_programs(kind)

    def ensure_program_directory(self):
        if PROGRAMS_DIR.is_dir():
            return True

        if PROGRAMS_DIR.exists():
            QMessageBox.warning(
                self,
                "Ошибка каталога",
                f"Путь существует, но не является папкой:\n"
                f"{PROGRAMS_DIR}",
            )
            return False

        answer = QMessageBox.question(
            self,
            "Папка не найдена",
            f"Папка программ отсутствует:\n\n{PROGRAMS_DIR}\n\n"
            "Создать её сейчас?",
            QMessageBox.StandardButton.Yes
            | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.Yes,
        )

        if answer != QMessageBox.StandardButton.Yes:
            return False

        try:
            PROGRAMS_DIR.mkdir(parents=True, exist_ok=True)
            return True
        except OSError as error:
            QMessageBox.critical(
                self,
                "Ошибка создания папки",
                f"Не удалось создать папку:\n{PROGRAMS_DIR}\n\n"
                f"Причина: {error}",
            )
            return False

    def scan_programs(self, kind):
        page = (
            self.programs_page if kind == "app"
            else self.java_page
        )

        # Remove previous cards and the previous stretch.
        while page.cards_layout.count():
            item = page.cards_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        if not self.ensure_program_directory():
            self.show_empty_message(
                page, "Нет доступного каталога программ."
            )
            return

        if kind == "app":
            extensions = {".appimage", ".run"}
        else:
            extensions = {".jar"}

        try:
            files = [
                entry
                for entry in PROGRAMS_DIR.iterdir()
                if entry.is_file()
                and entry.suffix.lower() in extensions
            ]
            files.sort(key=lambda path: path.name.casefold())
        except OSError as error:
            self.show_empty_message(page, "Не удалось прочитать каталог.")
            QMessageBox.warning(
                self,
                "Ошибка сканирования",
                f"Не удалось прочитать папку:\n{PROGRAMS_DIR}\n\n"
                f"Причина: {error}",
            )
            return

        if not files:
            self.show_empty_message(
                page,
                "Программы не найдены. "
                "Поместите файлы в папку ~/mine/.",
            )
            return

        for file_path in files:
            self.add_program_card(page, file_path)

        page.cards_layout.addStretch()
        self.statusBar().showMessage(
            f"Найдено программ: {len(files)}", 5000
        )

    def show_empty_message(self, page, message):
        label = QLabel(message)
        label.setObjectName("empty")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setWordWrap(True)
        page.cards_layout.addWidget(label)
        page.cards_layout.addStretch()

    def add_program_card(self, page, file_path):
        card = QFrame()
        card.setObjectName("programCard")
        card.setMinimumHeight(78)

        row = QHBoxLayout(card)
        row.setContentsMargins(18, 12, 14, 12)
        row.setSpacing(15)

        icon_label = QLabel("◈")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setFixedWidth(30)
        icon_label.setStyleSheet(
            f"color: {PURPLE}; font-size: 24px; font-weight: bold;"
        )
        row.addWidget(icon_label)

        info = QVBoxLayout()
        info.setSpacing(4)

        name = QLabel(file_path.stem)
        name.setObjectName("programName")
        name.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )
        name.setToolTip(str(file_path))
        info.addWidget(name)

        file_type = QLabel(file_path.suffix)
        file_type.setObjectName("subtitle")
        info.addWidget(file_type)

        row.addLayout(info, 1)

        launch_button = QPushButton("Запустить  ↗")
        launch_button.setObjectName("launch")
        launch_button.setMinimumHeight(42)
        launch_button.clicked.connect(
            lambda checked=False, p=file_path, pg=page:
                self.launch_program(p, pg)
        )
        row.addWidget(launch_button)

        page.cards_layout.addWidget(card)

    def launch_program(self, file_path, page):
        # A stale card must never cause an invalid launch.
        if not file_path.exists() or not file_path.is_file():
            QMessageBox.warning(
                self,
                "Файл не найден",
                f"Файл был удалён или недоступен:\n{file_path}\n\n"
                "Обновите список программ.",
            )
            return

        extension = file_path.suffix.lower()

        if extension == ".jar":
            self.launch_jar(file_path, page)
        elif extension in {".appimage", ".run"}:
            self.launch_executable(file_path, page)
        else:
            QMessageBox.warning(
                self,
                "Неподдерживаемый формат",
                f"Формат {extension} не поддерживается.",
            )

    def launch_executable(self, file_path, page):
        if not os.access(file_path, os.X_OK):
            answer = QMessageBox.question(
                self,
                "Нет права на исполнение",
                f"Файл не имеет права на исполнение:\n\n"
                f"{file_path}\n\n"
                "Разрешить запуск для текущего пользователя?\n"
                "Будет добавлено право на исполнение владельцу файла.",
                QMessageBox.StandardButton.Yes
                | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No,
            )

            if answer != QMessageBox.StandardButton.Yes:
                return

            try:
                current_mode = file_path.stat().st_mode
                file_path.chmod(current_mode | stat.S_IXUSR)
            except OSError as error:
                QMessageBox.critical(
                    self,
                    "Не удалось изменить права",
                    f"Не удалось разрешить исполнение:\n{file_path}\n\n"
                    f"Причина: {error}",
                )
                return

            if not os.access(file_path, os.X_OK):
                QMessageBox.warning(
                    self,
                    "Ошибка доступа",
                    "Файл по-прежнему недоступен для исполнения.",
                )
                return

        if not file_path.exists():
            QMessageBox.warning(
                self, "Файл не найден", str(file_path)
            )
            return

        program = str(file_path)
        arguments = []

        if page.electron_checkbox.isChecked():
            arguments.append("--ozone-platform=x11")

        self.start_process(
            program,
            arguments,
            page,
            f"Запуск: {file_path.name}",
        )

    def launch_jar(self, file_path, page):
        if not JAVA_PATH.is_file():
            QMessageBox.critical(
                self,
                "Java 8 не найдена",
                "Не удалось найти Java по указанному пути:\n\n"
                f"{JAVA_PATH}\n\n"
                "Проверьте установку Liberica JDK 8 "
                "и расположение исполняемого файла java.",
            )
            return

        if not os.access(JAVA_PATH, os.X_OK):
            QMessageBox.critical(
                self,
                "Java недоступна",
                f"Файл Java не имеет права на исполнение:\n{JAVA_PATH}",
            )
            return

        arguments = ["-jar", str(file_path)]

        self.start_process(
            str(JAVA_PATH),
            arguments,
            page,
            f"Запуск Java-программы: {file_path.name}",
        )

    def start_process(self, program, arguments, page, description):
        # QProcess starts the application asynchronously.
        # The GUI thread never waits for the child process to finish.
        process = QProcess(self)

        environment = QProcessEnvironment.systemEnvironment()

        if page.mode_combo.currentData() == "x11":
            environment.insert("GDK_BACKEND", "x11")

        process.setProcessEnvironment(environment)
        process.setProgram(program)
        process.setArguments(arguments)

        self.processes.append(process)

        process.started.connect(
            lambda p=process, message=description:
                self.on_process_started(p, message)
        )
        process.errorOccurred.connect(
            lambda error, p=process:
                self.on_process_error(p, error)
        )
        process.finished.connect(
            lambda exit_code, exit_status, p=process:
                self.on_process_finished(p, exit_code, exit_status)
        )

        self.statusBar().showMessage(
            f"Отправка команды запуска: {description}", 4000
        )

        try:
            process.start()
        except Exception as error:
            self.remove_process(process)
            QMessageBox.critical(
                self,
                "Ошибка запуска",
                f"Не удалось запустить программу:\n{program}\n\n"
                f"Причина: {error}",
            )

    def on_process_started(self, process, description):
        self.statusBar().showMessage(
            f"Процесс создан: {description}", 5000
        )

    def on_process_error(self, process, error):
        # FailedToStart is emitted when the operating system could
        # not create the child process.
        if error == QProcess.ProcessError.FailedToStart:
            details = process.errorString()
            QMessageBox.critical(
                self,
                "Не удалось запустить программу",
                f"Операционная система не смогла создать процесс.\n\n"
                f"{details}",
            )
            self.remove_process(process)
        else:
            self.statusBar().showMessage(
                f"Ошибка процесса: {process.errorString()}", 7000
            )

    def on_process_finished(self, process, exit_code, exit_status):
        if exit_status == QProcess.ExitStatus.CrashExit:
            self.statusBar().showMessage(
                "Программа завершилась аварийно.", 7000
            )
        elif exit_code != 0:
            self.statusBar().showMessage(
                f"Программа завершилась с кодом {exit_code}.", 7000
            )
        else:
            self.statusBar().showMessage(
                "Программа завершилась.", 4000
            )

        self.remove_process(process)

    def remove_process(self, process):
        if process in self.processes:
            self.processes.remove(process)
        process.deleteLater()


def main():
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setStyle("Fusion")
    app.setStyleSheet(STYLESHEET)

    font = QFont("Noto Sans", 10)
    app.setFont(font)

    window = OrbitalAppManager()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()