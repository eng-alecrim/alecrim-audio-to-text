# =============================================================================
# BIBLIOTECAS E MÓDULOS
# =============================================================================

import os
import time
from pathlib import Path

import azure.cognitiveservices.speech as speechsdk
import dotenv

from .utils import get_path_project

# =============================================================================
# CONSTANTES
# =============================================================================

# Carregando as variáveis de ambiente
dotenv.load_dotenv()

# Diretórios
DIR_PROJETO = get_path_project()
DIR_OUTPUT = DIR_PROJETO / "data/raw/transcriptions"
DIR_OUTPUT.mkdir(exist_ok=True, parents=True)

# =============================================================================
# FUNÇÕES
# =============================================================================

# -----------------------------------------------------------------------------
# Retorna o diretório do projeto
# -----------------------------------------------------------------------------


def audio_to_text(audio_file_path: str, audio_language: str = "pt-BR") -> None:
    """
    Converte áudio de fala em texto usando o Azure Cognitive Services Speech SDK.

    Args:
        audio_file_path (str, optional): Caminho para o arquivo de áudio a ser transcrito.
        audio_language (str, optional): Idioma da fala a ser reconhecida. Padrão é "pt-BR" (Português do Brasil).

    Returns:
        None

    Raises:
        Exception: Se ocorrer um erro durante o reconhecimento de fala.

    Notes:
        - Esta função requer variáveis de ambiente chamadas "SPEECH_KEY" e "SPEECH_REGION" configuradas com a chave de 
          assinatura e a região válidas do Azure Cognitive Services Speech.
        - O texto reconhecido é salvo em um arquivo na pasta "output/transcricoes/".
    """

    # Função auxiliar para escrever o texto reconhecido em um arquivo
    def write_to_file(f_path: Path, text: str) -> None:
        try:
            # Verifica se o arquivo existe
            if f_path.exists():
                text = "\n" + text

            # Abre o arquivo no modo de adição ('a')
            with open(f_path, "a") as file:
                # Escreve o texto no arquivo
                file.write(text)

            print("Texto escrito com sucesso no arquivo.")
        except Exception as e:
            print("OCORREU UM ERRO:", e)

    # Função de callback para parar o reconhecimento contínuo
    def stop_cb(evt):
        print("Encerrando em {}".format(evt))
        speech_recognizer.stop_continuous_recognition()
        nonlocal done
        done = True

    # Função para lidar com o resultado final do reconhecimento
    def handle_final_result(evt):
        # Escreve o texto reconhecido em um arquivo na pasta "output/transcricoes/"
        output_path = DIR_OUTPUT / f"{Path(audio_file_path).stem}.txt"
        write_to_file(output_path, evt.result.text)
        return None

    # Configurações de fala
    speech_config = speechsdk.SpeechConfig(subscription=os.environ.get("SPEECH_KEY"), region=os.environ.get("SPEECH_REGION"))
    speech_config.speech_recognition_language = audio_language
    audio_config = speechsdk.audio.AudioConfig(filename=audio_file_path)

    # Inicializa o reconhecedor de fala
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    done = False

    # Conecta os eventos ao reconhecedor de fala
    speech_recognizer.recognized.connect(lambda evt: handle_final_result(evt))
    speech_recognizer.session_started.connect(lambda evt: print("Sessão iniciada: {}".format(evt)))
    speech_recognizer.session_stopped.connect(lambda evt: print("Sessão encerrada: {}".format(evt)))
    speech_recognizer.canceled.connect(lambda evt: print("Cancelado: {}".format(evt)))

    # Conecta os eventos de parada ao callback de parada
    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    # Inicia o reconhecimento contínuo
    speech_recognizer.start_continuous_recognition()
    while not done:
        time.sleep(.5)

    return None
