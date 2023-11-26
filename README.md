# Snake Game AI

This is my project for the 24th MMU Hackerspace Hackathon. The goal is to train a neural network to play snake game using RL (Reinforcement Learning) with [Deep Q Learning](https://en.wikipedia.org/wiki/Q-learning#Deep_Q-learning) in [PyTorch](https://pytorch.org/). 

This snake game is playing on a 8x8 grid, because I didn't have much time to train for a 20x20 board. Feel free to change `self.N` parameter in the `environment.py` and retrain it.

## Snake Game Environment

I believe everyone know snake game pretty well. However, if you don't, here are some links that can help you:
- [Snake Game](https://playsnake.org/)
- [Wikipedia](https://en.wikipedia.org/wiki/Snake_(video_game_genre))

### Action Space

The agent has 3 discrete actions available, each denoted by a number:
- Go straight - 0
- Go left - 1
- Go right - 2

### Observation Space

The agent's observation space consists of a state vector with 11 **boolean** features:

`[d_s, d_l, d_r, m_d, m_r, m_u, m_l, a_d, a_u, a_r, a_l]`

- `d_s` indicates whether moving straight is dangerous
- `d_l` indicates whether moving left is dangerous
- `d_r` indicates whether moving right is dangerous
- `m_d` indicates whether the snake is moving down on the game board
- `m_r` indicates whether the snake is moving right on the game board
- `m_u` indicates whether the snake is moving up on the game board
- `m_l` indicates whether the snake is moving left on the game board
- `a_d` indicates whether the apple is below the snake
- `a_u` indicates whether the apple is above the snake
- `a_r` indicates whether the apple is to the right of the snake
- `a_l` indicates whether the apple is to the left of the snake

This state definition is inspired by this [article](https://medium.com/@nancy.q.zhou/teaching-an-ai-to-play-the-snake-game-using-reinforcement-learning-6d2a6e8f3b1c).

> Fun fact: I thought representing the state in this way is "cheating" because it looks like we're providing *extra* informations to the neural network. However, after knowing about the perfect information games and imperfect information games, I realized this is actually fine. Initially, I had the idea to use the grid as the state, let the neural network figure everything out by itself. Unfortunately, it didn't work out (basically, the snake just go in circle after 1/2 moves), and the hackathon presentation is happening in an hour, I had to start looking for an existing approach.

### Rewards

The snake game environment has the following reward system:
- Eating apple: 5 points
- Losing the game (Hitting the wall or self): -10 points

### Episode Termination

An episode ends when the snake hit the wall or itself.





