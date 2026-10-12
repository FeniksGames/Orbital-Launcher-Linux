# 🛰️ ORBITAL Launcher Linux

**Русский** | [English](#english)

ORBITAL Launcher Linux — графическая программа для запуска приложений и игровых лаунчеров в форматах `.AppImage`, `.run` и `.jar`.

## ✨ Возможности

- 🖥️ Графический интерфейс на Python и PySide6.
- 📦 Запуск файлов `.AppImage`, `.run` и `.jar`.
- ☕ Поддержка нескольких версий Java.
- 📁 Единая папка `~/mine` для запускаемых файлов.
- 🐧 Для Linux.

## 📋 Требования

Для запуска готовой сборки обычно не требуется устанавливать Python и библиотеки проекта.

Для запуска из исходного кода потребуются:

- Linux на базе Arch Linux (например, CachyOS).
- Python 3, `pip` и `venv`.
- Java 8, 17, 21 или 25 — в зависимости от требований запускаемого `.jar`.

## 📥 Установка

### Вариант 1 — Скачать готовую версию (рекомендуется)

Вы можете скачать уже скомпилированную версию ORBITAL Launcher Linux со страницы релизов GitHub:

**[⬇️ Скачать ORBITAL Launcher Linux — Releases](https://github.com/FeniksGames/Orbital-Launcher-Linux/releases)**

1. Откройте страницу Releases.
2. Выберите последнюю версию.
3. Скачайте готовый файл лаунчера из раздела Assets.
4. Запустите скачанный файл согласно его формату.
5. Создайте папку `mine` в домашнем каталоге, если она ещё не существует:

```bash
mkdir -p ~/mine
```

6. Поместите файлы `.AppImage`, `.run` и `.jar`, которые хотите запускать через ORBITAL Launcher, в папку `~/mine`.

**Важно:** папка `~/mine` необходима даже при использовании готовой сборки. В ней хранятся файлы, которые нужно запускать через лаунчер. Python и зависимости проекта для запуска готовой сборки обычно устанавливать не требуется.

### Вариант 2 — Запуск из исходного кода

Если вы хотите запустить проект из исходного кода или самостоятельно собрать приложение, выполните следующие шаги.

#### 1. Клонирование репозитория

```bash
git clone https://github.com/FeniksGames/Orbital-Launcher-Linux.git
cd Orbital-Launcher-Linux
```

#### 2. Создание виртуального окружения

```bash
python -m venv .venv
source .venv/bin/activate
```

#### 3. Установка зависимостей Python

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

#### 4. Создание папки для файлов

```bash
mkdir -p ~/mine
```

Теперь помещайте все файлы, запускаемые через лаунчер, в `~/mine`.

## ☕ Установка Java

Для CachyOS и Arch Linux можно установить следующие версии Liberica JDK:

```bash
yay -S liberica-jdk-8-full-bin
yay -S liberica-jdk-17-full-bin
yay -S liberica-jdk-21-full-bin
yay -S liberica-jdk-25-full-bin
```

Не всем программам нужны все версии Java. Выбирайте версию, совместимую с запускаемым `.jar`.

## 📁 Папка `mine`

Путь к папке:

```text
~/mine/
├── PentacraftBootstrap-x86_64.AppImage
├── installer.run
└── launcher.jar
```

Названия приведены для примера.

**В папку `~/mine` необходимо помещать все файлы, которые вы хотите запускать через ORBITAL Launcher:**

- `.AppImage` — приложения AppImage.
- `.run` — исполняемые установщики и программы.
- `.jar` — Java-программы и игровые лаунчеры.

При необходимости предоставьте права на исполнение файлов:

```bash
chmod +x ~/mine/*.AppImage
chmod +x ~/mine/*.run
```

Если файлов одного из этих типов нет, соответствующая команда может вывести предупреждение — это нормально.

## 🚀 Запуск из исходного кода

Из каталога проекта активируйте виртуальное окружение и запустите программу:

```bash
source .venv/bin/activate
python main.py
```

## 📦 Сборка приложения

Для создания отдельного исполняемого файла:

```bash
python -m PyInstaller \
  --clean \
  --noconfirm \
  --onefile \
  --windowed \
  --name "ORBITAL-LAUNCHER" \
  main.py
```

Готовый файл появится в `dist/ORBITAL-LAUNCHER`.

## 🛠️ Зависимости Python

Все зависимости Python и их версии перечислены в [`requirements.txt`](requirements.txt).

Для запуска из исходного кода установите зависимости из этого файла. `PyInstaller` нужен для сборки приложения, а не для обычного запуска через Python.

## 🔗 Ссылки

- **GitHub:** https://github.com/FeniksGames/Orbital-Launcher-Linux
- **Releases:** https://github.com/FeniksGames/Orbital-Launcher-Linux/releases
- **Discord:** https://discord.gg/bSxaQgQvyq

---

<a id="english"></a>

# 🛰️ ORBITAL Launcher Linux — English

ORBITAL Launcher Linux is a graphical application for launching applications and game launchers in `.AppImage`, `.run`, and `.jar` formats.

## ✨ Features

- 🖥️ Graphical interface built with Python and PySide6.
- 📦 Launch `.AppImage`, `.run`, and `.jar` files.
- ☕ Support for multiple Java versions.
- 📁 A dedicated `~/mine` directory for launchable files.
- 🐧 Designed for Linux.

## 📋 Requirements

A precompiled release usually does not require Python or the project's Python dependencies to be installed.

To run from source, you will need:

- An Arch-based Linux distribution, such as CachyOS.
- Python 3, `pip`, and `venv`.
- Java 8, 17, 21, or 25, depending on the requirements of the `.jar` file.

## 📥 Installation

### Option 1 — Download a precompiled release (recommended)

You can download a precompiled version of ORBITAL Launcher Linux from GitHub Releases:

**[⬇️ Download ORBITAL Launcher Linux — Releases](https://github.com/FeniksGames/Orbital-Launcher-Linux/releases)**

1. Open the Releases page.
2. Select the latest release.
3. Download the launcher executable from the Assets section.
4. Run the downloaded file according to its format.
5. Create the `mine` directory in your home directory if it does not already exist:

```bash
mkdir -p ~/mine
```

6. Place the `.AppImage`, `.run`, and `.jar` files you want to launch through ORBITAL Launcher in `~/mine`.

**Important:** the `~/mine` directory is required even when using a precompiled release. It stores the files you want to launch. Python and the project's dependencies usually do not need to be installed to run a precompiled build.

### Option 2 — Run from source

If you want to run the project from source or build it yourself, follow these steps.

#### 1. Clone the repository

```bash
git clone https://github.com/FeniksGames/Orbital-Launcher-Linux.git
cd Orbital-Launcher-Linux
```

#### 2. Create a Python virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

#### 3. Install Python dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

#### 4. Create the files directory

```bash
mkdir -p ~/mine
```

Place all files you want to launch through the launcher in `~/mine`.

## ☕ Installing Java

On CachyOS and Arch Linux, you can install these Liberica JDK versions:

```bash
yay -S liberica-jdk-8-full-bin
yay -S liberica-jdk-17-full-bin
yay -S liberica-jdk-21-full-bin
yay -S liberica-jdk-25-full-bin
```

Not every application requires all Java versions. Use the version compatible with the `.jar` file you want to run.

## 📁 The `mine` directory

The directory is located at:

```text
~/mine/
├── PentacraftBootstrap-x86_64.AppImage
├── installer.run
└── launcher.jar
```

The filenames above are examples only.

**Place all files you want to launch through ORBITAL Launcher in `~/mine`:**

- `.AppImage` — AppImage applications.
- `.run` — executable installers and applications.
- `.jar` — Java applications and game launchers.

If necessary, make `.AppImage` and `.run` files executable:

```bash
chmod +x ~/mine/*.AppImage
chmod +x ~/mine/*.run
```

If files of either type are missing, the corresponding command may print a warning. This is normal.

## 🚀 Launch from source

From the project directory, activate the virtual environment and start the launcher:

```bash
source .venv/bin/activate
python main.py
```

## 📦 Build the application

To create a standalone executable:

```bash
python -m PyInstaller \
  --clean \
  --noconfirm \
  --onefile \
  --windowed \
  --name "ORBITAL-LAUNCHER" \
  main.py
```

The resulting executable will be located at `dist/ORBITAL-LAUNCHER`.

## 🛠️ Python dependencies

All Python dependencies and their versions are listed in [`requirements.txt`](requirements.txt).

Install them from that file to run the application from source. `PyInstaller` is required for building the executable, not for normal Python execution.

## 🔗 Links

- **GitHub:** https://github.com/FeniksGames/Orbital-Launcher-Linux
- **Releases:** https://github.com/FeniksGames/Orbital-Launcher-Linux/releases
- **Discord:** https://discord.gg/bSxaQgQvyq

---

**ORBITAL Launcher Linux**  
*One launcher. Multiple formats. Your Linux.* 🛰️
