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

RAIO_BUSCA_INIMIGO = 15  # Aumentado para busca mais agressiva
RAIO_FUGA_MINIMO = 3   





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

def tem_bomba_na_posicao(x, y, bombas):
    """Verifica se já existe bomba na posição."""
    for bomba in bombas:
        if not bomba.get("explodida", False):
            bx, by = bomba["pos"]
            if bx == x and by == y:
                return True
    return False

def calcular_zonas_perigo(bombas, mapa, player):
    """Calcula todas as zonas de perigo das bombas ativas."""
    largura, altura = len(mapa[0]), len(mapa)
    zonas_perigo = set()
    
    for bomba in bombas:
        if bomba.get("explodida", False):
            continue
            
        bx, by = bomba["pos"]
        alcance = bomba.get("alcance", player.get("bomba_nivel", 2))
        
        # Adiciona posição da bomba
        zonas_perigo.add((bx, by))
        
        # Expande em 4 direções
        for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
            for i in range(1, alcance + 1):
                nx, ny = bx + dx * i, by + dy * i
                
                # Verifica limites
                if not (0 <= nx < largura and 0 <= ny < altura):
                    break
                    
                # Paredes indestrutíveis bloqueiam
                if mapa[ny][nx] == 2:
                    break
                    
                zonas_perigo.add((nx, ny))
                
                # Paredes destrutíveis bloqueiam propagação
                if mapa[ny][nx] == 1:
                    break
    
    return zonas_perigo


def tem_rota_fuga_segura(x, y, mapa, zonas_perigo_atuais, alcance_bomba):
    """
    Verifica se há pelo menos UMA rota de fuga viável.
    Simula a bomba sendo colocada em (x,y) e busca caminho seguro.
    """
    largura, altura = len(mapa[0]), len(mapa)
    
    # Simula zona de perigo da nova bomba
    zonas_perigo_simuladas = set(zonas_perigo_atuais)
    zonas_perigo_simuladas.add((x, y))
    
    for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
        for i in range(1, alcance_bomba + 1):
            nx, ny = x + dx * i, y + dy * i
            if not (0 <= nx < largura and 0 <= ny < altura):
                break
            if mapa[ny][nx] == 2:
                break
            zonas_perigo_simuladas.add((nx, ny))
            if mapa[ny][nx] == 1:
                break
    
    # BFS para encontrar posição segura
    fila = deque([(x, y, 0)])
    visitados = {(x, y)}
    
    while fila:
        cx, cy, dist = fila.popleft()
        
        # Se encontrou posição segura a distância mínima
        if (cx, cy) not in zonas_perigo_simuladas and dist >= RAIO_FUGA_MINIMO:
            return True
        
        # Explora vizinhos
        for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
            nx, ny = cx + dx, cy + dy
            
            if (0 <= nx < largura and 0 <= ny < altura and 
                (nx, ny) not in visitados and 
                mapa[ny][nx] in [0, 3, 4]):  # Livre ou powerup
                
                visitados.add((nx, ny))
                fila.append((nx, ny, dist + 1))
    
    
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
   return random.choice(['cima', 'baixo', 'esquerda', 'direita'])


import random
from collections import deque

def atacar_e_desviar(player, mapa, jogadores, bombas, powerups):
    """
    CORREÇÃO: Agora valida que jogadores[] não contém o próprio player.
    """
    x, y = player["pos"]
    id_player = player["id"]
    largura, altura = len(mapa[0]), len(mapa)
    alcance_bomba = player.get("bomba_nivel", 2)
    bombas_ativas = player.get("bombas_ativas", 0)
    max_bombas = player.get("max_bombas", 1)
    
    print(f"\n⚔️ MODO COMBATE - Player {id_player} em ({x},{y})")
    print(f"   Bombas: {bombas_ativas}/{max_bombas} | Alcance: {alcance_bomba}")
    
    def dentro(a, b):
        return 0 <= a < largura and 0 <= b < altura
    
    def direcao_para(orig, dest):
        ox, oy = orig
        dx, dy = dest
        if dx > ox: return "direita"
        if dx < ox: return "esquerda"
        if dy > oy: return "baixo"
        if dy < oy: return "cima"
        return "parado"
    
    def celula_livre(nx, ny):
        return dentro(nx, ny) and mapa[ny][nx] in [0, 3, 4]
    
    # Calcular zonas de perigo
    zonas_perigo = calcular_zonas_perigo(bombas, mapa, player)
    
    # Fuga emergencial
    if (x, y) in zonas_perigo:
        print("  🚨 PERIGO CRÍTICO - Fugindo!")
        
        melhores_fugas = []
        for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
            nx, ny = x + dx, y + dy
            if celula_livre(nx, ny) and (nx, ny) not in zonas_perigo:
                dist_min_bomba = min(
                    distancia_manhattan(nx, ny, *b["pos"]) 
                    for b in bombas if not b.get("explodida", False)
                ) if bombas else 999
                melhores_fugas.append(((nx, ny), dist_min_bomba))
        
        if melhores_fugas:
            melhor = max(melhores_fugas, key=lambda x: x[1])
            print(f"    → Fugindo para {melhor[0]} (dist: {melhor[1]})")
            return direcao_para((x, y), melhor[0])
        
        return "parado"
    
    # CORREÇÃO: Valida que jogadores não contém o próprio player
    inimigos = []
    for j in jogadores:
        if not j["ativo"]:
            continue
        
        jx, jy = j["pos"]
        
        # VALIDAÇÃO: Não adiciona se for a mesma posição
        if jx == x and jy == y:
            print(f"  ⚠️ Ignorando jogador na mesma posição (ID: {j['id']})")
            continue
        
        # VALIDAÇÃO: Não adiciona se for o mesmo ID
        if j["id"] == id_player:
            print(f"  ⚠️ Ignorando próprio player (ID: {j['id']})")
            continue
        
        inimigos.append(j)
    
    if not inimigos:
        print("  ❌ SEM INIMIGOS - Modo exploração")
        return quebrar_blocos_proximo(x, y, mapa, bombas_ativas, max_bombas, zonas_perigo, alcance_bomba, bombas)
    
    print(f"  🎯 {len(inimigos)} inimigos detectados")
    
    # Selecionar alvo prioritário
    alvos_priorizados = []
    for inimigo in inimigos:
        ax, ay = inimigo["pos"]
        dist = distancia_manhattan(x, y, ax, ay)
        
        vizinhos_livres = sum(
            1 for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]
            if dentro(ax+dx, ay+dy) and mapa[ay+dy][ax+dx] == 0
        )
        
        score = dist - (vizinhos_livres * 2)
        alvos_priorizados.append((inimigo, dist, score))
    
    alvo, dist_alvo, _ = min(alvos_priorizados, key=lambda t: t[2])
    ax, ay = alvo["pos"]
    
    print(f"  🎯 ALVO: Inimigo ID {alvo['id']} em ({ax},{ay}) | Distância: {dist_alvo}")
    
    # Ataque direto
    alinhado_horizontal = (y == ay and abs(x - ax) <= alcance_bomba + 2)
    alinhado_vertical = (x == ax and abs(y - ay) <= alcance_bomba + 2)
    
    if (alinhado_horizontal or alinhado_vertical) and dist_alvo <= alcance_bomba + 2:
        caminho_livre = True
        
        if alinhado_horizontal:
            for ix in range(min(x, ax) + 1, max(x, ax)):
                if mapa[y][ix] not in [0, 3, 4]:
                    caminho_livre = False
                    break
        
        if alinhado_vertical:
            for iy in range(min(y, ay) + 1, max(y, ay)):
                if mapa[iy][x] not in [0, 3, 4]:
                    caminho_livre = False
                    break
        
        if caminho_livre and bombas_ativas < max_bombas and not tem_bomba_na_posicao(x, y, bombas):
            tem_fuga = tem_rota_fuga_segura(x, y, mapa, zonas_perigo, alcance_bomba)
            inimigo_muito_proximo = dist_alvo <= 2
            
            if tem_fuga or inimigo_muito_proximo:
                print(f"    💣 BOMBA TÁTICA! (fuga: {tem_fuga}, prox: {inimigo_muito_proximo})")
                return "bomba"
    
    # Perseguição
    if dist_alvo <= RAIO_BUSCA_INIMIGO:
        print(f"    🏃 PERSEGUINDO ALVO...")
        
        movimentos_possiveis = []
        
        for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
            nx, ny = x + dx, y + dy
            
            if not celula_livre(nx, ny) or (nx, ny) in zonas_perigo:
                continue
            
            nova_dist = distancia_manhattan(nx, ny, ax, ay)
            
            score = -nova_dist * 10
            
            if nx == ax or ny == ay:
                score += 30
            
            if abs(nx - ax) <= 2 and abs(ny - ay) <= 2:
                score += 20
            
            if nova_dist > RAIO_BUSCA_INIMIGO:
                score -= 50
            
            movimentos_possiveis.append(((nx, ny), score))
        
        if movimentos_possiveis:
            melhor = max(movimentos_possiveis, key=lambda m: m[1])
            print(f"      → Movimento: {melhor[0]} (score: {melhor[1]})")
            return direcao_para((x, y), melhor[0])
    
    # Busca ativa
    print(f"    🔍 BUSCANDO INIMIGO...")
    
    movimentos = []
    for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
        nx, ny = x + dx, y + dy
        if celula_livre(nx, ny) and (nx, ny) not in zonas_perigo:
            dist = distancia_manhattan(nx, ny, ax, ay)
            movimentos.append(((nx, ny), dist))
    
    if movimentos:
        melhor = min(movimentos, key=lambda m: m[1])
        return direcao_para((x, y), melhor[0])
    
    # Fallback
    return quebrar_blocos_proximo(x, y, mapa, bombas_ativas, max_bombas, zonas_perigo, alcance_bomba, bombas)


def quebrar_blocos_proximo(x, y, mapa, bombas_ativas, max_bombas, zonas_perigo, alcance_bomba, bombas):
    """Quebra blocos quando não há inimigos."""
    largura, altura = len(mapa[0]), len(mapa)
    
    for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < largura and 0 <= ny < altura and mapa[ny][nx] == 1:
            if bombas_ativas < max_bombas and not tem_bomba_na_posicao(x, y, bombas):
                if tem_rota_fuga_segura(x, y, mapa, zonas_perigo, alcance_bomba):
                    print(f"    💣 Quebrando bloco adjacente")
                    return "bomba"
    
    blocos_proximos = []
    for iy in range(altura):
        for ix in range(largura):
            if mapa[iy][ix] == 1:
                dist = distancia_manhattan(x, y, ix, iy)
                if dist < 8:
                    blocos_proximos.append((ix, iy, dist))
    
    if blocos_proximos:
        bloco = min(blocos_proximos, key=lambda b: b[2])
        bx, by, _ = bloco
        
        movimentos = []
        for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
            nx, ny = x + dx, y + dy
            if (0 <= nx < largura and 0 <= ny < altura and 
                mapa[ny][nx] == 0 and (nx, ny) not in zonas_perigo):
                dist = distancia_manhattan(nx, ny, bx, by)
                movimentos.append(((nx, ny), dist))
        
        if movimentos:
            melhor = min(movimentos, key=lambda m: m[1])
            return "direita" if melhor[0][0] > x else "esquerda" if melhor[0][0] < x else "baixo" if melhor[0][1] > y else "cima"
    
    for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
        nx, ny = x + dx, y + dy
        if (0 <= nx < largura and 0 <= ny < altura and 
            mapa[ny][nx] == 0 and (nx, ny) not in zonas_perigo):
            return "direita" if dx == 1 else "esquerda" if dx == -1 else "baixo" if dy == 1 else "cima"
    
    return "parado"
    
# Função auxiliar necessária
def distancia_manhattan(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


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
    print(f"🔧 andar_e_quebrar INICIADA - Player: {player['pos']}")
    
    pos = player["pos"]
    x, y = pos
    largura = len(mapa[0])
    altura = len(mapa)

    # Debug do mapa ao redor
    print(f"🗺️  Mapa ao redor de ({x},{y}):")
    for dy in range(-1, 2):
        linha = ""
        for dx in range(-1, 2):
            nx, ny = x + dx, y + dy
            if 0 <= nx < largura and 0 <= ny < altura:
                celula = mapa[ny][nx]
                simbolo = {
                    0: "·",  # chão
                    1: "█",  # bloco quebrável  
                    2: "▓",  # parede indestrutível
                    3: "B",  # powerup bomba
                    4: "F"   # powerup fogo
                }.get(celula, "?")
                linha += f"{simbolo} "
            else:
                linha += "X "
        print(f"    {linha}")
    
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
    CORREÇÃO: Agora pega o ID correto do player para evitar
    que ele se detecte como inimigo.
    """
    # Tenta pegar o ID de várias formas possíveis
    if hasattr(player, 'id'):
        player_id = player.id
    elif isinstance(player, dict) and 'id' in player:
        player_id = player['id']
    else:
        # Fallback: encontra o player na lista de jogadores pela posição
        player_pos = (player.grid_x if hasattr(player, 'grid_x') else player['pos'][0],
                      player.grid_y if hasattr(player, 'grid_y') else player['pos'][1])
        
        player_id = None
        for i, j in enumerate(jogadores):
            j_pos = (j.grid_x if hasattr(j, 'grid_x') else j['pos'][0],
                     j.grid_y if hasattr(j, 'grid_y') else j['pos'][1])
            if j_pos == player_pos:
                player_id = i
                break
        
        if player_id is None:
            player_id = 0
    
    print(f"🆔 Player ID detectado: {player_id}")

    info = {
        "player": {
            "id": player_id,
            "pos": (player.grid_x if hasattr(player, 'grid_x') else player['pos'][0],
                    player.grid_y if hasattr(player, 'grid_y') else player['pos'][1]),
            "ativo": player.ativo if hasattr(player, 'ativo') else player.get('ativo', True),
            "bomba_nivel": player.bomba_nivel if hasattr(player, 'bomba_nivel') else player.get('bomba_nivel', 1),
            "max_bombas": player.max_bombas if hasattr(player, 'max_bombas') else player.get('max_bombas', 1),
            "bombas_ativas": len(player.bombas) if hasattr(player, 'bombas') else player.get('bombas_ativas', 0)
        },
        "jogadores": [],
        "bombas": [],
        "powerups": [],
        "tem_bombas": False,
        "tem_powerups": False
    }

    # CORREÇÃO: Filtra o próprio jogador
    for i, j in enumerate(jogadores):
        if i == player_id:  # ← PULA A SI MESMO
            continue
            
        info["jogadores"].append({
            "id": i,
            "pos": (j.grid_x if hasattr(j, 'grid_x') else j['pos'][0],
                    j.grid_y if hasattr(j, 'grid_y') else j['pos'][1]),
            "ativo": j.ativo if hasattr(j, 'ativo') else j.get('ativo', True),
            "time": j.time if hasattr(j, 'time') else j.get('time', 0)
        })

    # Bombas
    for b in bombas:
        info["bombas"].append({
            "pos": (b.x if hasattr(b, 'x') else b['pos'][0],
                    b.y if hasattr(b, 'y') else b['pos'][1]),
            "nivel": b.nivel if hasattr(b, 'nivel') else b.get('nivel', 1),
            "explodida": b.explodida if hasattr(b, 'explodida') else b.get('explodida', False),
            "tempo_explosao": b.tempo_explosao if hasattr(b, 'tempo_explosao') else b.get('tempo_explosao', 4),
            "ativo": not (b.explodida if hasattr(b, 'explodida') else b.get('explodida', False)),
            "owner_id": getattr(b, "owner_id", None)
        })
    info["tem_bombas"] = len(info["bombas"]) > 0

    # PowerUps
    for y, linha in enumerate(mapa):
        for x, val in enumerate(linha):
            if val in [3, 4]:
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
    CORREÇÃO: Agora valida que não está calculando distância
    para si mesmo.
    """
    dados = {
        'perigo': 0,
        'mais_de_um_jogador_perto': 0,
        'oportunidade': 0,
        'neutro': 0,
        'player_com_powerup': 0,
        'powerup_existe': 0,
    }

    if not player.get('pos'):
        return dados

    px, py = player['pos']
    player_id = player['id']
    
    print(f"🔍 transformar_dados para player {player_id} em ({px},{py})")

    # CORREÇÃO: Filtra jogadores (já vem filtrado de extrair_informacoes)
    distancias_jogadores = []
    for j in jogadores:
        if not j['ativo'] or not j.get('pos'):
            continue
        
        # VALIDAÇÃO EXTRA: Confirma que não é o próprio jogador
        jx, jy = j['pos']
        if jx == px and jy == py:
            print(f"  ⚠️ Pulando jogador na mesma posição (ID: {j['id']})")
            continue
        
        d = distancia_manhattan(px, py, jx, jy)
        distancias_jogadores.append(d)
        print(f"  🎯 Jogador {j['id']} em {j['pos']} → distância: {d}")

    # Lógica de perigo
    jogadores_perto = [d for d in distancias_jogadores if d < 3]
    print(f"  📊 Jogadores perto (dist < 3): {jogadores_perto}")
    
    if len(jogadores_perto) >= 1:
        dados['perigo'] = 1
        print(f"  🚨 PERIGO DETECTADO: {len(jogadores_perto)} jogador(es) próximo(s)")
    if len(jogadores_perto) > 1:
        dados['mais_de_um_jogador_perto'] = 1

    # PowerUp
    if len(powerups) > 0:
        dados['powerup_existe'] = 1
        dist_p = min(
            distancia_manhattan(px, py, *p['pos'])
            for p in powerups if p.get('pos')
        )
        if dist_p <= limite_powerup and not dados['perigo']:
            dados['oportunidade'] = 1
    else:
        dados['powerup_existe'] = 0

    # Neutro
    if not dados['perigo'] and not dados['oportunidade']:
        dados['neutro'] = 1

    # Powerup do player
    if player.get('tem_powerup', False):
        dados['player_com_powerup'] = 1

    print(f"  📋 Dados finais: {dados}")
    return dados




def decidir_acao(player, mapa, jogadores, bombas, tempo_restante, pontos, hud_info, self_state):
    try:
        estado = extrair_informacoes(player, mapa, jogadores, bombas)
        print(f'\n🎮 Estado do Jogo - Player: {estado["player"]["pos"]}')
        
        exemploDadoReal = transformar_dados(
            estado["player"],
            estado["jogadores"],
            estado["bombas"],
            estado["powerups"],
            distancia_manhattan
        )

        print(f"📊 Dados para IA: {exemploDadoReal}")
        
        dataframeTreino = pd.DataFrame(dados_treinamento_fixos())
        dadoReal = pd.DataFrame([exemploDadoReal])

        result = arvorePredict(dadoReal, dataframeTreino)
        acao = result[0]
        print(f"🤖 Ação decidida pela IA: {acao}")

        # Dispatch das ações
        if acao == 'atacar_e_desviar':
            resultado = atacar_e_desviar(estado["player"], mapa, estado["jogadores"], estado["bombas"], estado["powerups"])
        elif acao == 'fugir':
            resultado = fugir()
        elif acao == 'pegar_powerUp':
            resultado = pegar_powerup(estado["player"], mapa, estado["powerups"], estado["bombas"])
        elif acao == 'andar_e_quebrar':
            resultado = andar_e_quebrar(estado["player"], mapa, estado["jogadores"], estado["bombas"])
        else:
            resultado = "parado"

        print(f"🎯 Ação final: {resultado}")
        return resultado

    except Exception as e:
        print(f"❌ Erro em decidir_acao: {e}")
        return "parado"
