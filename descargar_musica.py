import os
import yt_dlp
from yt_dlp.utils import DownloadError

DIRECTORIO_SCRIPT = os.path.dirname(os.path.abspath(__file__))
CARPETA_MUSICA = os.path.join(DIRECTORIO_SCRIPT, "musica")
ARCHIVO_COOKIES = os.path.join(DIRECTORIO_SCRIPT, "cookies.txt")


def preparar_carpeta():
    os.makedirs(CARPETA_MUSICA, exist_ok=True)


def es_url(texto):
    return texto.startswith("http://") or texto.startswith("https://")


def opciones_descarga():
    opciones = {
        "format": "bestaudio/best",
        "outtmpl": os.path.join(CARPETA_MUSICA, "%(title)s.%(ext)s"),
        "noplaylist": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        # Pausas para no saturar a YouTube (evita el error 429)
        "sleep_interval_requests": 1,
        "sleep_interval": 3,
        "max_sleep_interval": 8,
        # Reintentos ante fallos de red
        "retries": 5,
        "fragment_retries": 5,
        "extractor_retries": 3,
    }

    if os.path.isfile(ARCHIVO_COOKIES):
        opciones["cookiefile"] = ARCHIVO_COOKIES

    return opciones


def explicar_error(mensaje):
    m = mensaje.lower()
    if "sign in to confirm" in m or "not a bot" in m:
        print("🤖 YouTube pide verificar que no eres un bot.")
        if os.path.isfile(ARCHIVO_COOKIES):
            print("👉 Tus cookies.txt pueden estar caducadas: expórtalas de nuevo.")
        else:
            print("👉 Pon un archivo cookies.txt junto al script (exportado con")
            print("   la extensión 'Get cookies.txt LOCALLY' con sesión iniciada).")
    elif "429" in m or "too many requests" in m:
        print("⏳ YouTube ha limitado tu IP por demasiadas peticiones.")
        print("👉 Espera un rato (minutos u horas) y vuelve a intentarlo.")
    elif "ffmpeg" in m or "ffprobe" in m:
        print("🔧 Falta FFmpeg o no está en el PATH.")
        print("👉 Instálalo para poder convertir a mp3.")
    elif "video unavailable" in m or "private video" in m:
        print("🚫 El vídeo no está disponible o es privado.")
    elif "unsupported url" in m:
        print("🔗 El enlace no es válido.")
    else:
        print("👉 Revisa el enlace o el texto introducido.")
        print("   Si persiste, actualiza yt-dlp: pip install -U \"yt-dlp[default]\"")


def descargar_audio(entrada):
    if not es_url(entrada):
        entrada = f"ytsearch1:{entrada}"

    try:
        with yt_dlp.YoutubeDL(opciones_descarga()) as ydl:
            ydl.download([entrada])
        print("✅ Descarga completada")
    except DownloadError as e:
        print("❌ Error al descargar")
        explicar_error(str(e))
    except Exception as e:
        print("❌ Error inesperado:")
        print(e)


if __name__ == "__main__":
    try:
        preparar_carpeta()
        print("🎵 Descargador de música (YouTube)")

        if os.path.isfile(ARCHIVO_COOKIES):
            print("🍪 Usando cookies.txt")
        else:
            print("⚠️  No se ha encontrado cookies.txt: YouTube podría bloquear las descargas")

        while True:
            print("\nPega un enlace, escribe un título o 'salir' para terminar:")
            entrada = input("> ").strip()

            if entrada.lower() == "salir":
                print("👋 Cerrando programa...")
                break

            if entrada:
                descargar_audio(entrada)
            else:
                print("❌ No se ha introducido nada")

    except KeyboardInterrupt:
        print("\n👋 Cerrando programa...")
    except Exception as e:
        print("❌ Ha ocurrido un error:")
        print(e)

    input("\nPulsa ENTER para salir...")