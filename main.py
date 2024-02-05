import time
import os
import torch
from torch import nn
from environment import Environment

env = Environment()
state_size = env.state_size
number_of_actions = env.number_of_actions

device = "cpu"

if torch.cuda.is_available():
    device = "cuda"
elif torch.backends.mps.is_available():
    device = "mps"

class QNetwork(nn.Module):
    def __init__(self):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(state_size, 256),
            nn.ReLU(),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, number_of_actions),
        )
        
    def forward(self, x):
        y = self.layers(x)
        return y

q_network = QNetwork().to(device)

def test():
    state = env.reset()
    total_points = 0
    
    q_network.load_state_dict(torch.load('./qnet_weights.pth'))

    env.render()
    time.sleep(0.5)
    while (True):
        state_tensor = torch.tensor([state])
        state_tensor = state_tensor.to(device).float()
        action = 0
        with torch.no_grad():
            action = torch.argmax(q_network(state_tensor)[0])
    
        next_state, reward, done = env.step(action)
        state = next_state
        total_points += reward

        os.system('cls')
        env.render()
        time.sleep(0.5)
        
        if done:
            return

test()