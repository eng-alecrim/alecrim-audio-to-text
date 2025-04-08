# Bibliotecas
from alecrim_audio_to_text.transcricao import audio_to_text, EnvVariable
from dotenv import find_dotenv, load_dotenv
import os

# Carregando as variáveis de ambiente
load_dotenv(find_dotenv())

env_variables = EnvVariable(
    os.getenv("NOME_PROJETO"),
    os.getenv("SPEECH_KEY"),
    os.getenv("SPEECH_REGION"),
)


# Função main
def main() -> None:
    audio_file_path = input("Insira o caminho do áudio: ")
    audio_to_text(audio_file_path, env_variables=env_variables)
    return None


# Execução
if __name__ == "__main__":
    main()
