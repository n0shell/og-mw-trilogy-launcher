# launcher que hice para mis 3 juegos de call of duty (modern warfare 1, 2 y 3)
# uso pywebview para meter el html dentro de una ventana normal de windows
#
# para arrancarlo: python main.py
# para hacer el exe: python -m PyInstaller --onefile --windowed --icon "icon.ico" --add-data "launcher_ui.html;." --add-data "splash.html;." --name "COD-MW-Trilogy-Launcher" main.py

import json
import os
import subprocess
import sys
import threading
import time

import webview

from splash import crear_ventana_splash, SPLASH_DURATION_SECONDS

# configuracion de la ventana, esto lo puedes cambiar si quieres
WINDOW_TITLE = "Call of Duty: Modern Warfare Trilogy"
HTML_FILE = "launcher_ui.html"
FULLSCREEN = True  # pantalla completa, si lo pones en False sale en ventana normal
WINDOW_WIDTH = 1000  # esto solo se usa si FULLSCREEN esta en False
WINDOW_HEIGHT = 650

CONFIG_FILE = "config.json"  # aqui se guardan las rutas de los juegos que configuras


def app_directory():
    # esto es para que funcione tanto si lo ejecutas con python como si ya esta
    # compilado en exe, porque sys.executable cambia según el caso
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


def load_config():
    # carga el config.json si existe, si no pues diccionario vacio y ya
    path = os.path.join(app_directory(), CONFIG_FILE)
    if os.path.isfile(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def save_config(config):
    path = os.path.join(app_directory(), CONFIG_FILE)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)


class Api:
    # esta clase es el puente entre el html y python. las funciones de aqui
    # se llaman desde el javascript con window.pywebview.api.nombre_funcion()

    def __init__(self):
        self.config = load_config()
        self.window = None  # se rellena luego en main()

    def get_saved_paths(self):
        # el html llama a esto para saber que rutas ya estan guardadas
        return self.config

    def choose_executable(self, game_id, mode):
        # abre el explorador de archivos de windows para elegir el exe del juego
        # mode puede ser "singleplayer" o "multiplayer"
        result = self.window.create_file_dialog(
            webview.FileDialog.OPEN,
            file_types=("Archivos ejecutables (*.exe)", "Todos los archivos (*.*)"),
        )
        if not result:
            return None

        path = result[0]
        self.config.setdefault(game_id, {})[mode] = path
        save_config(self.config)
        return path

    def launch_game(self, game_id, mode):
        # esto lanza el juego de verdad. oculta el launcher mientras juegas
        # y cuando cierras el juego se vuelve a abrir solo
        path = self.config.get(game_id, {}).get(mode)
        if not path or not os.path.isfile(path):
            return {"ok": False, "error": "not_configured"}

        try:
            process = subprocess.Popen(path, cwd=os.path.dirname(path))
        except Exception as exc:
            return {"ok": False, "error": str(exc)}

        # esto lo hago en otro hilo para que no se quede pillado esperando
        threading.Thread(target=self._hide_wait_and_reopen, args=(process,), daemon=True).start()
        return {"ok": True}

    def _hide_wait_and_reopen(self, process):
        time.sleep(1.0)  # le doy un segundo para que el juego arranque bien
        self.window.hide()

        process.wait()  # aqui se queda parado hasta que cierres el juego

        self.window.show()
        self.window.evaluate_js("window.onJuegoCerrado()")


def crear_ventana_launcher():
    # esto crea la ventana del launcher, pero empieza oculta (hidden=True)
    # hasta que se acabe la pantalla de carga. La creo aqui, en el hilo
    # principal, junto con la del splash, porque crear ventanas nuevas
    # desde otro hilo da error con algunos motores de windows
    api = Api()
    window = webview.create_window(
        title=WINDOW_TITLE,
        url=HTML_FILE,
        width=WINDOW_WIDTH,
        height=WINDOW_HEIGHT,
        resizable=True,
        fullscreen=FULLSCREEN,
        js_api=api,
        hidden=True,
    )
    api.window = window
    return window


def main():
    # creo las DOS ventanas aqui, en el hilo principal, antes de arrancar
    # el bucle de webview. la del launcher empieza oculta (hidden=True)
    splash_window = crear_ventana_splash()
    launcher_window = crear_ventana_launcher()

    def cuando_termine_la_carga():
        # espero a que la ventana del splash haya cargado de verdad la
        # imagen antes de empezar a contar los 5 segundos. si no, en un
        # pc lento el motor tarda en arrancar y se ve en blanco todo el rato
        splash_window.events.loaded.wait()
        time.sleep(SPLASH_DURATION_SECONDS)
        splash_window.destroy()
        launcher_window.show()

    # gui="edgechromium" para forzar el motor moderno de Edge en vez del
    # motor viejo de windows (que no carga bien imagenes grandes en base64
    # y encima da error al intentar abrir una ventana desde otro hilo)
    webview.start(cuando_termine_la_carga, gui="edgechromium")


if __name__ == "__main__":
    main()
