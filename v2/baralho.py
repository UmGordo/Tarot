"""
Baralho completo de Tarô (78 cartas).
Contém 22 Arcanos Maiores + 56 cartas dos quatro naipes.
Cada carta tem nome, naipe, número e descrição resumida.
"""

from card_model import Card
import random


class Baralho:
    """Baralho de Tarô completo com 78 cartas."""

    def __init__(self):
        self.cartas = self._criar_cartas()

    def _criar_cartas(self):
        """Cria todas as 78 cartas do baralho."""
        cartas = []

        # Arcanos Maiores (22)
        maiores = [
            (0, 'O Louco', 'Começo, espontaneidade, inocência'),
            (1, 'O Mago', 'Poder, criatividade, habilidade'),
            (2, 'A Sacerdotisa', 'Intuição, sabedoria, misterio'),
            (3, 'A Imperatriz', 'Fertilidade, abundância, criação'),
            (4, 'O Imperador', 'Autoridade, estrutura, controle'),
            (5, 'O Hierofante', 'Tradição, espiritualidade, conformidade'),
            (6, 'Os Enamorados', 'Amor, escolha, harmonia'),
            (7, 'O Carro', 'Determinação, movimento, vitória'),
            (8, 'A Justiça', 'Equilíbrio, verdade, responsabilidade'),
            (9, 'O Eremita', 'Introspecção, busca interna, solitude'),
            (10, 'A Roda da Fortuna', 'Ciclos, destino, mudança'),
            (11, 'A Força', 'Coragem, paciência, controle interno'),
            (12, 'O Enforcado', 'Renúncia, suspensão, nova perspectiva'),
            (13, 'A Morte', 'Transformação, fim, recomeço'),
            (14, 'A Temperança', 'Equilíbrio, modulação, cura'),
            (15, 'O Diabo', 'Limitações, escravidão, tentação'),
            (16, 'A Torre', 'Destruição, revelação, libertação'),
            (17, 'A Estrela', 'Esperança, inspiração, clareza'),
            (18, 'A Lua', 'Ilusão, medo, subconsciente'),
            (19, 'O Sol', 'Sucesso, vitalidade, alegria'),
            (20, 'O Julgamento', 'Despertar, chamado, ressurreição'),
            (21, 'O Mundo', 'Conclusão, completude, viagem'),
        ]

        for num, nome, desc in maiores:
            cartas.append(Card(nome, 'Maiores', num, '★', desc))

        # Paus (14)
        paus = [
            (1, 'Ás de Paus', 'Nova energia, inspiração, potencial'),
            (2, 'Dois de Paus', 'Planejamento, parceria, decisão'),
            (3, 'Três de Paus', 'Progresso, exploração, crescimento'),
            (4, 'Quatro de Paus', 'Celebração, comunidade, harmonia'),
            (5, 'Cinco de Paus', 'Conflito, competição, tensão'),
            (6, 'Seis de Paus', 'Sucesso, reconhecimento, liderança'),
            (7, 'Sete de Paus', 'Defesa, perseverança, coragem'),
            (8, 'Oito de Paus', 'Movimento, velocidade, progressão'),
            (9, 'Nove de Paus', 'Resiliência, resistência, força'),
            (10, 'Dez de Paus', 'Peso, responsabilidade, ônus'),
            (11, 'Pajem de Paus', 'Exploração, criatividade, juventude'),
            (12, 'Cavaleiro de Paus', 'Paixão, energia, movimento'),
            (13, 'Rainha de Paus', 'Aquecimento, hospitalidade, sensualidade'),
            (14, 'Rei de Paus', 'Liderança, visão, inspiração'),
        ]

        for num, nome, desc in paus:
            cartas.append(Card(nome, 'Paus', num, '✦', desc))

        # Copas (14)
        copas = [
            (1, 'Ás de Copas', 'Amor, novas emoções, inspiração'),
            (2, 'Dois de Copas', 'Parceria, amor, conexão'),
            (3, 'Três de Copas', 'Celebração, amizade, comunidade'),
            (4, 'Quatro de Copas', 'Apátia, desinteresse, dissatisfação'),
            (5, 'Cinco de Copas', 'Perda, arrependimento, tristeza'),
            (6, 'Seis de Copas', 'Inocência, nostalgia, generosidade'),
            (7, 'Sete de Copas', 'Ilusão, escolha, oportunidade'),
            (8, 'Oito de Copas', 'Abandono, busca, desengano'),
            (9, 'Nove de Copas', 'Satisfação, desejo realizado, alegria'),
            (10, 'Dez de Copas', 'Harmonia, família, felicidade'),
            (11, 'Pajem de Copas', 'Intuição, sensibilidade, juventude'),
            (12, 'Cavaleiro de Copas', 'Romance, idealismo, encanto'),
            (13, 'Rainha de Copas', 'Compaixão, empatia, intuição'),
            (14, 'Rei de Copas', 'Sabedoria emocional, compaixão, controle'),
        ]

        for num, nome, desc in copas:
            cartas.append(Card(nome, 'Copas', num, '♡', desc))

        # Espadas (14)
        espadas = [
            (1, 'Ás de Espadas', 'Verdade, clareza, nova ideia'),
            (2, 'Dois de Espadas', 'Impasse, indecisão, equilíbrio'),
            (3, 'Três de Espadas', 'Mágoa, sorrow, sofrimento'),
            (4, 'Quatro de Espadas', 'Descanso, pausa, contemplação'),
            (5, 'Cinco de Espadas', 'Derrota, conflito, perda'),
            (6, 'Seis de Espadas', 'Transição, jornada, movimento'),
            (7, 'Sete de Espadas', 'Furtividade, engano, estratégia'),
            (8, 'Oito de Espadas', 'Restrição, aprisionamento, confusão'),
            (9, 'Nove de Espadas', 'Ansiedade, medo, insônia'),
            (10, 'Dez de Espadas', 'Defeito, finalidade, limite'),
            (11, 'Pajem de Espadas', 'Observação, vigilância, escuta'),
            (12, 'Cavaleiro de Espadas', 'Confrontação, movimento, conflito'),
            (13, 'Rainha de Espadas', 'Clareza, lógica, independência'),
            (14, 'Rei de Espadas', 'Poder intelectual, autoridade, verdade'),
        ]

        for num, nome, desc in espadas:
            cartas.append(Card(nome, 'Espadas', num, '♠', desc))

        # Ouros (14)
        ouros = [
            (1, 'Ás de Ouros', 'Prosperidade, oportunidade, riqueza'),
            (2, 'Dois de Ouros', 'Equilíbrio, adaptação, flexibilidade'),
            (3, 'Três de Ouros', 'Trabalho em equipe, craft, maestria'),
            (4, 'Quatro de Ouros', 'Conservação, segurança, possessão'),
            (5, 'Cinco de Ouros', 'Dificuldade financeira, ansiedade, isolamento'),
            (6, 'Seis de Ouros', 'Generosidade, caridade, compartilhamento'),
            (7, 'Sete de Ouros', 'Avaliação, reflexão, reavaliação'),
            (8, 'Oito de Ouros', 'Aprendizado, mestria, desenvolvimento'),
            (9, 'Nove de Ouros', 'Luxo, independência, conforto'),
            (10, 'Dez de Ouros', 'Herança, família, legado'),
            (11, 'Pajem de Ouros', 'Estudo, talento, interesse'),
            (12, 'Cavaleiro de Ouros', 'Confiabilidade, responsabilidade, trabalho'),
            (13, 'Rainha de Ouros', 'Abundância, segurança, luxúria'),
            (14, 'Rei de Ouros', 'Riqueza, abundância, liderança'),
        ]

        for num, nome, desc in ouros:
            cartas.append(Card(nome, 'Ouros', num, '◆', desc))

        return cartas

    def tirar(self, quantidade=1):
        """Tira `quantidade` cartas aleatórias (sem repetição) do baralho."""
        if quantidade > len(self.cartas):
            quantidade = len(self.cartas)
        return random.sample(self.cartas, quantidade)

    def tirar_com_posicoes(self, quantidade=1):
        """Tira cartas e retorna também suas posições/índices no baralho."""
        cartas_tiradas = self.tirar(quantidade)
        return cartas_tiradas

    def get_carta_por_nome(self, nome):
        """Busca uma carta pelo nome (case-insensitive)."""
        for carta in self.cartas:
            if carta.name.lower() == nome.lower():
                return carta
        return None

    def listar_por_naipe(self, naipe):
        """Lista todas as cartas de um naipe específico."""
        return [c for c in self.cartas if c.suit == naipe]


# Demo e uso
if __name__ == '__main__':
    baralho = Baralho()
    print(f'Baralho criado com {len(baralho.cartas)} cartas.\n')

    # Exemplo: listar Arcanos Maiores
    maiores = baralho.listar_por_naipe('Maiores')
    print(f'Arcanos Maiores ({len(maiores)}):')
    for c in maiores[:5]:
        print(f'  {c.number:2d}. {c.name}: {c.description}')
    print('  ...\n')

    # Exemplo: tirar 3 cartas aleatórias
    print('Tirando 3 cartas aleatórias:')
    tiradas = baralho.tirar(3)
    for c in tiradas:
        print(f'  - {c.name} ({c.suit})')
