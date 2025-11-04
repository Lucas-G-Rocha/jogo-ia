import random
from sklearn.tree import DecisionTreeClassifier;
import pandas as pd;
import math
import json


indice_sequenciaDeAcoes = 0
sequenciaDeAcoes = []

ACOES = ["bomba", "atacar", "fugir", "afastar", "aproximar", "pegar"]
DIRECAO = ["cima", "baixo", "esquerda", "direita", "parado"]

# calculo de distancias

def calcular_distancia(pos1, pos2):
    return math.sqrt((pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2)
  

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

# Nó de decisão

def decidir_acao(player, mapa, jogadores, bombas, tempo_restante, pontos, hud_info, self_state):
    # Gera um contexto real
    dado_real = gerar_dado_real()
    
    # Faz o modelo prever a ação
    
    TrainningData = gerar_dados_treinamento(100)
    model = arvoreDeDecisoes(TrainningData)
    
    # Correção: usar apenas as colunas de treino sem a coluna de rótulo
    X_real = dado_real[TrainningData.columns[:-1]]
    
    acao_prevista = model.predict(X_real)[0]

    print(f"Ação prevista pela IA: {acao_prevista}")

    # Executa a ação prevista
    
    direcao = executar_acao(acao_prevista, player, mapa, jogadores, bombas)
    return direcao

def fugir(player, mapa, jogadores, bombas):
    print("fugindo do perigo")
    return random.choice(DIRECAO)

def atacar(player, mapa, jogadores):
    print("atacando jogador")
    return random.choice(DIRECAO)

def buscar_powerUp(player, mapa):
    print("procurando power-up")
    return random.choice(DIRECAO)

def quebrar_parede(player, mapa):
    print("quebrando parede")
    return random.choice(DIRECAO)

def aproximar(player, mapa, jogadores):
    print("aproximando do inimigo")
    return random.choice(DIRECAO)

#executar ação 

def executar_acao(acao, player, mapa, jogadores, bombas):
    if acao == "fugir":
        return fugir(player, mapa, jogadores, bombas)
    elif acao == "atacar":
        return atacar(player, mapa, jogadores)
    elif acao == "pegar_item":
        return buscar_powerUp(player, mapa)
    elif acao == "quebrarBloco":
        return quebrar_parede(player, mapa)
    elif acao == "aproximar":
        return aproximar(player, mapa, jogadores)
    else:
        return "parado"


def arvoreDeDecisoes(TrainningData):
    X_treino = TrainningData.iloc[:, :-1]
    Y_treino = TrainningData.iloc[:, -1]
    
    model = DecisionTreeClassifier()
    
    model.fit(X_treino, Y_treino)
    
    return model

def arvorePredict(realData):
    TrainningData = gerar_dados_treinamento(50)
    model = arvoreDeDecisoes(TrainningData)
    
    # Correção: usar apenas as colunas de treino sem a coluna de rótulo
    X_real = realData[TrainningData.columns[:-1]]
    
    result = model.predict(X_real)
    print("\n\n arvorePredict \n\n")
    print(result)
    
#dados de treinamento

def gerar_dados_treinamento(qtd_exemplos=30):
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

        # Ações possíveis (por enquanto só como rótulos de exemplo)
        funcao = random.choice(["atacar", "fugir", "pegar_item", "quebrarBloco", "aproximar"])

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
            "self_state": self_state,
            "funcao": funcao
        })

    dataframe = pd.DataFrame(dados)
    print("\n\ngerar_Dado_Treinamento \n\n")
    print(dataframe)
    return dataframe


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
    
dadoReal = gerar_dado_real()

arvorePredict(dadoReal)

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