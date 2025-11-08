import random
from sklearn.tree import DecisionTreeClassifier;
import pandas as pd;
import math
import json
import pprint;
from collections import deque

indice_sequenciaDeAcoes = 0
sequenciaDeAcoes = []

ACOES = ["bomba", "atacar, fugir, afastar, aproximar, pegar"]
DIRECAO = ["cima", "baixo", "esquerda", "direita", "parado"]

    





def arvoreDeDecisoes(TrainningData):
    X_treino = TrainningData.drop(columns=['funcao'])
    Y_treino = TrainningData['funcao']
    
    model = DecisionTreeClassifier()
    
    model.fit(X_treino, Y_treino)
    
    return model

def arvorePredict(realData, trainningData):
    model = arvoreDeDecisoes(trainningData)
    result = model.predict(realData)
    print("\n\n arvorePredict \n\n")
    print(result)
    try:
        return result
    except Exception:
        return result


import random

def gerar_dados_treinamento(
    qtd_exemplos=30,
    funcao="fugir",
    perigo=1,
    oportunidade=0,
    neutro=0
):
    """
    Gera dados sintéticos simplificados para treino da IA.
    Retorna apenas os campos:
    - perigo
    - mais_de_um_jogador_perto
    - oportunidade
    - funcao
    - neutro
    - player_com_powerup
    - powerup_existe
    """
    
    dados = []
    
    for _ in range(qtd_exemplos):
        # Simula quantidade de jogadores próximos (0 a 4)
        jogadores_perto = random.randint(0, 4)
        mais_de_um_jogador_perto = 1 if jogadores_perto > 1 else 0

        # Simula presença de powerup
        powerup_existe = random.choice([0, 1])
        player_com_powerup = random.choice([0, 1])
        
        linha = {
            "perigo": perigo,
            "mais_de_um_jogador_perto": mais_de_um_jogador_perto,
            "oportunidade": oportunidade,
            "funcao": funcao,
            "neutro": neutro,
            "player_com_powerup": player_com_powerup,
            "powerup_existe": powerup_existe
        }
        
        dados.append(linha)

    print("\n--- Dados gerados com sucesso ✅ ---\n")
    return dados




def log_estado_jogo(player, jogadores, bombas, mapa):
    print("\n========== ESTADO ATUAL DO JOGO ==========")

    print("\n🧍 JOGADORES:")
    for i, j in enumerate(jogadores, start=1):
        print(
            f"Jogador {i}: ativo={j.ativo}, tipo={j.tipo}, time={j.time}, "
            f"pos=({j.grid_x},{j.grid_y}), bombas={len(j.bombas)}, nivel={j.bomba_nivel}"
        )

    print(f"\n⭐ JOGADOR PRINCIPAL:")
    print(
        f"pos=({player.grid_x},{player.grid_y}), ativo={player.ativo}, "
        f"tipo={player.tipo}, time={player.time}, bombas={len(player.bombas)}, nivel={player.bomba_nivel}"
    )

    print("\n💣 BOMBAS:")
    if not bombas:
        print("Nenhuma bomba ativa.")
    else:
        for i, b in enumerate(bombas, start=1):
            try:
                dono_id = jogadores.index(b.dono) + 1
            except ValueError:
                dono_id = "?"
            print(
                f"Bomba {i}: pos=({b.x},{b.y}), explodida={b.explodida}, "
                f"dono=Jogador {dono_id}, fogo={len(b.fogo)} tiles"
            )

    print("\n🔹 POWERUPS NO MAPA:")
    powerups = []
    for y, linha in enumerate(mapa):
        for x, val in enumerate(linha):
            if val in [3, 4]:
                tipo = "BOMBA" if val == 3 else "FOGO"
                powerups.append((x, y, tipo))
    if not powerups:
        print("Nenhum power-up ativo.")
    else:
        for (x, y, tipo) in powerups:
            print(f"PowerUp {tipo} em ({x},{y})")

    print("==========================================\n")

    
    
def distancia_manhattan(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)




    
def filtrarDadosTreinamento(dadosDeTreinamento, **filtros):
    """
    Filtra dados de treinamento (lista de dicionários) com base em condições dinâmicas.

    Exemplo:
        filtrados = filtrarDadosTreinamento(dados, perigo=1, funcao="fugir")

    - Retorna apenas os registros que satisfazem TODAS as condições fornecidas.
    - Ignora filtros que não existem no dicionário.
    """
    if not isinstance(dadosDeTreinamento, list):
        raise ValueError("dadosDeTreinamento deve ser uma lista de dicionários")

    if not filtros:
        return dadosDeTreinamento  # sem filtros → retorna tudo

    filtrados = []
    for item in dadosDeTreinamento:
        # verifica se o item atende a todos os filtros
        if all(str(item.get(chave)) == str(valor) for chave, valor in filtros.items()):
            filtrados.append(item)

    return filtrados




# dadosTreinamento = gerar_dados_treinamento(
#     qtd_exemplos=100,
#     funcao="andar_e_quebrar",
#     perigo=0,
#     oportunidade=0,
#     neutro=1
# )

# dadosFiltrados = filtrarDadosTreinamento(dadosTreinamento, )
# print(dadosFiltrados)
#Incrementos nos dados:
#Caso bomba esteja a uma distancia X, fugir ou atacar e desviar

#Dados já gerados:
#Caso Perigo=1 e +1JogadoresPerto=1 -> fugir
#Caso Perigo=1 e +1JogadoresPerto=0 -> atacar_e_desviar
#Caso Oportunidade=1 e powerup_existe=1 e +1JogadoresPerto=1 e 0 -> pegarPower_up


    

    
    
    
    
    
    
    
    
    
    
    
    
    
# Parâmetros de jogo
# TILE_SIZE = 48
# ROWS, COLS = 11, 13
# HUD_HEIGHT = 60
# WIDTH, HEIGHT = COLS * TILE_SIZE, ROWS * TILE_SIZE
# TEMPO_MOVIMENTO = 0.1
# TEMPO_EXPLOSAO = 4
# TEMPO_FOGO = 0.5
# MAX_BOMBAS = 5
# TEMPO_PARTIDA = 180

# PONTOS_BLOCO = 100
# PONTOS_POWERUP_COLETADO = 200
# PONTOS_POWERUP_DESTRUIDO = -50
# PONTOS_MATAR_JOGADOR = 1000
# PONTOS_VITORIA = 10000

# PROB_BOMBA = 0.12
# PROB_FOGO = 0.10


# Funções de camada inferior não executam outras funções dentro dela
# Funções de camada intermediario executam funções de camada inferior
# Funções de camada superior executam funções de camada intermediária e inferior

# A função da camada superior deve juntar e/ou retornar um array das ações planejadas pela IA que será armazenado em sequenciaDeAcoes
# O decidir_acao só pode retornar 1 string/ação por vez. Isso será controlado por indice_sequenciaDeAcoes, que será resetado quando uma nova sequenciaDeAcoes for definida
# A sequencia de Ações irá persistir até que uma situação nova aconteça.
# O contexto ou estado do jogo será armazenado, sendo atualizado a cada frame por X frames. Ao ser identificado uma situação nova(como perigo, oportunidade ou a mudança do estado de algo que tava na sequencia de ações, tipo um jogador morre ou parede alvo quebra) a sequencia de ações então será reexecutada

# Colocar a arvore de decisões do SCKIT-LEARN para tomar decisões gerais(quebrar paredes? atacar jogadores? pegar powerUp?). A arvore irá receber dataFrame(podemos usar o pandas) e será treinada com esse dataFrame, com base nos diferentes contextos que a gente por no dataFrame a IA vai analisar e tomar uma decisão do que fazer...

# exemplo: 
# dist_jogador	explosao_perto	bloqueado	ação
#     1	               1	        0	    fugir
#     2	               0	        1	    colocar_bomba
#     5	               0	        0	    andar

# A IA é treinada com um dataFrame assim e então quando dermos uma nova situação, ela consegue prever qual ação tomar

# Dentro das funções utilizamos Node, DecisionNode ou SequencialNode para controlar o comportamento

#FUNÇÕES DE PESQUISA
# def localizacaoJogador():
# def localizacaoPowerUp():
# def localizacaoParedes():
# def caminho():
# def localizacaoBombas():

# FUNÇÕES DE CAMADA INFERIOR
# def andar(quantidade, direcao):
# def bomba(acao):

# FUNÇÕES DE CAMADA INTERMEDIARIA
# def sairAlcance_bomba():
# def distancia_jogadorEnemy(player[rol, col], enemy[rol, col], mapa)
# def 

# FUNÇÕES DE CAMADA SUPERIOR
# def quebrarParedes():
# def atacarJogador():
# def

def dados_treinamento_fixos():
    return [
  {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'fugir', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 0}, 
  
  {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 0}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 1, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'atacar_e_desviar', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 0},
  
  {'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 1, 'funcao': 'pegar_powerUp', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 0, 'oportunidade': 1, 'funcao': 'pegar_powerUp', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 1, 'funcao': 'pegar_powerUp', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 0, 'oportunidade': 1, 'funcao': 'pegar_powerUp', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 1, 'funcao': 'pegar_powerUp', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 1, 'funcao': 'pegar_powerUp', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 0, 'oportunidade': 1, 'funcao': 'pegar_powerUp', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 1, 'funcao': 'pegar_powerUp', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 0, 'oportunidade': 1, 'funcao': 'pegar_powerUp', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 0, 'oportunidade': 1, 'funcao': 'pegar_powerUp', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 1, 'funcao': 'pegar_powerUp', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 1, 'funcao': 'pegar_powerUp', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 1, 'funcao': 'pegar_powerUp', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 1, 'funcao': 'pegar_powerUp', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 1, 'funcao': 'pegar_powerUp', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 0, 'oportunidade': 1, 'funcao': 'pegar_powerUp', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 0, 'oportunidade': 1, 'funcao': 'pegar_powerUp', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 1, 'funcao': 'pegar_powerUp', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 1, 'funcao': 'pegar_powerUp', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 1, 'funcao': 'pegar_powerUp', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 1, 'funcao': 'pegar_powerUp', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 1, 'funcao': 'pegar_powerUp', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 1, 'funcao': 'pegar_powerUp', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 1, 'funcao': 'pegar_powerUp', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 0, 'oportunidade': 1, 'funcao': 'pegar_powerUp', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 1, 'funcao': 'pegar_powerUp', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 0, 'oportunidade': 1, 'funcao': 'pegar_powerUp', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 0, 'oportunidade': 1, 'funcao': 'pegar_powerUp', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 1, 'funcao': 'pegar_powerUp', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 0, 'oportunidade': 1, 'funcao': 'pegar_powerUp', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 1, 'funcao': 'pegar_powerUp', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 0, 'oportunidade': 1, 'funcao': 'pegar_powerUp', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 0, 'oportunidade': 1, 'funcao': 'pegar_powerUp', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 0, 'oportunidade': 1, 'funcao': 'pegar_powerUp', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 0, 'oportunidade': 1, 'funcao': 'pegar_powerUp', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 0, 'oportunidade': 1, 'funcao': 'pegar_powerUp', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 0, 'oportunidade': 1, 'funcao': 'pegar_powerUp', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 0, 'oportunidade': 1, 'funcao': 'pegar_powerUp', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 1, 'funcao': 'pegar_powerUp', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 0, 'oportunidade': 1, 'funcao': 'pegar_powerUp', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 1, 'funcao': 'pegar_powerUp', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 1, 'funcao': 'pegar_powerUp', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 1, 'funcao': 'pegar_powerUp', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 1, 'funcao': 'pegar_powerUp', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 0, 'oportunidade': 1, 'funcao': 'pegar_powerUp', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 0, 'oportunidade': 1, 'funcao': 'pegar_powerUp', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 0, 'oportunidade': 1, 'funcao': 'pegar_powerUp', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 1, 'funcao': 'pegar_powerUp', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 0, 'oportunidade': 1, 'funcao': 'pegar_powerUp', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 0, 'oportunidade': 1, 'funcao': 'pegar_powerUp', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 1},{'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 1, 'funcao': 'pegar_powerUp', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 1, 'funcao': 'pegar_powerUp', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 1, 'funcao': 'pegar_powerUp', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 0, 'oportunidade': 1, 'funcao': 'pegar_powerUp', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 0, 'oportunidade': 1, 'funcao': 'pegar_powerUp', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 0, 'oportunidade': 1, 'funcao': 'pegar_powerUp', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 1, 'funcao': 'pegar_powerUp', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 0, 'oportunidade': 1, 'funcao': 'pegar_powerUp', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 0, 'oportunidade': 1, 'funcao': 'pegar_powerUp', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 1},{'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 1, 'funcao': 'pegar_powerUp', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 1, 'funcao': 'pegar_powerUp', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 1, 'funcao': 'pegar_powerUp', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 0, 'oportunidade': 1, 'funcao': 'pegar_powerUp', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 0, 'oportunidade': 1, 'funcao': 'pegar_powerUp', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 0, 'oportunidade': 1, 'funcao': 'pegar_powerUp', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 1, 'funcao': 'pegar_powerUp', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 0, 'oportunidade': 1, 'funcao': 'pegar_powerUp', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 0, 'oportunidade': 1, 'funcao': 'pegar_powerUp', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 1},{'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 1, 'funcao': 'pegar_powerUp', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 1, 'funcao': 'pegar_powerUp', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 1, 'funcao': 'pegar_powerUp', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 0, 'oportunidade': 1, 'funcao': 'pegar_powerUp', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 0, 'oportunidade': 1, 'funcao': 'pegar_powerUp', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 0, 'oportunidade': 1, 'funcao': 'pegar_powerUp', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 1, 'funcao': 'pegar_powerUp', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 0, 'oportunidade': 1, 'funcao': 'pegar_powerUp', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 0, 'oportunidade': 1, 'funcao': 'pegar_powerUp', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 1},{'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 1, 'funcao': 'pegar_powerUp', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 1, 'funcao': 'pegar_powerUp', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 1, 'funcao': 'pegar_powerUp', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 0, 'oportunidade': 1, 'funcao': 'pegar_powerUp', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 0, 'oportunidade': 1, 'funcao': 'pegar_powerUp', 'neutro': 0, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 0, 'oportunidade': 1, 'funcao': 'pegar_powerUp', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 1, 'funcao': 'pegar_powerUp', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 0, 'oportunidade': 1, 'funcao': 'pegar_powerUp', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 0, 'oportunidade': 1, 'funcao': 'pegar_powerUp', 'neutro': 0, 'player_com_powerup': 1, 'powerup_existe': 1},
  
  {'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 1, 'powerup_existe': 0}, {'perigo': 0, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 1, 'powerup_existe': 0}, {'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 0, 'powerup_existe': 0}, {'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 0, 'powerup_existe': 0}, {'perigo': 0, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 1, 'powerup_existe': 0}, {'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 0, 'powerup_existe': 0}, {'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 0, 'powerup_existe': 0}, {'perigo': 0, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 0, 'powerup_existe': 0}, {'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 0, 'powerup_existe': 0}, {'perigo': 0, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 0, 'powerup_existe': 0}, {'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 0, 'powerup_existe': 0}, {'perigo': 0, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 1, 'powerup_existe': 0}, {'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 1, 'powerup_existe': 0}, {'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 0, 'powerup_existe': 0}, {'perigo': 0, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 1, 'powerup_existe': 0}, {'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 1, 'powerup_existe': 0}, {'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 0, 'powerup_existe': 0}, {'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 1, 'powerup_existe': 0}, {'perigo': 0, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 1, 'powerup_existe': 0}, {'perigo': 0, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 1, 'powerup_existe': 0}, {'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 1, 'powerup_existe': 0}, {'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 1, 'powerup_existe': 0}, {'perigo': 0, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 0, 'powerup_existe': 0}, {'perigo': 0, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 1, 'powerup_existe': 0}, {'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 1, 'powerup_existe': 0}, {'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 1, 'powerup_existe': 0}, {'perigo': 0, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 1, 'powerup_existe': 0}, {'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 0, 'powerup_existe': 0}, {'perigo': 0, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 0, 'powerup_existe': 0}, {'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 0, 'powerup_existe': 0}, {'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 1, 'powerup_existe': 0}, {'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 1, 'powerup_existe': 0}, {'perigo': 0, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 1, 'powerup_existe': 0}, {'perigo': 0, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 1, 'powerup_existe': 0}, {'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 0, 'powerup_existe': 0}, {'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 1, 'powerup_existe': 0}, {'perigo': 0, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 1, 'powerup_existe': 0}, {'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 1, 'powerup_existe': 0}, {'perigo': 0, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 0, 'powerup_existe': 0}, {'perigo': 0, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 1, 'powerup_existe': 0}, {'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 0, 'powerup_existe': 0}, {'perigo': 0, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 0, 'powerup_existe': 0}, {'perigo': 0, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 1, 'powerup_existe': 0}, {'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 1, 'powerup_existe': 0}, {'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 1, 'powerup_existe': 0}, {'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 1, 'powerup_existe': 0}, {'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 1, 'powerup_existe': 0}, {'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 0, 'powerup_existe': 0}, {'perigo': 0, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 0, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 1, 'powerup_existe': 1}, {'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 0, 'powerup_existe': 0}, {'perigo': 0, 'mais_de_um_jogador_perto': 0, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 0, 'powerup_existe': 0}, {'perigo': 0, 'mais_de_um_jogador_perto': 1, 'oportunidade': 0, 'funcao': 'andar_e_quebrar', 'neutro': 1, 'player_com_powerup': 1, 'powerup_existe': 1}
  ]
    
# exemploDadoReal = [{'bomba_existe': 1,
#   'bomba_player': 1,
#   'dist_bomba1': 3,
#   'dist_bomba2': 9,
#   'dist_bomba3': 10,
#   'dist_bomba4': 5,
#   'dist_jogador1': 0,
#   'dist_jogador2': 9,
#   'dist_jogador3': 11,
#   'dist_jogador4': 3,
#   'dist_powerup': 2,
#   'mais_de_um_jogador_perto': 0,
#   'neutro': 0,
#   'oportunidade': 0,
#   'perigo': 1,
#   'player_com_powerup': 0,
#   'powerup_existe': 1}]
# dadosFiltrados = filtrarDadosTreinamento(dadosTreinamento, powerup_existe=0)
# pprint.pprint(dadosFiltrados)

# dataframeTreino = pd.DataFrame(dados_treinamento_fixos())
# dadoReal = pd.DataFrame(exemploDadoReal)
# result = arvorePredict(dadoReal, dataframeTreino)
# print(result)








def fugir():
    return 'cima'
import random
from collections import deque

def atacar_e_desviar(player, mapa, jogadores, bombas, powerups):
    """
    Estratégia ofensiva inteligente: busca posições onde a bomba pode atingir o inimigo,
    tenta alcançá-las, planta e recua, desviando de perigos.
    """
    from collections import deque
    import random

    x, y = player["pos"]
    id_player = player["id"]
    largura, altura = len(mapa[0]), len(mapa)
    alcance_bomba = player.get("bomba_nivel", 2)

    # === Funções auxiliares ===
    def dentro(a, b): return 0 <= a < largura and 0 <= b < altura

    def perigo(pos):
        """Verifica se a posição está dentro da área de explosão de alguma bomba."""
        px, py = pos
        for b in bombas:
            bx, by = b["pos"]
            alcance = b.get("alcance", b.get("nivel", b.get("bomba_nivel", 2)))
            if px == bx and abs(py - by) <= alcance:
                return True
            if py == by and abs(px - bx) <= alcance:
                return True
        return False

    def vizinhos(a, b):
        return [(a+1,b), (a-1,b), (a,b+1), (a,b-1)]

    def direcao_para(orig, dest):
        ox, oy = orig; dx, dy = dest
        if dx > ox: return "direita"
        if dx < ox: return "esquerda"
        if dy > oy: return "baixo"
        if dy < oy: return "cima"
        return "parado"

    def bfs(destinos, evitar_perigo=True):
        fila = deque([(x, y, [])])
        visitado = {(x, y)}
        while fila:
            cx, cy, caminho = fila.popleft()
            if (cx, cy) in destinos:
                return caminho + [(cx, cy)]
            for nx, ny in vizinhos(cx, cy):
                if dentro(nx, ny) and (nx, ny) not in visitado:
                    if mapa[ny][nx] in [0, 3, 4, 2]:
                        if not (evitar_perigo and perigo((nx, ny))):
                            fila.append((nx, ny, caminho + [(cx, cy)]))
                            visitado.add((nx, ny))
        return []

    # === 1️⃣ Evitar perigo imediato ===
    if perigo((x, y)):
        seguros = [p for p in vizinhos(x, y) if dentro(*p) and not perigo(p) and mapa[p[1]][p[0]] in [0, 3, 4]]
        if seguros:
            destino = random.choice(seguros)
            return direcao_para((x, y), destino)
        return "parado"

    # === 2️⃣ Selecionar inimigo mais próximo ===
    inimigos = [j for j in jogadores if j["ativo"] and j["id"] != id_player]
    if not inimigos:
        return "parado"
    alvo = min(inimigos, key=lambda j: abs(j["pos"][0]-x) + abs(j["pos"][1]-y))
    ax, ay = alvo["pos"]

    # === 3️⃣ Calcular posições onde a bomba atingiria o inimigo ===
    posicoes_ataque = []
    # horizontal
    if ay == y:
        for dx in range(-alcance_bomba, alcance_bomba + 1):
            tx = x + dx
            if dentro(tx, y) and abs(tx - ax) <= alcance_bomba:
                # sem obstáculo no caminho
                livre = True
                passo = 1 if ax > tx else -1
                for i in range(tx, ax, passo):
                    if mapa[y][i] not in [0, 3, 4]:
                        livre = False
                        break
                if livre:
                    posicoes_ataque.append((tx, y))
    # vertical
    if ax == x:
        for dy in range(-alcance_bomba, alcance_bomba + 1):
            ty = y + dy
            if dentro(x, ty) and abs(ty - ay) <= alcance_bomba:
                livre = True
                passo = 1 if ay > ty else -1
                for j in range(ty, ay, passo):
                    if mapa[j][x] not in [0, 3, 4]:
                        livre = False
                        break
                if livre:
                    posicoes_ataque.append((x, ty))

    # === 4️⃣ Se já está em posição ideal, plantar bomba ===
    if (x, y) in posicoes_ataque and player["bombas_ativas"] < player["max_bombas"]:
        return "bomba"

    # === 5️⃣ Se há posição de ataque viável, mover até ela ===
    if posicoes_ataque:
        caminho = bfs(posicoes_ataque)
        if caminho and len(caminho) > 1:
            prox = caminho[1]
            return direcao_para((x, y), prox)

    # === 6️⃣ Caso contrário, tentar encurralar o inimigo ===
    viz_inimigo = vizinhos(ax, ay)
    livres = [v for v in viz_inimigo if dentro(*v) and mapa[v[1]][v[0]] in [0, 3, 4] and not perigo(v)]
    if livres:
        # mover para bloquear rota de fuga
        caminho = bfs(livres)
        if caminho and len(caminho) > 1:
            prox = caminho[1]
            return direcao_para((x, y), prox)

    # === 7️⃣ Se o caminho está bloqueado, destruir blocos na direção do inimigo ===
    blocos = [(ix, iy) for iy in range(altura) for ix in range(largura)
              if mapa[iy][ix] == 2 and abs(ix - ax) + abs(iy - ay) < 6]
    if blocos:
        alvo_bloco = min(blocos, key=lambda b: abs(b[0]-x) + abs(b[1]-y))
        caminho = bfs([alvo_bloco])
        if caminho and len(caminho) > 1:
            prox = caminho[1]
            return direcao_para((x, y), prox)

    # === 8️⃣ Movimento tático leve se nada a fazer ===
    livres = [p for p in vizinhos(x, y) if dentro(*p) and not perigo(p) and mapa[p[1]][p[0]] in [0, 3, 4]]
    if livres:
        prox = random.choice(livres)
        return direcao_para((x, y), prox)

    return "parado"



def pegar_powerup(player, mapa, powerups, bombas):
    """
    Versão melhorada de pegar_powerup:
    - Trata a célula do powerup (valores 3/4) como percorrível para a BFS.
    - Evita zonas de perigo.
    - Se uma parede destrutível bloqueia o único caminho, aproxima-se e aciona 'bomba'.
    - Retorna uma das strings: "cima", "baixo", "esquerda", "direita", "bomba", "parado".
    """
    from collections import deque

    pos = player["pos"]
    if not pos:
        return "parado"
    x, y = pos
    largura = len(mapa[0])
    altura = len(mapa)

    def mover_para(origem, destino):
        ox, oy = origem
        dx, dy = destino
        if dx > ox: return "direita"
        if dx < ox: return "esquerda"
        if dy > oy: return "baixo"
        if dy < oy: return "cima"
        return "parado"

    # --- calcular zonas de perigo (mesma lógica que antes) ---
    zonas_perigo = set()
    for bomba in bombas:
        bx, by = bomba["pos"]
        alcance = bomba.get("alcance", player.get("bomba_nivel", 1) + 2)
        zonas_perigo.add((bx, by))
        for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
            for i in range(1, alcance+1):
                nx, ny = bx + dx*i, by + dy*i
                if not (0 <= nx < largura and 0 <= ny < altura):
                    break
                if mapa[ny][nx] == 2:  # indestrutível bloqueia
                    break
                zonas_perigo.add((nx, ny))
                if mapa[ny][nx] == 1:  # parede destrutível bloqueia propagação
                    break

    # Se estou em perigo, tento escapar primeiro
    if (x, y) in zonas_perigo:
        destino_seguro = achar_posicao_segura(mapa, zonas_perigo, (x, y))
        if destino_seguro:
            return mover_para((x, y), destino_seguro)
        return "parado"

    # Sem powerups
    if not powerups:
        return "parado"

    # encontra o powerup mais próximo (Manhattan)
    def manhattan(a, b):
        return abs(a[0]-b[0]) + abs(a[1]-b[1])
    # assegura formato consistente: lista de dicts com 'pos'
    powerups_validos = [p for p in powerups if p and p.get("pos")]
    if not powerups_validos:
        return "parado"
    alvo = min(powerups_validos, key=lambda p: manhattan((x,y), p["pos"]))["pos"]

    # Se já estou adjacente ao powerup, mover direto (ou pegar se estiver na mesma célula)
    if (x, y) == alvo:
        return "parado"  # se já na mesma célula, nada a fazer (ou coleta automática)
    if manhattan((x, y), alvo) == 1:
        return mover_para((x, y), alvo)

    # BFS que considera célula alvo como transitável mesmo que mapa != 0
    fila = deque([(x, y)])
    visitados = {(x, y)}
    pais = {(x, y): None}
    parede_bloqueio = None
    encontrou = False

    while fila:
        cx, cy = fila.popleft()
        if (cx, cy) == alvo:
            encontrou = True
            break

        for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
            nx, ny = cx + dx, cy + dy
            if not (0 <= nx < largura and 0 <= ny < altura):
                continue
            if (nx, ny) in visitados or (nx, ny) in zonas_perigo:
                continue

            celula = mapa[ny][nx]
            # Se for célula livre (0) ou é o alvo (pode ser 3/4) -> pode caminhar
            if celula == 0 or (nx, ny) == alvo:
                visitados.add((nx, ny))
                pais[(nx, ny)] = (cx, cy)
                fila.append((nx, ny))
            # Se for parede destrutível e ainda não marcamos uma bloqueadora, salvamos para tentar explodir
            elif celula == 1 and parede_bloqueio is None:
                parede_bloqueio = (nx, ny, (cx, cy))

    # Se encontrou caminho, reconstrói primeiro passo a partir do alvo até a origem
    if encontrou:
        step_x, step_y = alvo
        # sobe até o step cujo pai é a origem (x,y)
        while pais.get((step_x, step_y)) is not None and pais[(step_x, step_y)] != (x, y):
            step_x, step_y = pais[(step_x, step_y)]
        # se o pai direto for a origem, então (step_x,step_y) é o próximo passo
        return mover_para((x, y), (step_x, step_y))

    # Se não encontrou, mas há parede destrutível bloqueando — aproximar e plantar bomba
    if parede_bloqueio:
        bx, by, origem = parede_bloqueio
        # se estamos adjacentes à parede, soltar bomba
        if manhattan((x, y), (bx, by)) == 1 and player.get("bombas_ativas", 0) < player.get("max_bombas", 1):
            return "bomba"
        # caso contrário, mover em direção à célula filha que leva até a parede
        # origem é a célula a partir da qual descobrimos a parede; mover até origem
        return mover_para((x, y), origem)

    # última tentativa: mover para qualquer vizinho seguro em direção ao alvo (heurística simples)
    melhor = None
    melhor_dist = math.inf
    for dx, dy in [(0,-1),(0,1),(-1,0),(1,0)]:
        nx, ny = x+dx, y+dy
        if 0 <= nx < largura and 0 <= ny < altura:
            if (nx, ny) not in zonas_perigo and mapa[ny][nx] == 0:
                d = manhattan((nx, ny), alvo)
                if d < melhor_dist:
                    melhor_dist = d
                    melhor = (nx, ny)
    if melhor:
        return mover_para((x, y), melhor)

    return "parado"





def andar_e_quebrar(player, mapa, jogadores, bombas):
    pos = player["pos"]
    x, y = pos
    largura = len(mapa[0])
    altura = len(mapa)

    # -------------------------------------------------------------
    # Funções auxiliares
    def pos_valida(px, py):
        return 0 <= px < largura and 0 <= py < altura and mapa[py][px] == 0

    def mover_para(origem, destino):
        ox, oy = origem
        dx, dy = destino
        if dx > ox: return "direita"
        if dx < ox: return "esquerda"
        if dy > oy: return "baixo"
        if dy < oy: return "cima"
        return "parado"

    # -------------------------------------------------------------
    # 1️⃣ Calcular zonas de perigo com base nas bombas
    zonas_perigo = set()
    for bomba in bombas:
        bx, by = bomba["pos"]
        alcance = bomba.get("alcance", player["bomba_nivel"] + 2)
        zonas_perigo.add((bx, by))
        for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
            for i in range(1, alcance+1):
                nx, ny = bx + dx*i, by + dy*i
                if not (0 <= nx < largura and 0 <= ny < altura):
                    break
                if mapa[ny][nx] == 2:  # parede indestrutível bloqueia explosão
                    break
                zonas_perigo.add((nx, ny))
                if mapa[ny][nx] == 1:  # para em bloco quebrável
                    break

    # -------------------------------------------------------------
    # 2️⃣ Se estiver em perigo → fugir
    if (x, y) in zonas_perigo:
        destino_seguro = achar_posicao_segura(mapa, zonas_perigo, (x, y))
        if destino_seguro:
            return mover_para((x, y), destino_seguro)
        else:
            return "parado"

    # -------------------------------------------------------------
    # 3️⃣ Se tiver bloco quebrável adjacente → soltar bomba
    for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < largura and 0 <= ny < altura:
            if mapa[ny][nx] == 1 and player["bombas_ativas"] < player["max_bombas"]:
                return "bomba"

    # -------------------------------------------------------------
    # 4️⃣ Procurar bloco quebrável mais próximo (via BFS)
    alvo = achar_bloco_quebravel_mais_proximo(mapa, (x, y), zonas_perigo)
    if alvo:
        return mover_para((x, y), alvo)

    # -------------------------------------------------------------
    # 5️⃣ Se não houver blocos → andar aleatoriamente em zona segura
    direcoes = [("cima", (0, -1)), ("baixo", (0, 1)), ("esquerda", (-1, 0)), ("direita", (1, 0))]
    random.shuffle(direcoes)
    for nome, (dx, dy) in direcoes:
        nx, ny = x + dx, y + dy
        if pos_valida(nx, ny) and (nx, ny) not in zonas_perigo:
            return nome

    return "parado"


def achar_posicao_segura(mapa, zonas_perigo, origem):
    """Busca a posição segura mais próxima (fora da área de explosão)."""
    largura = len(mapa[0])
    altura = len(mapa)
    fila = deque([origem])
    visitados = {origem}
    pais = {origem: None}

    while fila:
        x, y = fila.popleft()
        if (x, y) not in zonas_perigo and mapa[y][x] == 0:
            # Achou posição segura — retorna o primeiro passo
            while pais[(x, y)] != origem and pais[(x, y)] is not None:
                x, y = pais[(x, y)]
            return (x, y)
        for dx, dy in [(0,1),(0,-1),(1,0),(-1,0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < largura and 0 <= ny < altura and (nx, ny) not in visitados:
                if mapa[ny][nx] == 0:
                    visitados.add((nx, ny))
                    pais[(nx, ny)] = (x, y)
                    fila.append((nx, ny))
    return None


def achar_bloco_quebravel_mais_proximo(mapa, origem, zonas_perigo):
    """Procura o bloco quebrável mais próximo e retorna a primeira direção pra chegar até ele."""
    largura = len(mapa[0])
    altura = len(mapa)
    fila = deque([origem])
    visitados = {origem}
    pais = {origem: None}

    while fila:
        x, y = fila.popleft()
        # se há bloco quebrável adjacente, encontramos o destino final
        for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < largura and 0 <= ny < altura:
                if mapa[ny][nx] == 1 and (x, y) not in zonas_perigo:
                    # sobe até o primeiro passo
                    while pais[(x, y)] != origem and pais[(x, y)] is not None:
                        x, y = pais[(x, y)]
                    return (x, y)
        # expandir busca
        for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < largura and 0 <= ny < altura and (nx, ny) not in visitados:
                if mapa[ny][nx] == 0 and (nx, ny) not in zonas_perigo:
                    visitados.add((nx, ny))
                    pais[(nx, ny)] = (x, y)
                    fila.append((nx, ny))
    return None


def extrair_informacoes(player, mapa, jogadores, bombas):
    """
    Extrai informações do estado atual do jogo para uso em IA.
    Retorna um dicionário com posições e status relevantes.
    """

    info = {
        "player": {
    "id": getattr(player, "id", 0),
    "pos": (player.grid_x, player.grid_y),
    "ativo": player.ativo,
    "bomba_nivel": player.bomba_nivel,
    "max_bombas": player.max_bombas,
    "bombas_ativas": len(player.bombas)
    },
        "jogadores": [],
        "bombas": [],
        "powerups": [],
        "tem_bombas": False,
        "tem_powerups": False
    }

    # Jogadores
    for j in jogadores:
        info["jogadores"].append({
            "id": jogadores.index(j),
            "pos": (j.grid_x, j.grid_y),
            "ativo": j.ativo,
            "time": j.time
        })

    # Bombas
    for b in bombas:
        info["bombas"].append({
        "pos": (b.x, b.y),
        "nivel": b.nivel,
        "explodida": b.explodida,
        "tempo_explosao": b.tempo_explosao,
        "ativo": not b.explodida,  # ativa enquanto não explodir
        "owner_id": getattr(b, "owner_id", None)  # se existir, adiciona o dono
    })
    info["tem_bombas"] = len(info["bombas"]) > 0

    # PowerUps
    for y, linha in enumerate(mapa):
        for x, val in enumerate(linha):
            if val in [3, 4]:  # 3 = bomba, 4 = fogo
                info["powerups"].append({
                    "pos": (x, y),
                    "tipo": "bomba" if val == 3 else "fogo"
                })
    info["tem_powerups"] = len(info["powerups"]) > 0

    return info





def transformar_dados(
    player,
    jogadores,
    bombas,
    powerups,
    distancia_manhattan,
    funcao="fugir",
    limite_powerup=6
):
    """
    Transforma o estado atual do jogo em um dicionário simplificado,
    compatível com os dados gerados por gerar_dados_treinamento().

    Retorna apenas:
    perigo, mais_de_um_jogador_perto, oportunidade,
    funcao, neutro, player_com_powerup, powerup_existe.
    """

    # --- Inicialização do dicionário base ---
    dados = {
        'perigo': 0,
        'mais_de_um_jogador_perto': 0,
        'oportunidade': 0,
        'neutro': 0,
        'player_com_powerup': 0,
        'powerup_existe': 0,
    }


    # Caso o player não tenha posição válida
    if not player.get('pos'):
        return dados

    px, py = player['pos']

    # --- Distâncias dos jogadores ---
    distancias_jogadores = []
    for j in jogadores[:4]:
        if j['ativo'] and j.get('pos'):
            d = distancia_manhattan(px, py, *j['pos'])
            if j['id'] != player['id']:
                distancias_jogadores.append(d)

    # --- Lógica de jogadores próximos ---
    jogadores_perto = [d for d in distancias_jogadores if d < 5]
    if len(jogadores_perto) >= 1:
        dados['perigo'] = 1
    if len(jogadores_perto) > 1:
        dados['mais_de_um_jogador_perto'] = 1

    # --- PowerUp ---
    if len(powerups) > 0:
        dados['powerup_existe'] = 1
        # Pega o powerup mais próximo
        dist_p = min(
            distancia_manhattan(px, py, *p['pos'])
            for p in powerups if p.get('pos')
        )
        # Se existe powerup e está dentro do limite de distância
        if dist_p <= limite_powerup and not dados['perigo']:
            dados['oportunidade'] = 1
    else:
        dados['powerup_existe'] = 0

    # --- Caso nenhum perigo ou oportunidade ---
    if not dados['perigo'] and not dados['oportunidade']:
        dados['neutro'] = 1

    # --- Powerup do player ---
    if player.get('tem_powerup', False):
        dados['player_com_powerup'] = 1

    return dados





def decidir_acao(player, mapa, jogadores, bombas, tempo_restante, pontos, hud_info, self_state):
    # estadoDeJogo = extrair_informacoes(player, mapa, jogadores, bombas)
    # print('\n\n estado de jogo \n\n')
    # print(estadoDeJogo)
    estado = extrair_informacoes(player, mapa, jogadores, bombas)
    print('\n\n Extrair Informações\n')
    print(estado)
    # Transforma o estado em dados estruturados para IA
    exemploDadoReal = transformar_dados(
        estado["player"],
        estado["jogadores"],
        estado["bombas"],
        estado["powerups"],
        distancia_manhattan
    )

    print("\n--- Estado Transformado ---")
    print(exemploDadoReal)
    dataframeTreino = pd.DataFrame(dados_treinamento_fixos())
    dadoReal = pd.DataFrame([exemploDadoReal])

    result = arvorePredict(dadoReal, dataframeTreino)
    acao = result[0]

    if acao == 'atacar_e_desviar':
        # return atacar_e_desviar()
        return atacar_e_desviar(estado['player'], mapa, estado['jogadores'], estado['bombas'], estado['powerups'])
    elif acao == 'fugir':
        # return fugir()
        return andar_e_quebrar(estado["player"], mapa, estado["jogadores"], estado["bombas"])
    elif acao == 'pegar_powerUp':
        return pegar_powerup(estado["player"], mapa, estado["powerups"], estado["bombas"])
    elif acao == 'andar_e_quebrar':
        # return andar_e_quebrar()
        return andar_e_quebrar(estado["player"], mapa, estado["jogadores"], estado["bombas"])
    log_estado_jogo(player, jogadores, bombas, mapa)
    
