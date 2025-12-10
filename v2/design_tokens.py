"""
Design tokens para o render responsivo das cartas (ASCII + ANSI).
Centraliza valores e estilos para manter energia concentrada.

Contém uma função robusta `get_terminal_size()` que tenta múltiplos métodos
para recuperar tamanho do terminal (cols, rows) com fallbacks seguros.
"""
import os
import sys
import shutil
import struct
import subprocess
try:
    import fcntl
    import termios
except Exception:
    fcntl = None
    termios = None

# Valores base (podem ser ajustados pelo usuário)
DESIGN_TOKENS = {
    # Percentual do terminal usado como padding lateral
    'container_padding_ratio': 0.04,

    # Largura mínima de carta (colunas)
    'min_card_width': 20,

    # Máxima proporção de largura para uma única carta
    'max_card_width_ratio': 0.6,

    # Proporção largura/altura (cols / rows)
    'aspect_ratio': 0.55,

    # Altura mínima (linhas)
    'min_card_height': 7,

    # Gutter entre cartas (multiplicador de base_unit)
    'gutter_units': 2,

    # token para bordas (troque estilo fácil)
    'border_chars': {
        'tl': '┌', 'tr': '┐', 'bl': '└', 'br': '┘', 'h': '─', 'v': '│', 'sep_t': '├', 'sep_b': '┤'
    },

    # Cores ANSI por naipe (padrões)
    'color_tokens': {
        'Maiores': '\033[35m',
        'Paus': '\033[33m',
        'Copas': '\033[36m',
        'Espadas': '\033[97m',
        'Ouros': '\033[33m',
        'RESET': '\033[0m',
        'BOLD': '\033[1m',
        'GRAY': '\033[90m'
    },

    # Símbolos por naipe
    'symbols': {
        'Maiores': '★', 'Paus': '✦', 'Copas': '♡', 'Espadas': '♠', 'Ouros': '◆'
    },

    # Indicador invertida
    'invert_indicator': '⟲ INVERTIDA ⟲',

    # Animação: frames relativos para revelação (simples)
    'reveal_frames': 4,
}


def terminal_size():
    # deprecated wrapper: mantemos para compatibilidade
    return get_terminal_size()


def get_terminal_size(fallback=(80, 24)):
    """Retorna (cols, rows) do terminal usando múltiplos fallbacks.

    Estratégia:
    1. `shutil.get_terminal_size()` (Python 3.3+)
    2. ioctl em file descriptors 0,1,2 (quando disponíveis)
    3. `stty size` via subprocess
    4. variáveis de ambiente `COLUMNS` e `LINES`
    5. fallback passado como parâmetro
    """
    # 1) tentativa direta
    try:
        sz = shutil.get_terminal_size()
        return sz.columns, sz.lines
    except Exception:
        pass

    # helper ioctl
    def ioctl_get(fd):
        if not fcntl or not termios:
            return None
        try:
            cr = fcntl.ioctl(fd, termios.TIOCGWINSZ, struct.pack('hhhh', 0, 0, 0, 0))
            rows, cols, _, _ = struct.unpack('hhhh', cr)
            if cols and rows:
                return cols, rows
        except Exception:
            return None

    for fd in (0, 1, 2):
        r = ioctl_get(fd)
        if r:
            return r

    # 3) stty size
    try:
        out = subprocess.check_output(['stty', 'size'], stderr=subprocess.DEVNULL).split()
        if len(out) >= 2:
            rows = int(out[0]); cols = int(out[1])
            return cols, rows
    except Exception:
        pass

    # 4) environment
    try:
        cols = int(os.environ.get('COLUMNS', 0))
        rows = int(os.environ.get('LINES', 0))
        if cols and rows:
            return cols, rows
    except Exception:
        pass

    # 5) fallback
    return fallback
