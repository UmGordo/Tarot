# Tarô v2 - Leitura Interativa de Cartas 🃏

Uma implementação moderna de um baralho de Tarô com suporte para terminal (ASCII art) e web (interface HTML/CSS/JS responsiva).

## 📋 Características

✨ **78 cartas completas** - 22 Arcanos Maiores + 56 cartas dos 4 naipes  
🎨 **Design responsivo** - Procedural layout que se adapta a qualquer tamanho de terminal  
📱 **Mobile-friendly** - Layouts verticais para telas pequenas  
🌈 **ANSI colors** - Cores diferentes por naipe (Maiores, Paus, Copas, Espadas, Ouros)  
🎭 **Duas interfaces** - Terminal (Python/CLI) e Web (HTML5/CSS3/JavaScript)  

## 🚀 Instalação

Não há dependências externas! Usa apenas bibliotecas padrão do Python 3.

```bash
# Nenhuma instalação necessária
# Tudo pronto para usar!
```

## 💻 Terminal (CLI)

### Interface Interativa (Recomendado)

Execute o programa interativo estilo **Metasploit** com menu bonito e loop contínuo:

```bash
./taro.py                       # Inicia a interface interativa
```

**Menu interativo com:**
- 🎲 Tirar cartas (quantidade customizável)
- 📚 Listar por naipe
- 🔍 Buscar cartas
- 🎴 Demonstração automática
- 📊 Informações do baralho
- ℹ️ Sobre o programa

### CLI Direto (Sem interface)

Para usar sem o loop interativo:

```bash
./cli.py --tirar 3              # Tira 3 cartas em layout vertical
./cli.py --tirar 5 --layout grid  # Tira 5 cartas em layout grid
```

**Opções disponíveis:**
```bash
./cli.py --demo                 # Demo com 5 cartas em grid
./cli.py --listar maiores       # Lista todos os Arcanos Maiores
./cli.py --listar paus          # Lista Paus (14 cartas)
./cli.py --listar copas         # Lista Copas (14 cartas)
./cli.py --listar espadas       # Lista Espadas (14 cartas)
./cli.py --listar ouros         # Lista Ouros (14 cartas)
./cli.py --search "Mundo"       # Busca "O Mundo"
./cli.py --search "Mago"        # Busca "O Mago"
./cli.py --info                 # Mostra estatísticas do baralho
./cli.py --help                 # Mostra ajuda completa
```

## 🌐 Web

Acesse a interface web interativa:

```bash
# No diretório raiz do projeto
cd /workspaces/Tarot
python3 -m http.server 8080

# Abra no navegador: http://localhost:8080
```

### Recursos Web

- 🎨 Design escuro com gradientes
- 🎴 Cards com cores específicas por naipe
- ✨ Hover effects e animações suaves
- 📱 Responsivo (grid adapta a desktop e mobile)
- 🎲 Shuffle com Fisher-Yates
- 🔄 Tirar novamente sem recarregar

## 📁 Estrutura

```
v2/
├── cli.py              # Interface de linha de comando (executável)
├── card_model.py       # Modelo de Carta + rendering ASCII
├── design_tokens.py    # Configuração centralizada (cores, proporções, etc)
├── baralho.py          # Baralho com 78 cartas
└── README.md           # Este arquivo

../
├── index.html          # Interface web interativa
└── card.py             # (v1 - anterior)
```

## 🎨 Arquitetura

### Interface Interativa (`taro.py`)

Interface estilo **Metasploit/Hydra** com:
- **Banner ASCII** colorido no estilo hacker
- **Menu numeral** com 6 opções principales
- **Animações de carregamento** tipo spinner
- **Cores ANSI** para melhor legibilidade
- **Loop infinito** até o usuário escolher sair
- **Mensagens contextuais** [✓] sucesso, [!] erro, [?] pergunta, [i] info

### CLI Direto (`cli.py`)

Interface de linha de comando tradicional com argparse:
- Opções diretas (`--tirar`, `--search`, `--listar`, etc)
- Saída direta sem menu
- Ideal para scripts e automação

### Design Tokens

Centraliza toda a configuração em `design_tokens.py`:
- Cores ANSI por naipe
- Proporções de aspecto (0.55 altura/largura)
- Tamanhos mínimos e máximos de cartas
- Caracteres de borda
- Símbolos Unicode

### Layout Responsivo

A função `compute_layout()` calcula dimensões baseado em:
1. Tamanho do terminal (`get_terminal_size()` com 5 fallbacks)
2. Tokens de design
3. Quantidade de cartas por linha (`cards_per_row`)
4. Modo compacto (`ignore_rows=True` por padrão)

### Sem hardcoded values

Todo tamanho, espaçamento e cor é calculado dinamicamente:
- Card width = (terminal_width - padding) / cards_per_row
- Card height = width * aspect_ratio
- Text wrap width = card_width - 2 (bordas)

## 📚 Classes e Funções

### Card (card_model.py)

```python
card = Card(
    name="O Mago",
    suit="Maiores",
    number=1,
    symbol="★",
    description="Poder, criatividade, habilidade"
)
```

### Baralho (baralho.py)

```python
baralho = Baralho()
cartas = baralho.tirar(3)           # 3 cartas aleatórias
maiores = baralho.listar_por_naipe('Maiores')
carta = baralho.get_carta_por_nome('O Mundo')
```

### Rendering (card_model.py)

```python
output = render_cards_grid(
    cartas,
    requested_cards_per_row=1,      # 1 = vertical, 3 = grid
    ignore_rows=True                # layout compacto
)
print(output)  # ASCII art com cores ANSI
```

## 🌈 Cores por Naipe

- **Maiores** (Purple): `#8b4fc1` | `\033[95m` (Magenta)
- **Paus** (Gold): `#d4a574` | Amarelo claro
- **Copas** (Red): `#e74c3c` | Vermelho
- **Espadas** (Dark): `#34495e` | Cinza escuro
- **Ouros** (Orange): `#f39c12` | Amarelo

## 📊 Exemplo de Saída

```
        ┌──────────────────────────────────────────────────────────┐
        │                         O Mago                           │
        │                            ★                             │
        │                                                          │
        ├──────────────────────────────────────────────────────────┤
        │               Poder, criatividade, habilidade            │
        └──────────────────────────────────────────────────────────┘
```

## 🛠️ Desenvolvimento

### Adicionar nova carta

Em `baralho.py`, adicione tupla `(número, nome, descrição)` à lista apropriada:

```python
maiores = [
    (0, 'O Louco', 'Descrição...'),
    # Adicionar aqui ↓
    (22, 'Nova Carta', 'Nova descrição'),
]
```

### Modificar design

Edite `design_tokens.py`:

```python
DESIGN_TOKENS = {
    'aspect_ratio': 0.55,           # altura/largura de cartas
    'min_card_width': 20,           # largura mínima
    'max_card_width_ratio': 0.6,    # máximo 60% da tela
    'color_tokens': {...},          # cores ANSI
    'symbols': {...},               # símbolos Unicode
}
```

### Rodar testes

```bash
python3 -c "from baralho import Baralho; b = Baralho(); print(len(b.cartas))"
# Output: 78
```

## 🎯 Próximos Passos (Planejado)

- [ ] Complex ASCII art designs para centros de cartas
- [ ] Layouts de spread (3-card, Cruz Celta, etc)
- [ ] Significados para posições invertidas
- [ ] Persistência de histórico de leituras
- [ ] Temas alternativos (light mode, sépia, etc)
- [ ] Integração entre web e terminal (API)

## 📝 Notas

- **Terminal**: Funciona melhor em terminais com pelo menos 80x24 caracteres
- **Web**: Chrome, Firefox, Safari, Edge (suporte moderno para CSS Grid e Flexbox)
- **Python**: Requer Python 3.6+ (usa type hints)

## 🤝 Uso Programático

```python
from baralho import Baralho
from card_model import render_cards_grid

# Criar baralho
baralho = Baralho()

# Tirar 5 cartas
cartas = baralho.tirar(5)

# Renderizar em ASCII art
saida = render_cards_grid(cartas, requested_cards_per_row=2, ignore_rows=True)
print(saida)
```

## 📄 Licença

Livre para uso pessoal e educacional.

---

**Versão**: 2.0  
**Ultima atualização**: Dezembro 2024
