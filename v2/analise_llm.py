#!/usr/bin/env python3
"""
Análise de Tiragens de Tarô com LLM Local (Ollama)

USO:
1. Instalar Ollama: https://ollama.ai
2. Baixar modelo: ollama pull mistral
3. Iniciar servidor: ollama serve
4. Rodar este script: python3 analise_llm.py

EXEMPLO:
    python3 analise_llm.py --assunto "relacionamento amoroso" --num-tiragens 5
    python3 analise_llm.py --assunto "carreira" --num-tiragens 10 --modelo llama2
"""

import sys
import os
import json
import argparse
import requests
from typing import List, Dict, Any

sys.path.insert(0, os.path.dirname(__file__))
from baralho import Baralho

# Configuração do Ollama
OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_TIMEOUT = 300  # 5 minutos para respostas longas


class AnalisadorTaroLLM:
    def __init__(self, modelo: str = "mistral"):
        """Inicializa analisador com modelo Ollama especificado"""
        self.modelo = modelo
        self.baralho = Baralho()
        self.url_generate = f"{OLLAMA_BASE_URL}/api/generate"
        self.verificar_disponibilidade()

    def verificar_disponibilidade(self):
        """Verifica se Ollama está rodando"""
        try:
            response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
            if response.status_code == 200:
                print(f"✓ Ollama disponível")
                modelos = response.json().get("models", [])
                nomes = [m.get("name", "").split(":")[0] for m in modelos]
                print(f"  Modelos instalados: {', '.join(set(nomes))}")
                
                if self.modelo not in nomes:
                    print(f"⚠ Modelo '{self.modelo}' não encontrado!")
                    print(f"  Execute: ollama pull {self.modelo}")
                    sys.exit(1)
            else:
                raise Exception("Ollama não respondeu")
        except requests.exceptions.ConnectionError:
            print("✗ Erro: Ollama não está rodando!")
            print("  Execute em outro terminal: ollama serve")
            sys.exit(1)

    def tirar_cartas(self, quantidade: int) -> List[Dict[str, Any]]:
        """Tira cartas aleatoriamente do baralho"""
        import random
        cartas_disponiveis = self.baralho.cartas.copy()
        random.shuffle(cartas_disponiveis)
        return [
            {
                "nome": c.name,
                "naipe": c.suit,
                "numero": c.number,
                "descricao": c.description
            }
            for c in cartas_disponiveis[:quantidade]
        ]

    def formatar_cartas(self, cartas: List[Dict[str, Any]]) -> str:
        """Formata cartas para apresentação textual"""
        texto = ""
        for i, carta in enumerate(cartas, 1):
            texto += f"\n{i}. {carta['nome']} ({carta['naipe']})"
            texto += f"\n   → {carta['descricao']}"
        return texto

    def gerar_prompt(self, assunto: str, cartas: List[Dict[str, Any]]) -> str:
        """Gera prompt para análise das cartas"""
        cartas_formatadas = self.formatar_cartas(cartas)
        
        prompt = f"""Você é um expert em Tarô com 20 anos de experiência. 
Analise as seguintes cartas em relação ao assunto especificado:

ASSUNTO: {assunto}

CARTAS TIRADAS:
{cartas_formatadas}

ANÁLISE SOLICITADA:
1. Interpretação de cada carta no contexto do assunto
2. Significado combinado das cartas (sinergias)
3. Mensagem principal (em 1-2 frases)
4. Recomendação/insight prático

Seja conciso mas profundo na análise. Foque em insights práticos."""

        return prompt

    def analisar_cartas(self, assunto: str, cartas: List[Dict[str, Any]]) -> str:
        """Envia prompt para Ollama e retorna análise"""
        prompt = self.gerar_prompt(assunto, cartas)
        
        print(f"\n⏳ Analisando com {self.modelo}...")
        
        try:
            response = requests.post(
                self.url_generate,
                json={
                    "model": self.modelo,
                    "prompt": prompt,
                    "stream": False,
                    "temperature": 0.7,
                    "num_predict": 500,  # máximo 500 tokens
                },
                timeout=OLLAMA_TIMEOUT
            )
            
            if response.status_code == 200:
                resultado = response.json()
                return resultado.get("response", "Erro ao gerar resposta")
            else:
                return f"Erro: {response.status_code} - {response.text}"
                
        except requests.exceptions.Timeout:
            return "Erro: Timeout (resposta muito lenta)"
        except Exception as e:
            return f"Erro: {str(e)}"

    def processar_multiplas_tiragens(
        self,
        assunto: str,
        num_tiragens: int,
        cartas_por_tiragem: int = 3
    ) -> Dict[str, Any]:
        """Processa múltiplas tiragens e resume padrões"""
        print(f"\n{'='*60}")
        print(f"ANÁLISE DE {num_tiragens} TIRAGENS SOBRE: {assunto}")
        print(f"{'='*60}\n")
        
        tiragens = []
        analises = []
        
        for i in range(num_tiragens):
            print(f"[{i+1}/{num_tiragens}] Tirando cartas...")
            cartas = self.tirar_cartas(cartas_por_tiragem)
            
            print(f"  Cartas: {', '.join(c['nome'] for c in cartas)}")
            analise = self.analisar_cartas(assunto, cartas)
            
            tiragens.append(cartas)
            analises.append(analise)
            print(f"  ✓ Análise concluída\n")
        
        # Síntese das múltiplas tiragens
        print(f"\n{'='*60}")
        print(f"SÍNTESE DE PADRÕES (baseado nas {num_tiragens} tiragens)")
        print(f"{'='*60}\n")
        
        sintese_prompt = self._gerar_prompt_sintese(assunto, tiragens, analises)
        sintese = self.analisar_cartas(assunto, [])  # dummy
        
        return {
            "assunto": assunto,
            "num_tiragens": num_tiragens,
            "tiragens": tiragens,
            "analises": analises,
            "sintese": self._gerar_sintese(assunto, analises)
        }

    def _gerar_prompt_sintese(
        self,
        assunto: str,
        tiragens: List[List[Dict]],
        analises: List[str]
    ) -> str:
        """Cria prompt para síntese de múltiplas tiragens"""
        cartas_unicas = {}
        for tiragem in tiragens:
            for carta in tiragem:
                nome = carta["nome"]
                cartas_unicas[nome] = cartas_unicas.get(nome, 0) + 1
        
        cartas_frequentes = sorted(
            cartas_unicas.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]
        
        prompt = f"""Dado que você analisou {len(tiragens)} tiragens diferentes sobre "{assunto}",
        
Cartas mais frequentes: {', '.join(f'{c[0]} ({c[1]}x)' for c in cartas_frequentes)}

Qual é o padrão ou mensagem geral que emerge dessas múltiplas tiragens?
Qual é o tema subjacente? Qual é a recomendação mais forte?

Seja direto e prático."""
        
        return prompt

    def _gerar_sintese(self, assunto: str, analises: List[str]) -> str:
        """Gera resumo simples das análises"""
        # Implementação simples: combina as análises
        return f"\n\nAnálises Individuais:\n" + "\n---\n".join(analises)

    def salvar_relatorio(self, resultado: Dict[str, Any], arquivo: str = None):
        """Salva relatório em JSON"""
        if arquivo is None:
            assunto_clean = resultado["assunto"].replace(" ", "_")
            arquivo = f"analise_{assunto_clean}.json"
        
        with open(arquivo, "w", encoding="utf-8") as f:
            json.dump(resultado, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ Relatório salvo em: {arquivo}")


def main():
    parser = argparse.ArgumentParser(
        description="Análise de Tiragens de Tarô com IA Local",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
EXEMPLOS:
  python3 analise_llm.py --assunto "relacionamento" --num-tiragens 5
  python3 analise_llm.py --assunto "carreira" --num-tiragens 10 --modelo llama2
  python3 analise_llm.py --assunto "finanças" --cartas 5 --num-tiragens 20
        """
    )
    
    parser.add_argument(
        "--assunto",
        required=True,
        help="Assunto para análise (ex: 'relacionamento', 'carreira')"
    )
    parser.add_argument(
        "--num-tiragens",
        type=int,
        default=5,
        help="Número de tiragens a fazer (padrão: 5)"
    )
    parser.add_argument(
        "--cartas",
        type=int,
        default=3,
        help="Número de cartas por tiragem (padrão: 3)"
    )
    parser.add_argument(
        "--modelo",
        default="mistral",
        help="Modelo Ollama a usar (padrão: mistral)"
    )
    parser.add_argument(
        "--salvar",
        action="store_true",
        help="Salvar relatório em JSON"
    )
    parser.add_argument(
        "--arquivo",
        help="Arquivo para salvar relatório (padrão: analise_<assunto>.json)"
    )
    
    args = parser.parse_args()
    
    # Executar análise
    analisador = AnalisadorTaroLLM(modelo=args.modelo)
    resultado = analisador.processar_multiplas_tiragens(
        assunto=args.assunto,
        num_tiragens=args.num_tiragens,
        cartas_por_tiragem=args.cartas
    )
    
    if args.salvar:
        analisador.salvar_relatorio(resultado, args.arquivo)
    
    print("\n✓ Análise concluída!")


if __name__ == "__main__":
    main()
