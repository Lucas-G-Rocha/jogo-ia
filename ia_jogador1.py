import random

indice_sequenciaDeAcoes = 0
sequenciaDeAcoes = []

ACOES = ["bomba", "atacar, fugir, afastar, aproximar, pegar"]
DIRECAO = ["cima", "baixo", "esquerda", "direita", "parado"]
def decidir_acao(player, mapa, jogadores, bombas, tempo_restante, pontos, hud_info, self_state):
    return random.choice(ACOES)



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
