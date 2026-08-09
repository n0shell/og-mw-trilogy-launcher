# esto solo se encarga de la pantalla de carga (la caratula) que sale
# cuando abres el programa, antes de que se abra el launcher de verdad
#
# lo separe del main.py para no tener todo mezclado en un archivo

import ctypes

import webview

SPLASH_HTML = "splash.html"
SPLASH_WIDTH = 507
SPLASH_HEIGHT = 680
SPLASH_DURATION_SECONDS = 5


def calcular_posicion_centrada():
    # pywebview no centra la ventana solo, hay que decirle exactamente en
    # que pixel ponerla. esto mira el tamaño de la pantalla de windows y
    # calcula donde tiene que ir la esquina de la ventana para que quede
    # justo en medio
    try:
        ancho_pantalla = ctypes.windll.user32.GetSystemMetrics(0)
        alto_pantalla = ctypes.windll.user32.GetSystemMetrics(1)
        x = (ancho_pantalla - SPLASH_WIDTH) // 2
        y = (alto_pantalla - SPLASH_HEIGHT) // 2
        return x, y
    except Exception:
        # si algo falla (por ejemplo, estas en otro sistema que no sea
        # windows) pues que la ponga donde quiera, tampoco pasa nada
        return None, None


def crear_ventana_splash():
    # ventana sin marco, tamaño normal (no pantalla completa), centrada en
    # medio de la pantalla de verdad
    x, y = calcular_posicion_centrada()
    return webview.create_window(
        title="",
        url=SPLASH_HTML,
        width=SPLASH_WIDTH,
        height=SPLASH_HEIGHT,
        x=x,
        y=y,
        frameless=True,
        resizable=False,
        on_top=True,
    )