#!/usr/bin/env python3
"""
Análise de Tiragens de Tarô com LLM (Ollama ou Groq)

USO - OLLAMA (Local, 100% Gratuito):
1. Instalar Ollama: https://ollama.ai
2. Baixar modelo: ollama pull mistral
3. Iniciar servidor: ollama serve
4. Rodar script: python3 analise_llm.py --assunto "seu assunto"

USO - GROQ (Nuvem, 100% Gratuito, 10x mais rápido):
1. Criar conta gratuita: https://console.groq.com
2. Copiar API Key
3. Exportar: export GROQ_API_KEY='sua-chave-aqui'
4. Rodar script: python3 analise_llm.py --assunto "seu assunto" --backend groq

EXEMPLOS:
    # Ollama (local, privado, sem internet)
    python3 analise_llm.py --assunto "relacionamento" --num-tiragens 5
    
    # Groq (nuvem, ultra-rápido, 10x mais rápido)
    python3 analise_llm.py --assunto "carreira" --num-tiragens 10 --backend groq
    
    # Com relatório
    python3 analise_llm.py --assunto "finanças" --num-tiragens 20 --salvar
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

# Configuração do Ollama
OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_TIMEOUT = 300  # 5 minutos para respostas longas

# Configuração do Groq
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "mixtral-8x7b-32768"  # Modelo mais rápido do Groq


class BackendLLM(ABC):
    """Interface abstrata para diferentes backends de LLM"""
    
    @abstractmethod
    def verificar_disponibilidade(self):
        """Verifica se o backend está disponível"""
        pass
    
    @abstractmethod
    def analisar(self, prompt: str) -> str:
        """Envia prompt e retorna análise"""
        pass


class OllamaBackend(BackendLLM):
    """Backend local usando Ollama"""
    
    def __init__(self, modelo: str = "mistral"):
        self.modelo = modelo
        self.url_generate = f"{OLLAMA_BASE_URL}/api/generate"
        self.verificar_disponibilidade()
    
    def verificar_disponibilidade(self):
        """Verifica se Ollama está rodando"""
        try:
            response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
            if response.status_code == 200:
                print(f"✓ Ollama disponível (local, privado)")
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
            print("✗ Erro: Ollama não está rodando!")
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
                timeout=OLLAMA_TIMEOUT
            )
            
            if response.status_code == 200:
                return response.json().get("response", "Erro ao gerar resposta")
            else:
                return f"Erro Ollama: {response.status_code}"
        except requests.exceptions.Timeout:
            return "Erro: Timeout (resposta muito lenta)"
        except Exception as e:
            return f"Erro: {str(e)}"


class GroqBackend(BackendLLM):
    """Backend nuvem usando Groq (GRATUITO, ultra-rápido)"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get("GROQ_API_KEY")
        self.modelo = GROQ_MODEL
        self.verificar_disponibilidade()
    
    def verificar_disponibilidade(self):
        """Verifica se API key do Groq está disponível"""
        if not self.api_key:
            print("⚠ GROQ_API_KEY não encontrada!")
            print("\nPara usar Groq (nuvem, 10x mais rápido):")
            print("1. Crie conta gratuita em: https://console.groq.com")
            print("2. Copie sua API Key")
            print("3. Execute: export GROQ_API_KEY='sua-chave-aqui'")
            print("\nOU use Ollama (local, 100% privado):")
            print("  python3 analise_llm.py --assunto 'seu assunto'")
            sys.exit(1)
        
        print(f"✓ Groq disponível (nuvem, ultra-rápido)")
        print(f"  Modelo: {self.modelo}")
        print(f"  ⚠ Nota: Dados são enviados para nuvem Groq")
    
    def analisar(self, prompt: str) -> str:
        """Envia prompt para Groq API"""
        try:
            response = requests.post(
                GROQ_API_URL,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.modelo,
                    "messages": [
                        {"role": "system", "content": "Você é um expert em Tarô com 20 anos de experiência."},
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
                error = response.json().get("error", {})
                return f"Erro Groq: {error.get('message', response.status_code)}"
        except Exception as e:
            return f"Erro: {str(e)}"


class AnalisadorTaroLLM:
    def __init__(self, backend: BackendLLM):
        """Inicializa analisador com um backend LLM"""
        self.backend = backend
        self.baralho = Baralho()

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
        
        prompt = f"""Analise as seguintes cartas em relação ao assunto especificado:

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
        """Envia prompt para backend e retorna análise"""
        prompt = self.gerar_prompt(assunto, cartas)
        
        print(f"⏳ Analisando...")
        resultado = self.backend.analisar(prompt)
        return resultado

    def processar_multiplas_tiragens(
        self,
        assunto: str,
        num_tiragens: int,
        cartas_por_tiragem: int = 3
    ) -> Dict[str, Any]:
        """Processa múltiplas tiragens e resume padrões"""
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
            print(f"  ✓ Análise concluída\n")
        
        # Calcular cartas frequentes
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
        
        return {
            "assunto": assunto,
            "num_tiragens": num_tiragens,
            "cartas_por_tiragem": cartas_por_tiragem,
            "tiragens": tiragens,
            "analises": analises,
            "cartas_frequentes": dict(cartas_frequentes),
        }

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
        description="Análise de Tiragens de Tarô com IA (Local ou Nuvem)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
EXEMPLOS DE USO:

  Local (Ollama - 100% privado, sem internet obrigatório):
    python3 analise_llm.py --assunto "relacionamento" --num-tiragens 5
    python3 analise_llm.py --assunto "carreira" --num-tiragens 100 --salvar

  Nuvem (Groq - 10x mais rápido, requer API key gratuita):
    export GROQ_API_KEY='sua-chave-aqui'
    python3 analise_llm.py --assunto "finanças" --backend groq --num-tiragens 20
    
COMPARAÇÃO:
  Ollama  → $0, 100% privado, 50-200ms/análise
  Groq    → $0, nuvem, 10-50ms/análise (10x mais rápido)
        """
    )
    
    parser.add_argument(
        "--backend",
        choices=["ollama", "groq"],
        default="ollama",
        help="Backend a usar: 'ollama' (local, padrão) ou 'groq' (nuvem)"
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
        help="Modelo para Ollama (padrão: mistral). Ignorado para Groq"
    )
    parser.add_argument(
        "--salvar",
        action="store_true",
        help="Salvar relatório em JSON"
    )
    parser.add_argument(
        "--arquivo",
        help="Nome do arquivo para relatório (padrão: analise_<assunto>.json)"
    )
    
    args = parser.parse_args()
    
    # Criar backend apropriado
    print(f"\n{'='*70}")
    if args.backend == "ollama":
        backend = OllamaBackend(modelo=args.modelo)
    else:  # groq
        backend = GroqBackend()
    print(f"{'='*70}\n")
    
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
