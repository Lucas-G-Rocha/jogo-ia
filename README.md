# jogo-ia

🧩 Estrutura do DataFrame de Treinamento — “Modelo Cognitivo de Decisão”

Cada linha representa um instante de decisão do jogador (self).
Cada coluna é uma “percepção” ou “situação interpretada” do ambiente.

🔹 Contexto Espacial
Coluna	Tipo	Descrição	Exemplo
player_x, player_y	int	Posição atual do jogador no grid.	(4,7)
tile_seguro	bool/int (0/1)	1 se o tile atual não está em raio de explosão iminente.	1
zona_segura_proxima	float	Distância até o tile seguro mais próximo.	2.3
bloqueado	bool	1 se não há para onde mover (preso por paredes/bombas).	0
💣 Percepção de Perigo
Coluna	Tipo	Descrição	Exemplo
bomba_mais_proxima_dist	float	Distância até a bomba mais próxima.	1.41
bomba_mais_proxima_raio	int	Raio de explosão da bomba mais próxima.	3
esta_no_raio_da_bomba	bool	1 se o jogador está dentro do raio da bomba mais próxima.	1
qtd_bombas_visiveis	int	Quantas bombas estão ativas e visíveis no mapa.	3
tempo_explosao_mais_proxima	float	Tempo restante pra bomba mais próxima explodir.	0.8
risco_morte	float	Índice calculado (ex: baseado na distância e tempo) de perigo imediato.	0.92
⚔️ Percepção de Inimigos
Coluna	Tipo	Descrição	Exemplo
inimigo_mais_proximo_dist	float	Distância até o inimigo mais próximo.	3.16
inimigo_mais_proximo_dir	str	Direção do inimigo mais próximo (ex: "esquerda", "baixo").	"direita"
inimigo_vindo_na_direcao	bool	1 se o inimigo mais próximo está se movendo na direção do player.	0
qtd_inimigos_visiveis	int	Quantos inimigos estão dentro do campo de visão.	2
vulnerabilidade_inimigo	float	Quão vulnerável está o inimigo (baseado em se está preso, parado etc).	0.6
🎁 Percepção de Oportunidade
Coluna	Tipo	Descrição	Exemplo
powerup_mais_proximo_dist	float	Distância até o power-up mais próximo.	4.47
powerup_acessivel	bool	1 se o caminho até o power-up é livre de bombas/barreiras.	1
qtd_powerups_visiveis	int	Quantos power-ups estão visíveis no mapa.	1
valor_powerup_proximo	int	Valor estratégico (por ex: bomba extra = 2, velocidade = 1, fogo = 3).	3
ganho_potencial	float	Pontuação esperada caso pegue o power-up.	0.75
🧱 Ambiente e Mobilidade
Coluna	Tipo	Descrição	Exemplo
qtd_blocos_destrutiveis_perto	int	Quantos blocos quebráveis estão em até 3 tiles de distância.	4
rota_de_fuga_disponivel	bool	1 se há caminho livre para fugir do raio de uma bomba.	1
caminho_livre_para_inimigo	bool	1 se há caminho direto até o inimigo mais próximo.	0
mapa_aberto	float	Índice de liberdade (proporção de espaços livres ao redor).	0.7
🕒 Tempo e Ritmo
Coluna	Tipo	Descrição	Exemplo
tempo_restante	float	Tempo restante da partida.	175.9
fase_final	bool	1 se o tempo está < 60s.	0
pressao_temporal	float	Índice que mede urgência (pode influenciar IA agressiva).	0.3
⭐ Status Geral (Self)
Coluna	Tipo	Descrição	Exemplo
bombas_ativas	int	Quantas bombas do player estão ativas.	1
max_bombas	int	Quantas bombas ele pode plantar.	2
bomba_nivel	int	Nível de explosão.	1
velocidade	float	Velocidade atual.	480
pontos	int	Pontuação atual.	320
modo_agressivo	bool	Se está num estado ofensivo (ex: perseguindo alguém).	0
🧠 Variáveis Derivadas / de Julgamento

Essas são as que imitam o raciocínio humano, criadas a partir das outras.

Coluna	Tipo	Descrição	Exemplo
decisao_sugerida	str	Rótulo da ação que deve ser aprendida (alvo da IA).	“fugir”, “plantar_bomba”, “pegar_item”
grau_de_perigo	float	Média ponderada entre proximidade de bomba e inimigos.	0.85
grau_de_oportunidade	float	Combina distância até power-ups, blocos destrutíveis, etc.	0.42
grau_de_vantagem	float	Avalia se o player está em situação melhor que inimigos próximos.	0.58
contexto_estrategico	str	Rótulo simplificado do contexto geral (“perigo”, “ataque”, “coleta”).	“perigo”
🧩 Exemplo visual simplificado de uma linha no DataFrame:
player_x	player_y	tile_seguro	bomba_mais_proxima_dist	inimigo_mais_proximo_dist	powerup_mais_proximo_dist	grau_de_perigo	grau_de_oportunidade	decisao_sugerida
4	7	0	1.41	3.16	4.47	0.9	0.3	“fugir”

Esse formato te permite:

Treinar uma IA mais “humana”, que entende contextos, não só coordenadas.

Adicionar novas percepções facilmente, sem mudar a lógica base.

Gerar dados reais durante gameplay, para reinforcement learning no futuro.

























DADOS VINDOS DO LOG DOS OBJETOS PLAYER, BOMBAS E ETC...:

===== ESTADO ATUAL DO JOGO =====

🧍 Player:
  grid_x: 0
  grid_y: 0
  pixel_x: 0
  pixel_y: 0
  dest_x: 0
  dest_y: 0
  tipo: ia
  time: 0
  frames: [<Surface(48x48x32 SW)>, <Surface(48x48x32 SW)>, <Surface(48x48x32 SW)>, <Surface(48x48x32 SW)>, <Surface(48x48x32 SW)>, <Surface(48x48x32 SW)>, <Surface(48x48x32 SW)>, <Surface(48x48x32 SW)>, <Surface(48x48x32 SW)>, <Surface(48x48x32 SW)>, <Surface(48x48x32 SW)>, <Surface(48x48x32 SW)>]
  anim_frame: 0
  anim_timer: 0
  anim_interval: 0.15
  ultima_direcao: baixo
  movendo: False
  tempo_mov: 0
  velocidade: 480.0
  max_bombas: 1
  bombas: [<__main__.Bomba object at 0x000001A9E2E5B440>]
  bomba_nivel: 1
  ativo: True
  ia_fn: <function decidir_acao at 0x000001A9E2B7F7E0>

🗺️ Mapa:
  [0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0]
  [0, 2, 1, 2, 0, 2, 0, 2, 1, 2, 1, 2, 0]
  [1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1]
  [0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
  [0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1]
  [1, 2, 0, 2, 1, 2, 0, 2, 1, 2, 1, 2, 1]
  [1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1]
  [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
  [0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]
  [0, 2, 1, 2, 0, 2, 1, 2, 0, 2, 0, 2, 0]
  [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0]

👥 Jogadores:
  Jogador 1:
    grid_x: 0
    grid_y: 0
    pixel_x: 0
    pixel_y: 0
    dest_x: 0
    dest_y: 0
    tipo: ia
    time: 0
    frames: [<Surface(48x48x32 SW)>, <Surface(48x48x32 SW)>, <Surface(48x48x32 SW)>, <Surface(48x48x32 SW)>, <Surface(48x48x32 SW)>, <Surface(48x48x32 SW)>, <Surface(48x48x32 SW)>, <Surface(48x48x32 SW)>, <Surface(48x48x32 SW)>, <Surface(48x48x32 SW)>, <Surface(48x48x32 SW)>, <Surface(48x48x32 SW)>]
    anim_frame: 0
    anim_timer: 0
    anim_interval: 0.15
    ultima_direcao: baixo
    movendo: False
    tempo_mov: 0
    velocidade: 480.0
    max_bombas: 1
    bombas: [<__main__.Bomba object at 0x000001A9E2E5B440>]
    bomba_nivel: 1
    ativo: True
    ia_fn: <function decidir_acao at 0x000001A9E2B7F7E0>
  Jogador 2:
    grid_x: 11
    grid_y: 0
    pixel_x: 528
    pixel_y: 0
    dest_x: 528
    dest_y: 0
    tipo: ia
    time: 1
    frames: [<Surface(48x48x32 SW)>, <Surface(48x48x32 SW)>, <Surface(48x48x32 SW)>, <Surface(48x48x32 SW)>, <Surface(48x48x32 SW)>, <Surface(48x48x32 SW)>, <Surface(48x48x32 SW)>, <Surface(48x48x32 SW)>, <Surface(48x48x32 SW)>, <Surface(48x48x32 SW)>, <Surface(48x48x32 SW)>, <Surface(48x48x32 SW)>]
    anim_frame: 0
    anim_timer: 0
    anim_interval: 0.15
    ultima_direcao: esquerda
    movendo: False
    tempo_mov: 0.115
    velocidade: 480.0
    max_bombas: 1
    bombas: [<__main__.Bomba object at 0x000001A9E2E70350>]
    bomba_nivel: 1
    ativo: True
    ia_fn: <function decidir_acao at 0x000001A9E2BBA2A0>
  Jogador 3:
    grid_x: 1
    grid_y: 10
    pixel_x: 48
    pixel_y: 480
    dest_x: 48
    dest_y: 480
    tipo: ia
    time: 1
    frames: [<Surface(48x48x32 SW)>, <Surface(48x48x32 SW)>, <Surface(48x48x32 SW)>, <Surface(48x48x32 SW)>, <Surface(48x48x32 SW)>, <Surface(48x48x32 SW)>, <Surface(48x48x32 SW)>, <Surface(48x48x32 SW)>, <Surface(48x48x32 SW)>, <Surface(48x48x32 SW)>, <Surface(48x48x32 SW)>, <Surface(48x48x32 SW)>]
    anim_frame: 0
    anim_timer: 6
    anim_interval: 0.15
    ultima_direcao: direita
    movendo: False
    tempo_mov: 0.1
    velocidade: 480.0
    max_bombas: 1
    bombas: [<__main__.Bomba object at 0x000001A9E2E70B00>]
    bomba_nivel: 1
    ativo: True
    ia_fn: <function decidir_acao at 0x000001A9E2E4BEC0>
  Jogador 4:
    grid_x: 12
    grid_y: 9
    pixel_x: 576
    pixel_y: 432
    dest_x: 576
    dest_y: 432
    tipo: ia
    time: 0
    frames: [<Surface(48x48x32 SW)>, <Surface(48x48x32 SW)>, <Surface(48x48x32 SW)>, <Surface(48x48x32 SW)>, <Surface(48x48x32 SW)>, <Surface(48x48x32 SW)>, <Surface(48x48x32 SW)>, <Surface(48x48x32 SW)>, <Surface(48x48x32 SW)>, <Surface(48x48x32 SW)>, <Surface(48x48x32 SW)>, <Surface(48x48x32 SW)>]
    anim_frame: 0
    anim_timer: 1
    anim_interval: 0.15
    ultima_direcao: baixo
    movendo: False
    tempo_mov: 0.116
    velocidade: 480.0
    max_bombas: 1
    bombas: [<__main__.Bomba object at 0x000001A9E2E71A30>]
    bomba_nivel: 1
    ativo: True
    ia_fn: <function decidir_acao at 0x000001A9E2E61A80>

💣 Bombas:
  Bomba 1:
    x: 0
    y: 0
    tempo_explosao: 0.0030000000000079963
    explodida: False
    nivel: 1
    tempo_fogo: 0
    fogo: []
    dono: <__main__.Player object at 0x000001A9FFD4E450>
    anim_frame: 1
    anim_timer: 0.017
    anim_interval: 0.2
  Bomba 2:
    x: 0
    y: 10
    tempo_explosao: 0.019000000000008108
    explodida: False
    nivel: 1
    tempo_fogo: 0
    fogo: []
    dono: <__main__.Player object at 0x000001A9FFCD85F0>
    anim_frame: 1
    anim_timer: 0.017
    anim_interval: 0.2
  Bomba 3:
    x: 11
    y: 10
    tempo_explosao: 0.12000000000000778
    explodida: False
    nivel: 1
    tempo_fogo: 0
    fogo: []
    dono: <__main__.Player object at 0x000001A9E2E598E0>
    anim_frame: 0
    anim_timer: 0.11800000000000001
    anim_interval: 0.2
  Bomba 4:
    x: 12
    y: 1
    tempo_explosao: 0.1520000000000079
    explodida: False
    nivel: 1
    tempo_fogo: 0
    fogo: []
    dono: <__main__.Player object at 0x000001A9E2B92300>
    anim_frame: 0
    anim_timer: 0.068
    anim_interval: 0.2

⏱️ Tempo restante: 175.986

⭐ Pontos: [0, 0, 0, 0, 0]

🧭 HUD info:
  tile_size: 48
  rows: 11
  cols: 13
  tempo_movimento: 0.1
  tempo_explosao: 4
  tempo_fogo: 0.5
  max_bombas: 5

🧩 Self state:
  grid_x: 0
  grid_y: 0
  max_bombas: 1
  bombas_ativas: 1
  bomba_nivel: 1
  ativo: True

================================

Jogador 1 morreu!
Jogador 3 morreu!
Jogador 4 morreu!

[Done] exited with code=0 in 7.833 seconds

























INFORMAÇÕES IMPORTANTES(VIA CHAT GPT):

🎯 Principais categorias e o que dá pra extrair do teu log
🧍 1. Estado do jogador (self)

Essencial para qualquer análise, especialmente pra IA.

grid_x, grid_y → posição no mapa.

ativo → se o jogador está vivo.

bombas_ativas, max_bombas → limita ações (pode ou não plantar outra bomba).

bomba_nivel → raio/poder da explosão.

velocidade, movendo → úteis pra prever deslocamento.

Usos:

movimentação segura, decisão de plantar bomba, fuga de explosão, coleta de power-up etc.

👥 2. Estado dos outros jogadores

posição (grid_x, grid_y)

ativo (vivo ou morto)

bombas (quantas têm ativas)

ultima_direcao (tendência de movimento)

time (caso haja times)

Usos:

prever ameaças, localizar inimigos vivos, evitar colisão, priorizar alvos, balancear pontuação.

💣 3. Bombas

posição (x, y)

tempo_explosao (quanto falta pra explodir)

explodida (estado atual)

nivel (raio da explosão)

dono (pra associar ao jogador)

Usos:

prever zonas de perigo, IA de fuga, prever mortes futuras, avaliar risco, detecção de “corrente” (bomba aciona bomba).

🗺️ 4. Mapa

distribuição de blocos (0 = vazio, 1 = parede destrutível?, 2 = obstáculo?)

permite saber onde é acessível e onde não dá pra andar.

Usos:

pathfinding (A*, BFS etc), visão do ambiente, geração de rotas seguras, planejamento de ataque/defesa.

⏱️ 5. Tempo restante

Define quanto tempo falta pra acabar a rodada.

Usos:

IA agressiva no fim da partida, aceleração de ritmo, contagem regressiva de round.

⭐ 6. Pontuação

Estado global de pontuação entre os times ou jogadores.

Usos:

análise de vantagem, critérios de vitória, HUD.

🧭 7. HUD info

Dados fixos de configuração: tile_size, tempo_movimento, tempo_explosao, max_bombas etc.

Usos:

ajuste de cálculos físicos e temporais, renderização, sincronização de lógica.

⚙️ Em resumo
Categoria	Informação Útil	Serve pra
Player (self)	posição, bombas, ativo	decisão imediata
Jogadores	posição, ativo, direção	IA tática e alvo
Bombas	posição, tempo, nível	zonas de risco
Mapa	layout	navegação, colisão
Tempo	segundos restantes	urgência da rodada
Pontuação	valores	HUD e fim de jogo
HUD info	configs	cálculo base, visual