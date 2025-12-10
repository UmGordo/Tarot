# Análise de Tiragens com IA Local

## O que é?

Este módulo permite analisar múltiplas tiragens de Tarô usando uma IA rodando **localmente no seu computador** (100% privado, 100% grátis).

## Como Funciona

```
Seu PC/Mac
    ↓
[Ollama - Servidor IA] ← Roda aqui
    ↓
[Seu Script Python] ← Você executa
    ↓
[Análise de Cartas] ← Resultado em texto
```

## Instalação (5 minutos)

### Passo 1: Instalar Ollama

**macOS/Linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

**Windows:**
- Baixar em: https://ollama.ai/download/windows

**Verificar instalação:**
```bash
ollama --version
```

### Passo 2: Baixar Modelo IA

Escolha um (recomendado: **mistral** para melhor custo-benefício):

```bash
# Mistral 7B (recomendado) - 4GB
ollama pull mistral

# OU Llama2 13B - mais poderoso - 7GB
ollama pull llama2

# OU Neural Chat - rápido - 3.8GB
ollama pull neural-chat
```

### Passo 3: Iniciar Servidor

```bash
ollama serve
```

Você verá:
```
Listening on 127.0.0.1:11434
```

**Deixe rodando em um terminal separado!**

### Passo 4: Executar Análises

Em outro terminal:

```bash
cd /workspaces/Tarot/v2

# Exemplo simples: 5 tiragens sobre relacionamento
python3 analise_llm.py --assunto "relacionamento" --num-tiragens 5

# Exemplo completo: 20 tiragens com 5 cartas cada
python3 analise_llm.py --assunto "carreira" --num-tiragens 20 --cartas 5 --salvar

# Usar modelo diferente
python3 analise_llm.py --assunto "finanças" --modelo llama2 --num-tiragens 10
```

## Exemplos de Saída

```
============================================================
ANÁLISE DE 5 TIRAGENS SOBRE: relacionamento
============================================================

[1/5] Tirando cartas...
  Cartas: O Mago, Ás de Copas, Dois de Copas
  ✓ Análise concluída

[2/5] Tirando cartas...
  Cartas: Os Enamorados, Rainha de Copas, Dez de Copas
  ✓ Análise concluída

...

[ANÁLISE 1]
Você é um expert em Tarô...
(análise detalhada da IA aqui)

[ANÁLISE 2]
...

============================================================
SÍNTESE DE PADRÕES (baseado nas 5 tiragens)
============================================================

Cartas mais frequentes:
- Copas (xx vezes) - amor, emoções
- Enamorados (xxx vezes) - escolha, harmonia
...
```

## Specs Hardware

| Modelo | RAM | GPU | Velocidade |
|--------|-----|-----|-----------|
| Neural Chat (3.8GB) | 4GB | Não precisa | 50ms |
| Mistral (4GB) | 6GB | Não precisa | 100ms |
| Llama2 (7GB) | 8GB | Recomendado | 200ms |
| GPT-4 (Nuvem) | N/A | GPU Cloud | 1s |

## Custos

| Solução | Custo | Privacidade |
|---------|-------|------------|
| **Ollama Local** | **$0** | ✅ Privado |
| **LM Studio** | **$0** | ✅ Privado |
| **Groq API** | **$0** | ❌ Nuvem |
| **OpenAI API** | $0.002/1K tokens | ❌ Nuvem |

## FAQ

**P: Posso usar offline?**
R: Sim! Uma vez baixado o modelo, funciona 100% offline.

**P: Qual modelo é melhor?**
R: Mistral tem melhor equilíbrio. Llama2 é mais poderoso mas mais lento.

**P: Quanto tempo leva analisar 100 tiragens?**
R: ~10-20 minutos (depende do modelo e do seu PC).

**P: Preciso de GPU?**
R: Não, mas ajuda muito. CPU é suficiente.

**P: Os dados são seguros?**
R: Sim, fica no seu PC, ninguém acessa.

## Troubleshooting

**Erro: "Ollama não está rodando"**
```bash
# Em outro terminal:
ollama serve
```

**Erro: "Modelo não encontrado"**
```bash
ollama pull mistral
```

**Resposta muito lenta?**
- Use `neural-chat` (mais rápido)
- Ou instale GPU drivers para acelerar

## Próximos Passos

1. Instalar Ollama (5 min)
2. Baixar um modelo (5 min)
3. Rodar análises
4. Encontrar padrões nas tiragens!

## Uso Avançado

```python
from analise_llm import AnalisadorTaroLLM

# Criar analisador
analisador = AnalisadorTaroLLM(modelo="mistral")

# Tirar cartas
cartas = analisador.tirar_cartas(3)

# Analisar
analise = analisador.analisar_cartas("seu assunto", cartas)

# Salvar
analisador.salvar_relatorio(resultado, "meu_relatorio.json")
```

---

**Dúvidas?** Consulte: https://ollama.ai
