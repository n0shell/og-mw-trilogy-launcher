# COD MW Trilogy Launcher

Esto es un launcher que me hice para mis 3 juegos (Modern Warfare 1, 2 y 3), para no tener que buscarlos por separado cada vez. Tiene portadas, música, pantalla de carga con la carátula al abrirlo, y hasta soporte para mando.

Este README lo escribo sobre todo para mí mismo, tipo notas, por si en algún momento formateo el pc, pierdo la carpeta, o me da un despiste y se me olvida cómo iba todo esto. Si estás viendo esto porque te ha llegado el repo de alguna forma, bienvenido, espero que te sirva también jaja.

> **Aviso random:** en algunas partes que no tenía ni idea de cómo hacer (sobre todo lo de pywebview, lo del mando y meter el config.json bien) usé la IA de Claude para que me echara una mano y me explicara cómo iba. La recomiendo bastante, la verdad, me ayudó a entender cosas que si no me hubiera costado la vida buscar por mi cuenta.

---

## Índice

- [Qué es esto exactamente](#qué-es-esto-exactamente)
- [Qué hace](#qué-hace)
- [Por si se me olvida cómo ponerlo a funcionar otra vez](#por-si-se-me-olvida-cómo-ponerlo-a-funcionar-otra-vez)
- [Cómo hacer el .exe otra vez](#cómo-hacer-el-exe-otra-vez)
- [Cómo configurar los juegos la primera vez](#cómo-configurar-los-juegos-la-primera-vez-o-si-reinstalas)
- [Los archivos que hay](#los-archivos-que-hay-y-para-qué-sirve-cada-uno)
- [Cosas que aprendí haciendo esto](#cosas-que-aprendí-haciendo-esto-por-si-me-sirve-para-otro-proyecto)

---

## Qué es esto exactamente

Un programa de escritorio (un `.exe`) hecho con Python + pywebview, que básicamente mete una página web (html/css/js) dentro de una ventana normal de Windows, como si fuera una app nativa. Uso esto en vez de hacer la interfaz directamente en Python porque se me da mejor y queda más bonito con html/css que con las librerías típicas tipo tkinter.

## Qué hace

- Salen 3 portadas, una por juego, y al pasar el cursor o entrar se ve más grande
- Le das a uno y te enseña info del juego + un botón de jugar
- Al jugar te deja elegir entre campaña o multijugador (cada uno tiene su propio `.exe` configurado aparte)
- Suena la música de cada juego cuando lo seleccionas
- Guarda las rutas de los juegos en un archivo `config.json`, así no hay que ponerlas cada vez que lo abres
- Se puede jugar con mando entero, sin ratón (dpad para moverte, A para aceptar, B para volver, arriba para ir a los ajustes)
- Al abrir el programa sale la carátula 5 segundos como si fuera pantalla de carga, y luego ya entra al launcher de verdad, a pantalla completa

## Por si se me olvida cómo ponerlo a funcionar otra vez

Primero necesitas Python instalado en el pc (lo bajas de [python.org](https://www.python.org/downloads/)). Importante: cuando lo instales, tienes que marcar la casilla que dice **"Add python.exe to PATH"**, si no luego el pc no reconoce el comando `python` en la terminal y da error.

> **Ojo con la versión de Python:** usa la **3.11 o la 3.12**, no cojas la última (3.13/3.14) aunque salga primero en la web. Me pasó que con una versión demasiado nueva, una librería que uso (`pythonnet`) no tenía soporte todavía, y el programa se veía en blanco sin la foto y luego petaba. Con 3.11/3.12 va perfecto.

Una vez tengas Python, abre una terminal (cmd) dentro de la carpeta del proyecto y pon:

```bash
pip install -r requirements.txt
```

Eso instala pywebview (para la ventana) y pyinstaller (para hacer el exe luego). Después, para probar que todo va bien antes de compilar nada:

```bash
python main.py
```

Si se abre la ventana y todo carga bien, genial, ya puedes seguir al siguiente paso.

## Cómo hacer el .exe otra vez

```bash
python -m PyInstaller --onefile --windowed --icon "icon.ico" --add-data "launcher_ui.html;." --add-data "splash.html;." --name "COD-MW-Trilogy-Launcher" main.py
```

Esto crea un par de carpetas nuevas (`build` y `dist`) y un archivo `.spec`, todo eso es basura que genera pyinstaller, no hace falta guardarlo ni subirlo a ningún lado. Lo único que importa es lo que hay dentro de `dist`, ahí está el `.exe` final ya listo para usar, se puede mover a donde sea.

> Si `pyinstaller` solo (sin más) te da el típico error de "no se reconoce como un comando interno o externo", usa `python -m PyInstaller` como arriba, es lo mismo pero así siempre funciona.

## Cómo configurar los juegos la primera vez (o si reinstalas)

Al abrir el launcher, arriba a la derecha hay un icono de tuerca (⚙). Le das clic (o con el mando, arriba + A) y te deja elegir el `.exe` de cada juego, tanto el modo un jugador como el multijugador van por separado. Eso se guarda solo en `config.json`, al lado del `.exe`.

> Si formateas el pc o mueves el launcher a otro pc, tienes que volver a configurar las rutas porque ahí serán distintas.

## Los archivos que hay y para qué sirve cada uno

| Archivo | Para qué sirve |
|---|---|
| `main.py` | El que arranca todo, tiene la lógica del launcher (guardar rutas, abrir los juegos, etc) |
| `splash.py` | Solo la pantalla de carga de la carátula, lo separé del main para no tenerlo todo mezclado |
| `launcher_ui.html` | Toda la interfaz visual, con las imágenes y la música ya metidas dentro del propio archivo (por eso pesa tanto) |
| `splash.html` | La carátula que se ve al abrir el programa |
| `requirements.txt` | La lista de librerías que hacen falta, para instalarlas todas de golpe con pip |
| `icon.ico` | El icono del programa, se usa al compilar el .exe |

## Cosas que aprendí haciendo esto (por si me sirve para otro proyecto)

- pywebview deja meter html/css/js normal dentro de una app de escritorio, y desde el javascript puedes llamar funciones de Python con `window.pywebview.api.nombre_de_la_funcion()`. Muy útil para no tener que aprender una librería nueva de interfaces cada vez.
- Para que la app funcione igual estando compilada en `.exe` que corriendo con `python main.py`, hay que usar `sys.frozen` para saber si está compilado o no, porque las rutas de los archivos cambian.
- La Gamepad API del navegador (`navigator.getGamepads()`) va también dentro de pywebview porque por debajo usa un motor de navegador de verdad. No hace falta ninguna librería aparte para que funcione un mando.
- Para lanzar otro programa desde Python y esperar a que se cierre sin que se quede todo pillado, hay que usar `subprocess.Popen` + un hilo aparte (`threading.Thread`) que llama a `.wait()`.
- Con pywebview en Windows, si no tienes `pythonnet` instalado (o usas una versión de Python demasiado nueva que aún no lo soporta), se usa un motor de renderizado antiguo de respaldo que no carga bien imágenes grandes y además no deja crear ventanas nuevas desde un hilo en segundo plano. Por eso ahora creo las dos ventanas (splash y launcher) en el hilo principal desde el principio, y solo la oculto/muestro después, en vez de crearla nueva a medias.
