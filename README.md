# 🤖 Projeto de Inteligência Artificial – Competição de IAs (Bomberman-like)

Este projeto foi desenvolvido para a disciplina de **Inteligência Artificial** da faculdade.  
O professor forneceu a estrutura base do jogo, e o desafio dos alunos era implementar uma **IA capaz de controlar um dos jogadores**, tomando decisões **a cada frame** da partida.

O objetivo final era realizar uma **competição entre as IAs criadas pela turma**, avaliando qual delas conseguia:

- 🛡️ sobreviver mais tempo  
- ⚔️ atacar com estratégia  
- 💥 evitar explosões  
- 🧠 demonstrar o comportamento mais inteligente dentro das regras do jogo  

---

## 🧠 Ideia da IA Desenvolvida

Foi implementada uma **árvore de decisão classificatória** (scikit-learn) para que a IA pudesse:

- analisar o estado atual do jogo  
- classificar a situação em uma categoria  
- executar a função apropriada (fugir, atacar, pegar power-up, quebrar blocos etc.)

Cada função contém sua própria lógica de movimento e uso de bombas, garantindo **modularidade e clareza** no comportamento do agente.

---

## 🗂️ Exemplo de features utilizadas no treinamento

```json
{
  "perigo": 0,
  "mais_de_um_jogador_perto": 1,
  "oportunidade": 0,
  "funcao": "andar_e_quebrar",
  "neutro": 1,
  "player_com_powerup": 1,
  "powerup_existe": 1
}
```

Essas variáveis — combinadas em diferentes cenários — ajudaram a árvore de decisão a determinar **qual ação estratégica** era mais adequada em cada frame.

---

## 🤖 Sobre a IA

A IA foi projetada para:

- analisar o ambiente do jogo a cada frame  
- tomar **exatamente uma** ação entre:  
  **cima, baixo, esquerda, direita, parado, bomba**  
- evitar suicídio ao plantar bombas  
- prever explosões e fugir de zonas de risco  
- encontrar rotas de fuga seguras  
- identificar oportunidades de ataque  
- decidir entre avançar ou recuar  
- coletar power-ups com segurança  
- navegar quebrando blocos quando necessário  

---

## 🎯 Prioridades da IA

1. 🛡️ Sobrevivência  
2. 🔍 Exploração e coleta de power-ups  
3. ⚔️ Oportunidades ofensivas  

---

## 🛠️ Tecnologias e Estrutura

- **Python** – implementação da IA  
- **scikit-learn** – árvore de decisão  
- **pandas** – criação de DataFrames  
- **Ambiente fornecido pelo professor**  
- Simulação em **grid (matriz)**  
- Lógica de explosões, colisões e áreas de perigo  
- Análise local de risco e busca por rotas seguras  

---

## 🔎 Observações Importantes

Projeto desenvolvido com **auxílio do ChatGPT** durante o processo de experimentação, prototipagem e otimização da lógica da IA — portanto, o código não reflete habilidades e/ou conhecimentos dos quais posso tomar plena propriedade, incluindo a linguagem Python, na qual possuo apenas conhecimento básico.

---

Sinta-se à vontade para explorar o código, refinar a IA ou testar novas abordagens de tomada de decisão!  
🚀🤖🎮
