from src.alecrim_audio_to_text.transcricao import audio_to_text


def main() -> None:
    audio_file_path = input("Insira o caminho do áudio: ")
    audio_to_text(audio_file_path=audio_file_path)
    return None


if __name__ == "__main__":
    main()
