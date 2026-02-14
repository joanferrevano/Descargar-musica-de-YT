import os
import yt_dlp

import os

CARPETA_MUSICA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "musica")
os.makedirs(CARPETA_MUSICA, exist_ok=True)


def preparar_carpeta():
    os.makedirs(CARPETA_MUSICA, exist_ok=True)

def es_url(texto):
    return texto.startswith("http://") or texto.startswith("https://")

def descargar_audio(entrada):
    if not es_url(entrada):
        entrada = f"ytsearch:{entrada}"

    opciones = {
        "format": "bestaudio/best",
        "outtmpl": f"{CARPETA_MUSICA}/%(title)s.%(ext)s",
        "noplaylist": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
    }

    try:
        with yt_dlp.YoutubeDL(opciones) as ydl:
            ydl.download([entrada])
        print("✅ Descarga completada")
    except Exception:
        print("❌ Error al descargar")
        print("👉 Revisa el enlace o el texto introducido")

if __name__ == "__main__":
    try:
        preparar_carpeta()
        print("🎵 Descargador de música (YouTube)")

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

    except Exception as e:
        print("❌ Ha ocurrido un error:")
        print(e)

    input("\nPulsa ENTER para salir...")


