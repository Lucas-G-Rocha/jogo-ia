import random
from sklearn.tree import DecisionTreeClassifier;
import pandas as pd;
import math
import json


indice_sequenciaDeAcoes = 0
sequenciaDeAcoes = []

ACOES = ["bomba", "atacar, fugir, afastar, aproximar, pegar"]
DIRECAO = ["cima", "baixo", "esquerda", "direita", "parado"]
def decidir_acao(player, mapa, jogadores, bombas, tempo_restante, pontos, hud_info, self_state):
    
    
    return random.choice(ACOES)





def arvoreDeDecisoes(TrainningData):
    X_treino = TrainningData.iloc[:, :-1]
    Y_treino = TrainningData.iloc[:, -1]
    
    model = DecisionTreeClassifier()
    
    model.fit(X_treino, Y_treino)
    
    return model

def arvorePredict(realData):
    TrainningData = gerar_dados_treinamento(50)
    model = arvoreDeDecisoes(TrainningData)
    result = model.predict(realData)
    print("\n\n arvorePredict \n\n")
    print(result)




def gerar_dados_treinamento(
qtd_exemplos=30,
funcao="fugir",
perigo=1,
oportunidade=0,
neutro=0,
player_index=1,
limite_distancia=5,
limite_powerup=12,
bomba_existe=1,
bomba_player=1
):
  """
  Gera dados sintéticos controlados apenas com distâncias, para treinar IA.

  ```
  Bombas respeitam a distância dos jogadores. Se bomba_player=1, o player terá bomba próxima.
  Se a distância do jogador for 0 e bomba_player=0, a bomba correspondente é 0.
  """

  if player_index not in [1, 2, 3, 4]:
      raise ValueError("player_index deve ser um número entre 1 e 4.")

  dados = []

  for _ in range(qtd_exemplos):
      # --- DISTÂNCIAS ALEATÓRIAS PARA OS JOGADORES ---
      dist_jogadores = {}
      jogadores_perto = 0
      for i in range(1, 5):
          if i == player_index:
              dist_jogadores[i] = 0
              continue
          dist = random.randint(1, limite_distancia) if perigo else random.randint(limite_distancia+1, limite_distancia*2)
          dist_jogadores[i] = dist
          if dist <= limite_distancia:
              jogadores_perto += 1

      mais_de_um_jogador_perto = 1 if jogadores_perto > 1 else 0

      # --- DISTÂNCIAS ALEATÓRIAS PARA BOMBAS (respeitando distâncias dos jogadores) ---
      dist_bombas = {}
      if bomba_existe:
          for i in range(1, 5):
              if i == player_index:
                  if bomba_player == 1:
                      # Player com bomba ativa → gera bomba próxima
                      dist_bombas[i] = random.randint(1, min(3, limite_distancia))
                  else:
                      # Player sem bomba ativa → bomba não existe
                      dist_bombas[i] = 0
              else:
                  # Para os outros jogadores, bomba próxima à distância deles ±2
                  dist_jog = dist_jogadores[i]
                  dist_bombas[i] = max(1, min(dist_jog + random.randint(-2, 2), limite_distancia*2))
      else:
          for i in range(1, 5):
              dist_bombas[i] = 0

      # --- POWER UP ---
      powerup_existe = random.choice([0, 1])
      dist_powerup = random.randint(1, limite_powerup) if powerup_existe else 0

      # --- PLAYER COM POWERUP ATIVO? ---
      player_com_powerup = random.choice([0, 1])

      # --- MONTA LINHA DO DATASET ---
      linha = {
          "dist_jogador1": dist_jogadores[1],
          "dist_jogador2": dist_jogadores[2],
          "dist_jogador3": dist_jogadores[3],
          "dist_jogador4": dist_jogadores[4],

          "dist_bomba1": dist_bombas[1],
          "dist_bomba2": dist_bombas[2],
          "dist_bomba3": dist_bombas[3],
          "dist_bomba4": dist_bombas[4],

          "bomba_player": bomba_player,
          "bomba_existe": bomba_existe,

          "powerup_existe": powerup_existe,
          "dist_powerup": dist_powerup,
          "player_com_powerup": player_com_powerup,

          "perigo": perigo,
          "mais_de_um_jogador_perto": mais_de_um_jogador_perto,
          "oportunidade": oportunidade,
          "neutro": neutro,

          "funcao": funcao
      }

      dados.append(linha)

  df = pd.DataFrame(dados)
  print(f"\n--- Dados de treinamento gerados ({qtd_exemplos} exemplos | Player: {player_index}) ---\n")
  print(df.to_string(index=False))
  return df


    








def gerar_dado_real(qtd_exemplos=1):
    dados = []

    for _ in range(qtd_exemplos):
        # Posições no mapa (13x11)
        player_x, player_y = random.randint(0, 12), random.randint(0, 10)
        inimigo_x, inimigo_y = random.randint(0, 12), random.randint(0, 10)
        bomba_x, bomba_y = random.randint(0, 12), random.randint(0, 10)

        # Distâncias
        distancia_inimigo = round(math.dist([player_x, player_y], [inimigo_x, inimigo_y]), 2)
        distancia_bomba = round(math.dist([player_x, player_y], [bomba_x, bomba_y]), 2)

        # Outros fatores do ambiente
        num_bombas_ativas = random.randint(0, 5)
        tempo_restante = random.randint(0, 300)
        pontos = random.randint(0, 1000)
        hud_info = random.randint(0, 3)
        self_state = random.randint(0, 5)


        # Monta uma linha
        dados.append({
            "player_x": player_x,
            "player_y": player_y,
            "inimigo_x": inimigo_x,
            "inimigo_y": inimigo_y,
            "bomba_x": bomba_x,
            "bomba_y": bomba_y,
            "distancia_inimigo": distancia_inimigo,
            "distancia_bomba": distancia_bomba,
            "num_bombas_ativas": num_bombas_ativas,
            "tempo_restante": tempo_restante,
            "pontos": pontos,
            "hud_info": hud_info,
            "self_state": self_state
        })
    dataframe = pd.DataFrame(dados)
    print("\n\ngerar_Dado_Real \n\n")
    print(dataframe)
    return dataframe
    
# dadoReal = gerar_dado_real()

# arvorePredict(dadoReal)

def exibir_estado_jogo(player, mapa, jogadores, bombas, tempo_restante, pontos, hud_info, self_state):
    print("===== ESTADO ATUAL DO JOGO =====\n")

    # Player
    print("🧍 Player:")
    if hasattr(player, '__dict__'):
        for k, v in player.__dict__.items():
            print(f"  {k}: {v}")
    else:
        print(f"  {player}")

    # Mapa
    print("\n🗺️ Mapa:")
    for linha in mapa:
        print(" ", linha)

    # Jogadores
    print("\n👥 Jogadores:")
    for i, j in enumerate(jogadores):
        print(f"  Jogador {i + 1}:")
        if hasattr(j, '__dict__'):
            for k, v in j.__dict__.items():
                print(f"    {k}: {v}")
        else:
            print(f"    {j}")

    # Bombas
    print("\n💣 Bombas:")
    for i, b in enumerate(bombas):
        print(f"  Bomba {i + 1}:")
        if hasattr(b, '__dict__'):
            for k, v in b.__dict__.items():
                print(f"    {k}: {v}")
        else:
            print(f"    {b}")

    # Tempo restante
    print(f"\n⏱️ Tempo restante: {tempo_restante:.3f}")

    # Pontos
    print(f"\n⭐ Pontos: {pontos}")

    # HUD info
    print("\n🧭 HUD info:")
    for k, v in hud_info.items():
        print(f"  {k}: {v}")

    # Self state
    print("\n🧩 Self state:")
    for k, v in self_state.items():
        print(f"  {k}: {v}")

    print("\n================================\n")
    
    
def distancia_manhattan(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

    
gerar_dados_treinamento(
    qtd_exemplos=30,
    funcao="fugir",
    perigo=1,
    oportunidade=0,
    neutro=0,
    player_index=1,
    limite_distancia=5,
    limite_powerup=12,
    bomba_existe=1,
    bomba_player=0)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
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





