"""
Modelo de Carta de Tarô com Arte ASCII e Cores ANSI (render responsivo)
Usa tokens centralizados em `v2/design_tokens.py` para calcular layout.
"""

import os
import sys
import shutil
import textwrap

# Garantir que o diretório `v2` está no path quando executado diretamente
sys.path.insert(0, os.path.dirname(__file__))
from design_tokens import DESIGN_TOKENS, terminal_size


class Card:
    """Modelo de uma carta de Tarô"""

    def __init__(self, name: str, suit: str, number: int = None, symbol: str = "✦", description: str = ""):
        self.name = name
        self.suit = suit  # "Maiores", "Paus", "Copas", "Espadas", "Ouros"
        self.number = number
        self.symbol = symbol
        self.description = description
        self.is_reversed = False

    def _suit_color(self):
        return DESIGN_TOKENS['color_tokens'].get(self.suit, DESIGN_TOKENS['color_tokens']['Espadas'])

    def _suit_symbol(self):
        return DESIGN_TOKENS['symbols'].get(self.suit, self.symbol)

    def render(self, cols=None, rows=None, requested_cards_per_row=None):
        """Renderiza a carta de forma procedural/responsiva.

        Recebe opcionalmente `cols`/`rows` (útil para testes); caso contrário lê terminal atual.
        """
        cols = cols or terminal_size()[0]
        rows = rows or terminal_size()[1]

        # compute layout
        layout = compute_layout(cols=cols, rows=rows, requested_cards_per_row=requested_cards_per_row)
        w = layout['card_width']
        h = layout['card_height']
        wrap_w = layout['wrap_width']
        border = DESIGN_TOKENS['border_chars']
        color = self._suit_color()
        reset = DESIGN_TOKENS['color_tokens']['RESET']
        bold = DESIGN_TOKENS['color_tokens']['BOLD']
        gray = DESIGN_TOKENS['color_tokens']['GRAY']

        # Build and return joined string (for backward compatibility)
        return '\n'.join(generate_card_lines(self, layout))

    def reverse(self):
        self.is_reversed = not self.is_reversed
        return self


def compute_layout(cols=None, rows=None, requested_cards_per_row=None, tokens=None, ignore_rows=False, sample_cards=None):
    """Calcula tamanho de carta e parâmetros relacionados responsivamente.

    Retorna dicionário com 'card_width', 'card_height', 'wrap_width', 'cards_per_row', 'container_padding'
    """
    import math
    tokens = tokens or DESIGN_TOKENS
    cols = cols or terminal_size()[0]
    rows = rows or terminal_size()[1]

    base_unit = max(1, cols // 100)
    container_padding = int(cols * tokens.get('container_padding_ratio', 0.04))
    gutter = max(1, base_unit * tokens.get('gutter_units', 2))
    min_card_width = tokens.get('min_card_width', 20)
    max_card_width_ratio = tokens.get('max_card_width_ratio', 0.6)
    aspect_ratio = tokens.get('aspect_ratio', 0.55)
    min_card_height = tokens.get('min_card_height', 7)

    # decide cards per row
    if requested_cards_per_row:
        cards_per_row = requested_cards_per_row
    else:
        if cols < 60:
            cards_per_row = 1
        elif cols < 120:
            cards_per_row = 2
        elif cols < 200:
            cards_per_row = 3
        else:
            cards_per_row = min(4, max(1, cols // 40))

    available = cols - 2 * container_padding - (cards_per_row - 1) * gutter
    card_width = max(min_card_width, available // cards_per_row)
    card_width = min(card_width, int(cols * max_card_width_ratio))

    # altura da carta: usar fator relativo (altura = largura * aspect_ratio)
    # altura da carta: por padrão usa proporção, mas pode ser ajustada
    default_height = max(min_card_height, int(card_width * aspect_ratio))

    # Se o chamador passar sample_cards e pedir compactamento (ignore_rows=True),
    # calcule a altura mínima necessária baseada no conteúdo (título + símbolo + descrição)
    def compute_min_height_for_card(title, description, wrap_w):
        import textwrap
        title_lines = textwrap.wrap(title or '', wrap_w)
        if len(title_lines) > 2:
            title_lines = title_lines[:2]
        desc_lines = textwrap.wrap(description or '', wrap_w)
        # estrutura: top border (1), title_lines, padding optional(0), middle(1), separator(1), desc_lines, bottom border(1)
        h = 1 + len(title_lines) + 1 + 1 + len(desc_lines) + 1
        return max(min_card_height, h)

    if ignore_rows and sample_cards:
        # calcule altura mínima necessária para todas as cartas do sample e use o máximo
        candidate_heights = [compute_min_height_for_card(c.name, c.description, max(1, card_width - 2 - base_unit * 2)) for c in sample_cards]
        card_height = max(candidate_heights) if candidate_heights else default_height
        card_height = max(min_card_height, card_height)
    else:
        card_height = default_height

    # wrap width for content inside borders
    wrap_width = max(1, card_width - 2 - max(1, base_unit) * 2)

    return {
        'cols': cols,
        'rows': rows,
        'cards_per_row': cards_per_row,
        'card_width': card_width,
        'card_height': card_height,
        'wrap_width': wrap_width,
        'container_padding': container_padding,
        'gutter': gutter,
    }


def generate_card_lines(card: Card, layout: dict):
    """Gera lista de linhas (strings) para uma carta com base no layout fornecido.

    Isso permite compor múltiplas cartas lado a lado.
    """
    w = layout['card_width']
    h = layout['card_height']
    wrap_w = layout['wrap_width']
    border = DESIGN_TOKENS['border_chars']
    color = DESIGN_TOKENS['color_tokens'].get(card.suit, DESIGN_TOKENS['color_tokens']['Espadas'])
    reset = DESIGN_TOKENS['color_tokens']['RESET']
    bold = DESIGN_TOKENS['color_tokens']['BOLD']
    gray = DESIGN_TOKENS['color_tokens']['GRAY']

    lines = []
    # top border
    lines.append(color + bold + border['tl'] + border['h'] * (w - 2) + border['tr'] + reset)

    # Title wrap (up to 2 lines)
    title_wrapped = textwrap.wrap(card.name, wrap_w)
    if len(title_wrapped) > 2:
        title_wrapped = title_wrapped[:2]

    # content area height (space between top border and separator)
    content_height = h - 4

    # add title lines
    for t in title_wrapped:
        tline = t.center(w - 2)
        lines.append(color + border['v'] + bold + tline + reset + color + border['v'] + reset)

    # padding above/below middle symbol. Use compact layout: only minimal padding
    # remaining lines available for padding and ensure middle is visible
    remaining = content_height - len(title_wrapped) - 1  # reserve 1 for middle symbol
    if remaining < 0:
        remaining = 0
    pad_top = remaining // 2
    pad_bottom = remaining - pad_top
    for _ in range(pad_top):
        lines.append(color + border['v'] + ' ' * (w - 2) + border['v'] + reset)

    # middle symbol
    mid = DESIGN_TOKENS['symbols'].get(card.suit, card.symbol).center(w - 2)
    lines.append(color + border['v'] + mid + border['v'] + reset)

    # pad bottom of content
    for _ in range(pad_bottom):
        lines.append(color + border['v'] + ' ' * (w - 2) + border['v'] + reset)

    # separator
    lines.append(color + border['sep_t'] + border['h'] * (w - 2) + border['sep_b'] + reset)

    # description lines (fit remaining space)
    desc_wrapped = textwrap.wrap(card.description or '', wrap_w)
    max_desc_lines = max(1, h - len(lines) - 1)
    desc_wrapped = desc_wrapped[:max_desc_lines]
    for d in desc_wrapped:
        dline = d.center(w - 2)
        lines.append(color + border['v'] + gray + dline + reset + color + border['v'] + reset)

    # bottom border
    lines.append(color + border['bl'] + border['h'] * (w - 2) + border['br'] + reset)

    # reversed indicator not included in card block; caller may show it below grid
    return lines


def render_cards_grid(cards, cols=None, rows=None, requested_cards_per_row=1, ignore_rows=True):
    """Renderiza lista de cartas em layout vertical (uma embaixo da outra).

    Por padrão, força `cards_per_row=1` para layout mobile-friendly (portabilidade para celular).
    Cada carta fica em uma "linha" independente, facilitando scroll vertical.

    Se `ignore_rows=True` (padrão), o layout ignora altura do terminal e usa altura compacta
    baseada no conteúdo (sem espaços verticais sobrando).

    Parâmetros:
    - cards: lista de Card
    - cols, rows: dimensões do terminal (auto-detecta se None)
    - requested_cards_per_row: default=1 (vertical layout). Mude para >1 se quiser grid.
    - ignore_rows: default=True (layout compacto baseado em conteúdo)
    """
    cols = cols or terminal_size()[0]
    rows = rows or terminal_size()[1]
    layout = compute_layout(cols=cols, rows=rows, requested_cards_per_row=requested_cards_per_row, ignore_rows=ignore_rows, sample_cards=cards if ignore_rows else None)

    out_lines = []
    pad = ' ' * layout['container_padding']

    # Renderiza cada carta verticalmente (uma por linha)
    for card in cards:
        card_lines = generate_card_lines(card, layout)
        for line in card_lines:
            out_lines.append(pad + line)

        # Indicador de invertida abaixo da carta se aplicável
        if card.is_reversed:
            indicator = DESIGN_TOKENS['invert_indicator'].center(layout['card_width'])
            out_lines.append(pad + indicator)
        
        # Espaço em branco entre cartas
        out_lines.append('')

    return '\n'.join(out_lines)


# Exemplos de uso / demo simples se executado diretamente
if __name__ == '__main__':
    # pequenas demos para validar responsividade
    cards = [
        Card('O Mago', 'Maiores', 1, symbol='★', description='Habilidade e recursos'),
        Card('Ás de Copas', 'Copas', 1, symbol='♡', description='Novo amor, começo emocional'),
        Card('Cinco de Espadas', 'Espadas', 5, symbol='♠', description='Conflito e perda'),
        Card('A Torre', 'Maiores', 16, symbol='⚡', description='Mudança súbita e libertação')
    ]

    # Print demo with current terminal size
    for c in cards:
        print(c.render())
        print()



