import webbrowser

def video_explicativo(video_link="https://www.youtube.com/watch?v=dQw4w9WgXcQ") -> None:
    """
    Função para exibir um vídeo explicativo do YouTube.

    Args:
    video_link (str): URL do vídeo do YouTube a ser exibido. 
                      O padrão é "https://www.youtube.com/watch?v=dQw4w9WgXcQ".
    """
    webbrowser.open(video_link)
