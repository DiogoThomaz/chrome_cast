import time
import pychromecast
import random
from pychromecast.controllers import youtube

# URL do vídeo do YouTube que você deseja compartilhar
video_urls = ["KmVmoHg9zuU", "sfZn3cJzWOc", "s0iXtH64swI"]
video_url = random.choice(video_urls)

# Função para encontrar o primeiro dispositivo Chromecast disponível
def find_chromecast():
    chromecasts, browser = pychromecast.get_chromecasts()
    if chromecasts:
        return chromecasts[0]
    return None

# Função para compartilhar e controlar o vídeo do YouTube
def cast_and_control_youtube(video_url):
    cast = find_chromecast()
    if cast:
        cast.wait()
        yt_controller = youtube.YouTubeController()
        cast.register_handler(yt_controller)
        yt_controller.play_video(video_url)
        print(f"Compartilhando e controlando {video_url} no Chromecast: {cast.name}")
        cast.media_controller.block_until_active()
        my_id = cast.status.app_id
        yt_screen_id = cast.status.display_name
        while True:
            time.sleep(2)
            yt_controller.add_to_queue(random.choice(video_urls))
            if my_id != cast.status.app_id or yt_screen_id != cast.status.display_name:
                print("Reconectando ao Chromecast...")
                cast_and_control_youtube(video_url)
    else:
        print("Nenhum dispositivo Chromecast encontrado na rede.")

if __name__ == "__main__":
    cast_and_control_youtube(video_url)
