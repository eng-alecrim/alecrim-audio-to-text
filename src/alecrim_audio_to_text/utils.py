# =============================================================================
# BIBLIOTECAS E MÓDULOS
# =============================================================================

from pathlib import Path
from typing import Callable, Union

# =============================================================================
# FUNÇÕES
# =============================================================================

# -----------------------------------------------------------------------------
# Retorna o diretório do projeto
# -----------------------------------------------------------------------------


def get_path_project(
    nome_projeto: str, path_projeto: Path = Path.cwd()
) -> Union[Callable, Path]:
    if path_projeto.name == nome_projeto:
        return path_projeto
    return get_path_project(path_projeto.parent, nome_projeto)
