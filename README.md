# COD MW Trilogy Launcher

This is a launcher I made for my three games (Modern Warfare 1, 2, and 3) so I don't have to look for them separately every time. It features game covers, music, a splash screen with box art when launching, and even full controller support.

I'm writing this README mostly for myself as reference notes—in case I ever format my PC, lose the folder, or simply forget how all of this works. If you're seeing this because you stumbled upon the repo somehow, welcome! I hope it helps you out too haha.

> **Note:** For certain parts I had no idea how to handle (especially pywebview, controller support, and setting up `config.json` properly), I used Claude AI to lend a hand and explain how things worked. Honestly, I really recommend it—it helped me understand things that would have taken me forever to figure out on my own.

---

## Table of Contents

- [What is this exactly?](#what-is-this-exactly)
- [Features](#features)
- [How to get it running](#how-to-get-it-running)
- [How to build the .exe](#how-to-build-the-exe)
- [How to configure the games](#how-to-configure-the-games)
- [File overview](#file-overview)
- [Things I learned making this](#things-i-learned-making-this)

---

## What is this exactly?

A desktop application (a `.exe`) built with Python + pywebview. It essentially embeds a web page (HTML/CSS/JS) inside a standard Windows window, making it behave like a native app. I used this approach instead of building the interface natively in Python because I'm better at HTML/CSS and it looks much cleaner than using standard GUI libraries like Tkinter.

## Features

- Displays 3 cover arts (one per game) that enlarge when hovered or focused.
- Clicking a game shows its info along with a Play button.
- Hitting Play lets you choose between Campaign or Multiplayer (each has its own `.exe` configured separately).
- Plays the respective game's theme music when selected.
- Saves game paths in a `config.json` file so you don't have to set them every time you open it.
- Full controller support with no mouse required (D-pad to navigate, A to select, B to go back, Up to open settings).
- On launch, a splash screen displays the box art for 5 seconds before loading the actual launcher in full screen.

## How to get it running

First, you need Python installed on your PC (download it from [python.org](https://www.python.org/downloads/)). **Important:** When installing, make sure to check the box that says **"Add python.exe to PATH"**; otherwise, your PC won't recognize the `python` command in the terminal and will throw an error.

> **Watch out for the Python version:** Use **3.11 or 3.12**. Avoid the latest releases (3.13/3.14) even if they appear first on the site. I ran into an issue where a library I use (`pythonnet`) didn't support newer versions yet, causing the app to load a blank screen with missing images before crashing. It works perfectly with 3.11/3.12.

Once Python is ready, open a terminal (`cmd`) inside the project folder and run:

```bash
pip install -r requirements.txt
```

This installs pywebview (for the window interface) and PyInstaller (to build the EXE later). Then, to test that everything works before compiling:

```bash
python main.py
```

If the window opens and everything loads properly, great—you can move on to the next step.

## How to build the .exe

```bash
python -m PyInstaller --onefile --windowed --icon "icon.ico" --add-data "launcher_ui.html;." --add-data "splash.html;." --name "COD-MW-Trilogy-Launcher" main.py
```

This command generates a few new folders (`build` and `dist`) along with a `.spec` file. All of that is temporary build output from PyInstaller and doesn't need to be kept or uploaded anywhere. The only thing that matters is inside the `dist` folder: that's where your final ready-to-use `.exe` lives, and you can move it wherever you like.

> If running `pyinstaller` on its own throws the classic "not recognized as an internal or external command" error, use `python -m PyInstaller` as shown above. It does the exact same thing but guarantees execution.

## How to configure the games

When you open the launcher, click the gear icon (⚙) at the top right (or press Up + A on a controller). This lets you select the `.exe` for each game, with Single Player and Multiplayer configured separately. Paths are saved automatically in `config.json` right next to the `.exe`.

> If you format your PC or move the launcher to another machine, you'll need to reconfigure the paths since they will be different.

## File overview

| File | Description |
|---|---|
| `main.py` | Launches everything and handles core launcher logic (saving paths, executing games, etc.) |
| `splash.py` | Handles only the splash screen; separated from `main.py` to keep the code clean |
| `launcher_ui.html` | The full visual UI, with images and music embedded directly inside the file (which is why it's large) |
| `splash.html` | The splash screen graphic displayed on startup |
| `requirements.txt` | The list of required Python libraries to install all at once via `pip` |
| `icon.ico` | The application icon used when compiling the EXE |

## Things I learned making this

- **pywebview** allows rendering standard HTML/CSS/JS inside a desktop app, and you can invoke Python functions directly from JavaScript using `window.pywebview.api.function_name()`. Super handy to avoid learning a new GUI library every time.
- To make the app work seamlessly whether running compiled as a `.exe` or via `python main.py`, you need `sys.frozen` to detect execution context, as file path resolution changes between the two.
- The browser's Gamepad API (`navigator.getGamepads()`) works natively inside pywebview because it runs a full web engine under the hood. No additional Python libraries are needed for controller support.
- Launching an external program from Python and waiting for it to close without freezing the UI requires `subprocess.Popen` combined with a background thread (`threading.Thread`) calling `.wait()`.
- On Windows, if `pythonnet` isn't installed (or if using an unsupported Python version), pywebview falls back to an older render engine. That legacy fallback fails to render large embedded images properly and prevents creating new windows from background threads. Because of this, I now instantiate both windows (splash and launcher) on the main thread right at startup, toggling visibility later rather than spawning new windows mid-execution.
