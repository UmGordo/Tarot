#!/usr/bin/env python3
"""
Análise de Tiragens de Tarô com múltiplas backends:
- Ollama (local, gratuito, privado)
- Groq (nuvem, gratuito, ultra-rápido)

USO:
    # Local (Ollama)
    python3 analise_llm_flex.py --assunto "relacionamento" --backend ollama --num-tiragens 5
    
    # Nuvem (Groq - mais rápido, mas dados vão pra nuvem)
    python3 analise_llm_flex.py --assunto "carreira" --backend groq --num-tiragens 10
    
    # Com relatório
    python3 analise_llm_flex.py --assunto "finanças" --backend ollama --num-tiragens 20 --salvar
"""

import sys
import os
import json
import argparse
import requests
from typing import List, Dict, Any
from abc import ABC, abstractmethod

sys.path.insert(0, os.path.dirname(__file__))
from baralho import Baralho


class BackendLLM(ABC):
    """Interface abstrata para diferentes backends de LLM"""
    
    @abstractmethod
    def verificar_disponibilidade(self):
        pass
    
    @abstractmethod
    def analisar(self, prompt: str) -> str:
        pass


class OllamaBackend(BackendLLM):
    """Backend local usando Ollama"""
    
    OLLAMA_BASE_URL = "http://localhost:11434"
    OLLAMA_TIMEOUT = 300
    
    def __init__(self, modelo: str = "mistral"):
        self.modelo = modelo
        self.url_generate = f"{self.OLLAMA_BASE_URL}/api/generate"
        self.verificar_disponibilidade()
    
    def verificar_disponibilidade(self):
        """Verifica se Ollama está rodando"""
        try:
            response = requests.get(f"{self.OLLAMA_BASE_URL}/api/tags", timeout=5)
            if response.status_code == 200:
                print(f"✓ Ollama disponível na porta 11434")
                modelos = response.json().get("models", [])
                nomes = [m.get("name", "").split(":")[0] for m in modelos]
                print(f"  Modelos: {', '.join(set(nomes))}")
                
                if self.modelo not in nomes:
                    print(f"⚠ Modelo '{self.modelo}' não encontrado!")
                    print(f"  Execute: ollama pull {self.modelo}")
                    sys.exit(1)
            else:
                raise Exception("Ollama não respondeu")
        except requests.exceptions.ConnectionError:
            print("✗ Ollama não está rodando!")
            print("  Execute em outro terminal: ollama serve")
            sys.exit(1)
    
    def analisar(self, prompt: str) -> str:
        """Envia prompt para Ollama"""
        try:
            response = requests.post(
                self.url_generate,
                json={
                    "model": self.modelo,
                    "prompt": prompt,
                    "stream": False,
                    "temperature": 0.7,
                    "num_predict": 500,
                },
                timeout=self.OLLAMA_TIMEOUT
            )
            
            if response.status_code == 200:
                return response.json().get("response", "Erro ao gerar resposta")
            else:
                return f"Erro Ollama: {response.status_code}"
        except Exception as e:
            return f"Erro: {str(e)}"


class GroqBackend(BackendLLM):
    """Backend nuvem usando Groq (GRATUITO, ultra-rápido)"""
    
    def __init__(self, api_key: str = None, modelo: str = "mixtral-8x7b-32768"):
        self.modelo = modelo
        self.api_key = api_key or os.environ.get("GROQ_API_KEY")
        self.url = "https://api.groq.com/openai/v1/chat/completions"
        self.verificar_disponibilidade()
    
    def verificar_disponibilidade(self):
        """Verifica se chave Groq está disponível"""
        if not self.api_key:
            print("⚠ GROQ_API_KEY não encontrada!")
            print("\nPara usar Groq:")
            print("1. Crie conta em: https://console.groq.com")
            print("2. Copie sua API key")
            print("3. Execute: export GROQ_API_KEY='sua-chave-aqui'")
            print("\nOU use Ollama (local, gratuito):")
            print("  python3 analise_llm_flex.py --backend ollama --assunto 'seu assunto'")
            sys.exit(1)
        
        print(f"✓ Groq disponível (ultra-rápido, nuvem)")
        print(f"  Modelo: {self.modelo}")
        print(f"  ⚠ Nota: Dados são enviados para nuvem Groq")
    
    def analisar(self, prompt: str) -> str:
        """Envia prompt para Groq API"""
        try:
            response = requests.post(
                self.url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.modelo,
                    "messages": [
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.7,
                    "max_tokens": 500,
                },
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
            else:
                return f"Erro Groq: {response.status_code}"
        except Exception as e:
            return f"Erro: {str(e)}"


class AnalisadorTaroLLM:
    """Analisador principal com suporte a múltiplos backends"""
    
    def __init__(self, backend: BackendLLM):
        self.backend = backend
        self.baralho = Baralho()
    
    def tirar_cartas(self, quantidade: int) -> List[Dict[str, Any]]:
        """Tira cartas aleatoriamente"""
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
        """Formata cartas para apresentação"""
        texto = ""
        for i, carta in enumerate(cartas, 1):
            texto += f"\n{i}. {carta['nome']} ({carta['naipe']})"
            texto += f"\n   → {carta['descricao']}"
        return texto
    
    def gerar_prompt(self, assunto: str, cartas: List[Dict[str, Any]]) -> str:
        """Gera prompt para análise"""
        cartas_formatadas = self.formatar_cartas(cartas)
        
        return f"""Você é um expert em Tarô com 20 anos de experiência.
Analise as cartas em relação ao assunto especificado:

ASSUNTO: {assunto}

CARTAS TIRADAS:
{cartas_formatadas}

ANÁLISE:
1. Interpretação de cada carta
2. Sinergias entre as cartas
3. Mensagem principal (1-2 frases)
4. Recomendação prática

Seja conciso mas profundo."""
    
    def analisar_cartas(self, assunto: str, cartas: List[Dict[str, Any]]) -> str:
        """Analisa cartas usando o backend"""
        prompt = self.gerar_prompt(assunto, cartas)
        print(f"⏳ Analisando...")
        return self.backend.analisar(prompt)
    
    def processar_multiplas_tiragens(
        self,
        assunto: str,
        num_tiragens: int,
        cartas_por_tiragem: int = 3
    ) -> Dict[str, Any]:
        """Processa múltiplas tiragens"""
        print(f"\n{'='*70}")
        print(f"ANÁLISE DE {num_tiragens} TIRAGENS SOBRE: {assunto}")
        print(f"{'='*70}\n")
        
        tiragens = []
        analises = []
        
        for i in range(num_tiragens):
            print(f"[{i+1}/{num_tiragens}] Tirando cartas...")
            cartas = self.tirar_cartas(cartas_por_tiragem)
            
            print(f"  Cartas: {', '.join(c['nome'] for c in cartas)}")
            analise = self.analisar_cartas(assunto, cartas)
            
            tiragens.append(cartas)
            analises.append(analise)
            print(f"  ✓ Pronta\n")
        
        return {
            "assunto": assunto,
            "num_tiragens": num_tiragens,
            "tiragens": tiragens,
            "analises": analises,
        }
    
    def salvar_relatorio(self, resultado: Dict[str, Any], arquivo: str = None):
        """Salva relatório em JSON"""
        if arquivo is None:
            assunto_clean = resultado["assunto"].replace(" ", "_")
            arquivo = f"analise_{assunto_clean}.json"
        
        with open(arquivo, "w", encoding="utf-8") as f:
            json.dump(resultado, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ Relatório salvo: {arquivo}")


def main():
    parser = argparse.ArgumentParser(
        description="Análise de Tiragens com IA (Local ou Nuvem)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
EXEMPLOS:

  # Usar Ollama (local, gratuito, privado)
  python3 analise_llm_flex.py --backend ollama --assunto "relacionamento" --num-tiragens 5

  # Usar Groq (nuvem, gratuito, ultra-rápido - precisa API key)
  export GROQ_API_KEY='sua-chave-aqui'
  python3 analise_llm_flex.py --backend groq --assunto "carreira" --num-tiragens 10

  # Com relatório
  python3 analise_llm_flex.py --backend ollama --assunto "finanças" --num-tiragens 20 --salvar
        """
    )
    
    parser.add_argument(
        "--backend",
        choices=["ollama", "groq"],
        default="ollama",
        help="Backend a usar (padrão: ollama - local e gratuito)"
    )
    parser.add_argument(
        "--assunto",
        required=True,
        help="Assunto para análise"
    )
    parser.add_argument(
        "--num-tiragens",
        type=int,
        default=5,
        help="Número de tiragens (padrão: 5)"
    )
    parser.add_argument(
        "--cartas",
        type=int,
        default=3,
        help="Cartas por tiragem (padrão: 3)"
    )
    parser.add_argument(
        "--modelo",
        default=None,
        help="Modelo específico (Ollama: mistral, llama2, etc | Groq: mixtral-8x7b-32768)"
    )
    parser.add_argument(
        "--salvar",
        action="store_true",
        help="Salvar relatório em JSON"
    )
    parser.add_argument(
        "--arquivo",
        help="Arquivo para relatório"
    )
    
    args = parser.parse_args()
    
    # Criar backend apropriado
    if args.backend == "ollama":
        modelo = args.modelo or "mistral"
        backend = OllamaBackend(modelo=modelo)
    else:  # groq
        modelo = args.modelo or "mixtral-8x7b-32768"
        backend = GroqBackend(modelo=modelo)
    
    # Executar análise
    analisador = AnalisadorTaroLLM(backend)
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
