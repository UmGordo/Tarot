#!/usr/bin/env python3
"""
🃏 TARÔ v2.0 - Interface Unificada
Executa como: ./taro.py [--cli [opções] | --demo]
- Sem argumentos: Interface interativa (Metasploit style)
- Com --cli: CLI direto com argparse
- Com --demo: Demonstração visual
"""

import os
import sys
import time
import argparse

# Garantir que o diretório `v2` está no path
sys.path.insert(0, os.path.dirname(__file__))
from baralho import Baralho
from card_model import render_cards_grid
from design_tokens import DESIGN_TOKENS


# ============================================================================
# CORES E ESTILOS
# ============================================================================

class Colors:
    """Cores ANSI para terminal"""
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    MAGENTA = '\033[95m'
    BLUE = '\033[94m'
    WHITE = '\033[97m'
    GRAY = '\033[90m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    UNDERLINE = '\033[4m'


def clear_screen():
    """Limpa a tela"""
    os.system('clear' if os.name == 'posix' else 'cls')


def print_banner():
    """Printa banner estilo Metasploit"""
    banner = f"""
{Colors.MAGENTA}{Colors.BOLD}
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║  ████████╗ █████╗ ██████╗ █████╗ ██╗   ██╗███████╗██╗  ██╗      ║
║  ╚══██╔══╝██╔══██╗██╔══██╗██╔══██╗██║   ██║██╔════╝╚██╗██╔╝      ║
║     ██║   ███████║██████╔╝███████║██║   ██║███████╗ ╚███╔╝       ║
║     ██║   ██╔══██║██╔══██╗██╔══██║██║   ██║╚════██║ ██╔██╗       ║
║     ██║   ██║  ██║██║  ██║██║  ██║╚██████╔╝███████║██╔╝ ██╗      ║
║     ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝      ║
║                                                                   ║
║              {Colors.CYAN}Leitura Interativa de Cartas de Tarô{Colors.MAGENTA}               ║
║                    {Colors.YELLOW}v2.0 - Terminal Edition{Colors.MAGENTA}                      ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
{Colors.RESET}
"""
    print(banner)


def print_menu():
    """Printa menu de opções"""
    menu = f"""
{Colors.CYAN}{Colors.BOLD}[*] MENU PRINCIPAL{Colors.RESET}
{Colors.GRAY}{'─' * 70}{Colors.RESET}

  {Colors.GREEN}1{Colors.RESET} │ {Colors.BOLD}Tirar Cartas{Colors.RESET}            Tire N cartas aleatórias
  {Colors.GREEN}2{Colors.RESET} │ {Colors.BOLD}Listar por Naipe{Colors.RESET}      Veja todas as cartas de um naipe
  {Colors.GREEN}3{Colors.RESET} │ {Colors.BOLD}Buscar Carta{Colors.RESET}          Procure uma carta específica
  {Colors.GREEN}4{Colors.RESET} │ {Colors.BOLD}Demonstração{Colors.RESET}         Veja 5 cartas em layout grid
  {Colors.GREEN}5{Colors.RESET} │ {Colors.BOLD}Informações{Colors.RESET}          Estatísticas do baralho
  {Colors.GREEN}6{Colors.RESET} │ {Colors.BOLD}Sobre{Colors.RESET}                Informações do programa

  {Colors.RED}0{Colors.RESET} │ {Colors.BOLD}Sair{Colors.RESET}                  Encerrar o programa

{Colors.GRAY}{'─' * 70}{Colors.RESET}
"""
    print(menu)


def print_header(title: str):
    """Printa header de seção"""
    print(f"\n{Colors.CYAN}{Colors.BOLD}[*] {title}{Colors.RESET}\n{Colors.GRAY}{'─' * 70}{Colors.RESET}\n")


def print_success(message: str):
    """Printa mensagem de sucesso"""
    print(f"{Colors.GREEN}[✓]{Colors.RESET} {message}")


def print_info(message: str):
    """Printa mensagem informativa"""
    print(f"{Colors.CYAN}[i]{Colors.RESET} {message}")


def print_error(message: str):
    """Printa mensagem de erro"""
    print(f"{Colors.RED}[!]{Colors.RESET} {message}")


def print_prompt(message: str) -> str:
    """Printa prompt e retorna input"""
    return input(f"{Colors.YELLOW}[?]{Colors.RESET} {message} {Colors.CYAN}➤{Colors.RESET} ")


def animate_loading(message: str = "Processando", duration: float = 0.5):
    """Animação de carregamento estilo hacker"""
    frames = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    start = time.time()
    idx = 0
    
    while time.time() - start < duration:
        print(f"\r{Colors.CYAN}{frames[idx % len(frames)]}{Colors.RESET} {message}...", end='', flush=True)
        time.sleep(0.05)
        idx += 1
    
    print(f"\r{Colors.GREEN}✓{Colors.RESET} {message}...    ", flush=True)


# ============================================================================
# INTERFACE INTERATIVA (Metasploit style)
# ============================================================================

def interactive_tirar_cartas(baralho: Baralho):
    """Menu: Tirar cartas"""
    clear_screen()
    print_banner()
    print_header("TIRAR CARTAS")
    
    while True:
        try:
            qtd_str = print_prompt("Quantas cartas? (1-78)")
            qtd = int(qtd_str)
            if qtd < 1 or qtd > 78:
                print_error(f"Valor inválido! Use entre 1 e 78.")
                continue
            break
        except ValueError:
            print_error("Digite um número válido!")
    
    layout_choice = print_prompt("Layout: [1] Vertical (padrão) [2] Grid").strip()
    layout = 'grid' if layout_choice == '2' else 'vert'
    
    animate_loading("Tirando cartas do baralho")
    cartas = baralho.tirar(qtd)
    
    print()
    if layout == 'grid':
        output = render_cards_grid(cartas, requested_cards_per_row=3, ignore_rows=True)
    else:
        output = render_cards_grid(cartas, requested_cards_per_row=1, ignore_rows=True)
    
    print(output)
    print_success(f"Total de {len(cartas)} carta(s) tirada(s)!")
    input(f"\n{Colors.GRAY}Pressione ENTER para continuar...{Colors.RESET}")


def interactive_listar_por_naipe(baralho: Baralho):
    """Menu: Listar por naipe"""
    clear_screen()
    print_banner()
    print_header("LISTAR POR NAIPE")
    
    naipes = {'1': 'Maiores', '2': 'Paus', '3': 'Copas', '4': 'Espadas', '5': 'Ouros'}
    
    print(f"  {Colors.GREEN}1{Colors.RESET} │ {Colors.BOLD}Arcanos Maiores{Colors.RESET}  (22 cartas)\n"
          f"  {Colors.GREEN}2{Colors.RESET} │ {Colors.BOLD}Paus{Colors.RESET}             (14 cartas)\n"
          f"  {Colors.GREEN}3{Colors.RESET} │ {Colors.BOLD}Copas{Colors.RESET}            (14 cartas)\n"
          f"  {Colors.GREEN}4{Colors.RESET} │ {Colors.BOLD}Espadas{Colors.RESET}          (14 cartas)\n"
          f"  {Colors.GREEN}5{Colors.RESET} │ {Colors.BOLD}Ouros{Colors.RESET}            (14 cartas)\n\n{Colors.GRAY}{'─' * 70}{Colors.RESET}\n")
    
    choice = print_prompt("Escolha um naipe (1-5)")
    
    if choice not in naipes:
        print_error("Opção inválida!")
        input(f"\n{Colors.GRAY}Pressione ENTER para continuar...{Colors.RESET}")
        return
    
    naipe = naipes[choice]
    animate_loading(f"Listando cartas de {naipe}")
    cartas = baralho.listar_por_naipe(naipe)
    
    print()
    output = render_cards_grid(cartas, requested_cards_per_row=2, ignore_rows=True)
    print(output)
    
    print_success(f"Total de {len(cartas)} carta(s) em {naipe}!")
    input(f"\n{Colors.GRAY}Pressione ENTER para continuar...{Colors.RESET}")


def interactive_buscar_carta(baralho: Baralho):
    """Menu: Buscar carta"""
    clear_screen()
    print_banner()
    print_header("BUSCAR CARTA")
    
    nome = print_prompt("Digite o nome da carta (ou parte dele)")
    
    if not nome.strip():
        print_error("Digite um nome válido!")
        input(f"\n{Colors.GRAY}Pressione ENTER para continuar...{Colors.RESET}")
        return
    
    animate_loading(f"Buscando '{nome}'")
    carta = baralho.get_carta_por_nome(nome)
    
    if not carta:
        search_lower = nome.lower()
        matches = [c for c in baralho.cartas if search_lower in c.name.lower()]
        
        if matches and len(matches) > 1:
            print()
            print_info(f"Encontradas {len(matches)} cartas com '{nome}':\n")
            for i, c in enumerate(matches, 1):
                print(f"  {Colors.CYAN}{i:2d}{Colors.RESET} │ {c.name} ({Colors.YELLOW}{c.suit}{Colors.RESET})")
            
            try:
                idx_str = print_prompt("Escolha uma carta (número)")
                idx = int(idx_str) - 1
                if 0 <= idx < len(matches):
                    carta = matches[idx]
                else:
                    print_error("Índice inválido!")
                    input(f"\n{Colors.GRAY}Pressione ENTER para continuar...{Colors.RESET}")
                    return
            except ValueError:
                print_error("Digite um número válido!")
                input(f"\n{Colors.GRAY}Pressione ENTER para continuar...{Colors.RESET}")
                return
        elif matches:
            carta = matches[0]
    
    if carta:
        print()
        print_success(f"Carta encontrada: {Colors.BOLD}{carta.name}{Colors.RESET}")
        print()
        output = render_cards_grid([carta], requested_cards_per_row=1, ignore_rows=True)
        print(output)
    else:
        print()
        print_error(f"Nenhuma carta encontrada com '{nome}'")
    
    input(f"\n{Colors.GRAY}Pressione ENTER para continuar...{Colors.RESET}")


def interactive_demo(baralho: Baralho):
    """Menu: Demonstração"""
    clear_screen()
    print_banner()
    print_header("DEMONSTRAÇÃO - 5 CARTAS ALEATÓRIAS")
    
    animate_loading("Gerando demonstração")
    cartas = baralho.tirar(5)
    
    print()
    output = render_cards_grid(cartas, requested_cards_per_row=3, ignore_rows=True)
    print(output)
    
    print_success("Demonstração concluída!")
    input(f"\n{Colors.GRAY}Pressione ENTER para continuar...{Colors.RESET}")


def interactive_info(baralho: Baralho):
    """Menu: Informações"""
    clear_screen()
    print_banner()
    print_header("INFORMAÇÕES DO BARALHO")
    
    total = len(baralho.cartas)
    naipes = {}
    for carta in baralho.cartas:
        naipe = carta.suit
        naipes[naipe] = naipes.get(naipe, 0) + 1
    
    print(f"{Colors.CYAN}{Colors.BOLD}Estatísticas:{Colors.RESET}\n  {Colors.GREEN}Total de cartas:{Colors.RESET} {Colors.BOLD}{total}{Colors.RESET}\n")
    print(f"{Colors.CYAN}{Colors.BOLD}Por naipe:{Colors.RESET}")
    
    for naipe, qtd in sorted(naipes.items()):
        symbol = DESIGN_TOKENS['symbols'].get(naipe, '?')
        print(f"  {Colors.YELLOW}{symbol}{Colors.RESET}  {naipe:15} {Colors.BOLD}{qtd:2d} cartas{Colors.RESET}")
    
    print(f"\n{Colors.CYAN}{Colors.BOLD}Funcionalidades:{Colors.RESET}\n"
          f"  {Colors.GREEN}✓{Colors.RESET} Tirar cartas aleatórias (Fisher-Yates shuffle)\n"
          f"  {Colors.GREEN}✓{Colors.RESET} Listar por naipe\n"
          f"  {Colors.GREEN}✓{Colors.RESET} Buscar cartas por nome\n"
          f"  {Colors.GREEN}✓{Colors.RESET} Layout responsivo (vertical e grid)\n"
          f"  {Colors.GREEN}✓{Colors.RESET} Cores ANSI por naipe\n"
          f"\n{Colors.CYAN}{Colors.BOLD}Versão:{Colors.RESET} {Colors.BOLD}2.0{Colors.RESET} │ "
          f"{Colors.CYAN}{Colors.BOLD}Python:{Colors.RESET} {Colors.BOLD}3.6+{Colors.RESET} │ "
          f"{Colors.CYAN}{Colors.BOLD}Deps:{Colors.RESET} {Colors.BOLD}Nenhuma{Colors.RESET}\n")
    
    input(f"{Colors.GRAY}Pressione ENTER para continuar...{Colors.RESET}")


def interactive_about():
    """Menu: Sobre"""
    clear_screen()
    print_banner()
    print_header("SOBRE O PROGRAMA")
    
    about = f"""
{Colors.CYAN}{Colors.BOLD}Tarô v2.0 - Terminal Edition{Colors.RESET}

Uma implementação moderna de um baralho de Tarô com suporte completo
para leitura interativa no terminal.

{Colors.CYAN}{Colors.BOLD}Desenvolvido com:{Colors.RESET}
  {Colors.GREEN}•{Colors.RESET} Python 3.6+ | ANSI codes | ASCII art | Algoritmos responsivos

{Colors.CYAN}{Colors.BOLD}Características:{Colors.RESET}
  {Colors.GREEN}•{Colors.RESET} 78 cartas completas (22 Maiores + 56 naipes)
  {Colors.GREEN}•{Colors.RESET} Layout 100% responsivo | Sem dependências externas
  {Colors.GREEN}•{Colors.RESET} Interface interativa estilo Metasploit
  {Colors.GREEN}•{Colors.RESET} Suporte para terminal e web

{Colors.CYAN}{Colors.BOLD}Autor:{Colors.RESET} Um Gordo | {Colors.CYAN}{Colors.BOLD}Data:{Colors.RESET} Dezembro 2024

{Colors.GRAY}Para usar via CLI: ./taro.py --cli --help{Colors.RESET}
"""
    
    print(about)
    input(f"{Colors.GRAY}Pressione ENTER para continuar...{Colors.RESET}")


def run_interactive(baralho: Baralho):
    """Loop da interface interativa"""
    while True:
        clear_screen()
        print_banner()
        print_menu()
        
        choice = print_prompt("Escolha uma opção")
        
        if choice == '1':
            interactive_tirar_cartas(baralho)
        elif choice == '2':
            interactive_listar_por_naipe(baralho)
        elif choice == '3':
            interactive_buscar_carta(baralho)
        elif choice == '4':
            interactive_demo(baralho)
        elif choice == '5':
            interactive_info(baralho)
        elif choice == '6':
            interactive_about()
        elif choice == '0':
            clear_screen()
            print_banner()
            print(f"\n{Colors.CYAN}[*] Encerrando...{Colors.RESET}\n{Colors.GREEN}✓{Colors.RESET} Obrigado por usar Tarô v2.0!\n{Colors.YELLOW}*{Colors.RESET} Até a próxima leitura...\n")
            sys.exit(0)
        else:
            print_error("Opção inválida!")
            time.sleep(1)


# ============================================================================
# CLI DIRETO (argparse)
# ============================================================================

def run_cli():
    """Interface CLI com argparse"""
    parser = argparse.ArgumentParser(
        description='🃏 Tarô v2.0 - Leitura interativa de cartas de tarot',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Exemplos: ./taro.py --cli --tirar 3  |  ./taro.py --cli --demo  |  ./taro.py --cli --search 'Mundo'"
    )

    parser.add_argument('-t', '--tirar', type=int, metavar='QTD', help='Tira N cartas aleatórias')
    parser.add_argument('-d', '--demo', action='store_true', help='Executa demo com 5 cartas')
    parser.add_argument('-l', '--listar', metavar='NAIPE', choices=['maiores', 'paus', 'copas', 'espadas', 'ouros'],
                        help='Lista cartas de um naipe específico')
    parser.add_argument('-s', '--search', metavar='NOME', help='Busca uma carta pelo nome')
    parser.add_argument('--layout', choices=['vert', 'grid'], default='vert', help='Layout: vert ou grid')
    parser.add_argument('-i', '--info', action='store_true', help='Mostra informações do baralho')

    args = parser.parse_args(sys.argv[2:])  # Pula "--cli"

    if len(sys.argv) == 2:  # Só --cli sem mais opções
        parser.print_help()
        sys.exit(0)

    baralho = Baralho()

    if args.tirar:
        if args.tirar < 1 or args.tirar > 78:
            print_error("Quantidade deve estar entre 1 e 78")
            sys.exit(1)
        cartas = baralho.tirar(args.tirar)
        output = render_cards_grid(cartas, requested_cards_per_row=3 if args.layout == 'grid' else 1, ignore_rows=True)
        print(output)

    elif args.demo:
        cartas = baralho.tirar(5)
        output = render_cards_grid(cartas, requested_cards_per_row=3, ignore_rows=True)
        print(output)
        print_success("Demonstração concluída!")

    elif args.listar:
        naipe_map = {'maiores': 'Maiores', 'paus': 'Paus', 'copas': 'Copas', 'espadas': 'Espadas', 'ouros': 'Ouros'}
        naipe_nome = naipe_map[args.listar]
        cartas = baralho.listar_por_naipe(naipe_nome)
        print(f"\n📚 Cartas de {naipe_nome.upper()} ({len(cartas)} cartas)\n")
        output = render_cards_grid(cartas, requested_cards_per_row=2, ignore_rows=True)
        print(output)

    elif args.search:
        carta = baralho.get_carta_por_nome(args.search)
        if not carta:
            search_lower = args.search.lower()
            matches = [c for c in baralho.cartas if search_lower in c.name.lower()]
            if matches:
                if len(matches) == 1:
                    carta = matches[0]
                else:
                    print(f"\n🔍 Encontradas {len(matches)} cartas com '{args.search}':\n")
                    for c in matches:
                        print(f"  • {c.name} ({c.suit})")
                    sys.exit(0)
        
        if carta:
            print(f"\n🔍 Carta encontrada: {carta.name}\n")
            output = render_cards_grid([carta], requested_cards_per_row=1, ignore_rows=True)
            print(output)
        else:
            print_error(f"Nenhuma carta encontrada com '{args.search}'")
            sys.exit(1)

    elif args.info:
        total = len(baralho.cartas)
        naipes = {}
        for carta in baralho.cartas:
            naipe = carta.suit
            naipes[naipe] = naipes.get(naipe, 0) + 1
        
        print(f"\n📊 INFORMAÇÕES DO BARALHO\n\nTotal de cartas: {total}\n")
        for naipe, qtd in sorted(naipes.items()):
            print(f"  • {naipe}: {qtd} cartas")
        print()


# ============================================================================
# DEMONSTRAÇÃO VISUAL
# ============================================================================

def run_demo_ui():
    """Demonstração visual"""
    print(f"""
{Colors.MAGENTA}{Colors.BOLD}
╔═══════════════════════════════════════════════════════════════════╗
║  ████████╗ █████╗ ██████╗ █████╗ ██╗   ██╗███████╗██╗  ██╗      ║
║  ╚══██╔══╝██╔══██╗██╔══██╗██╔══██╗██║   ██║██╔════╝╚██╗██╔╝      ║
║     ██║   ███████║██████╔╝███████║██║   ██║███████╗ ╚███╔╝       ║
║     ██║   ██╔══██║██╔══██╗██╔══██║██║   ██║╚════██║ ██╔██╗       ║
║     ██║   ██║  ██║██║  ██║██║  ██║╚██████╔╝███████║██╔╝ ██╗      ║
║     ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝      ║
║          Leitura Interativa de Cartas de Tarô - v2.0             ║
╚═══════════════════════════════════════════════════════════════════╝
{Colors.RESET}

{Colors.GREEN}[✓]{Colors.RESET} Interface Unificada
{Colors.GREEN}[✓]{Colors.RESET} Sem dependências externas
{Colors.GREEN}[✓]{Colors.RESET} 78 cartas completas
{Colors.GREEN}[✓]{Colors.RESET} Cores ANSI por naipe

{Colors.CYAN}Para usar:{Colors.RESET}
  ./taro.py              (Interface interativa - padrão)
  ./taro.py --cli --tirar 5  (CLI direto)
  ./taro.py --cli --help     (Ajuda CLI)
  ./taro.py --demo           (Demonstração visual)
""")


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Função principal"""
    if len(sys.argv) > 1:
        if sys.argv[1] == '--cli':
            run_cli()
        elif sys.argv[1] == '--demo':
            run_demo_ui()
        else:
            print(f"{Colors.RED}[!]{Colors.RESET} Argumento desconhecido: {sys.argv[1]}")
            print(f"{Colors.YELLOW}[*]{Colors.RESET} Use: ./taro.py [--cli [opções] | --demo]")
            sys.exit(1)
    else:
        baralho = Baralho()
        try:
            run_interactive(baralho)
        except KeyboardInterrupt:
            clear_screen()
            print_banner()
            print(f"\n{Colors.RED}[!] Programa interrompido pelo usuário{Colors.RESET}\n{Colors.YELLOW}*{Colors.RESET} Até a próxima...\n")
            sys.exit(0)


if __name__ == '__main__':
    main()
