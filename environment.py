import random
import copy
import time
import os

class Environment:

    """
    For direction, we will denote it with 0, 1, 2, 3 (down, right, up, left)

    For action, we will denote it with 0, 1, 2:
    - 0: Step into current direction
    - 1: Step into the left of the current direction (also change direction)
    - 2: Step into the right of the current direction (also change direction)
    """


    def __init__(self):
        self.N = 8
        self.APPLE = self.N ** 2 + 1
        self.EMPTY_CELL = 0
        self.state_size = 11
        self.number_of_actions = 3
        self.reset()
    
    # Reset the game
    def reset(self):
        self.board = [self.N * [0] for _ in range(self.N)]
        self.board[0][self.N//2] = 3
        self.board[1][self.N//2] = 2
        self.board[2][self.N//2] = 1
        self.head = [2, self.N//2]
        self.direction = 0
        self.spawn_apple()

        return self.get_state()

    # Spawn an apple randomly and set apple's coordinate
    def spawn_apple(self):
        empty_cells = []

        for i in range(self.N):
            for j in range(self.N):
                if (self.board[i][j] == 0):
                    empty_cells.append([i, j])
        
        apple = empty_cells[random.randint(0, len(empty_cells)-1)]

        self.board[apple[0]][apple[1]] = self.APPLE
        self.apple_coord = apple

    # Calculate manhattan distance between a and b
    def calculate_distance(self, a, b):
        return abs(a[0]-b[0]) + abs(a[1] - b[1])
    
    def get_new_dir(self, action):
        # Choose direction
        if (action == 1):
            # left
            # 0 to 1
            # 2 to 3
            # 3 to 0
            # 1 to 2
            return (self.direction + 1) % 4
        elif (action == 2):
            # right
            # 0 to 3
            # 1 to 0
            # 2 to 1
            # 3 to 2
            return (self.direction - 1) % 4
        else:
            return self.direction

    # Return [temp_board, temp_head, isDanger]
    def move_temp(self, action):
        # Make a copy of the current board
        temp_board = copy.deepcopy(self.board)

        dir = self.get_new_dir(action)
        
        # Set temporary head
        dr = [1, 0, -1, 0]
        dc = [0, 1, 0, -1]
        temp_head = [self.head[0] + dr[dir], self.head[1] + dc[dir]]

        # If head is invalid, reward = -100
        if (
            temp_head[0] >= self.N or
            temp_head[0] < 0 or
            temp_head[1] >= self.N or
            temp_head[1] < 0
        ):
            return [dir, temp_board, temp_head, True]

        # Move snake body and find tail
        snake_length = 0
        tail = [0, 0]
        for i in range(self.N):
            for j in range(self.N):
                if (temp_board[i][j] > 0 and temp_board[i][j] <= self.N**2):
                    temp_board[i][j] += 1
                    if (temp_board[i][j] > snake_length):
                        snake_length = temp_board[i][j]
                        tail = [i, j]

        # Check if the new head has an apple, if not move tail
        if (temp_board[temp_head[0]][temp_head[1]] != self.APPLE):
            temp_board[tail[0]][tail[1]] = self.EMPTY_CELL
        

        # If head touches its body, reward = -100
        if (temp_board[temp_head[0]][temp_head[1]] not in [self.APPLE, self.EMPTY_CELL]):
            return [dir, temp_board, temp_head, True]

        # Set the new head on the grid
        temp_board[temp_head[0]][temp_head[1]] = 1

        return [dir, temp_board, temp_head, False]

    def get_state(self):
        return [
            # Danger S
            self.move_temp(0)[3],
            # Danger L
            self.move_temp(1)[3],
            # Danger R
            self.move_temp(2)[3],
            self.direction == 0,
            self.direction == 1,
            self.direction == 2,
            self.direction == 3,
            self.head[0] < self.apple_coord[0],
            self.head[0] > self.apple_coord[0],
            self.head[1] < self.apple_coord[1],
            self.head[1] > self.apple_coord[1]
        ]

    # Return [state, reward, done]
    def step(self, action):
        if (action >= 3):
            raise Exception("Action invalid")

        dir, temp_board, temp_head, done = self.move_temp(action)

        if done:
            return [self.get_state(), -10, True]

        self.board = temp_board
        self.head = temp_head
        self.direction = dir

        reward = 0
        # Spawn a new apple, because previous apple is taken by the new head
        if (temp_head == self.apple_coord):
            reward = 5
            self.spawn_apple()
        
        return [self.get_state(), reward, False]
            

    def render(self):
        for i in self.board:
            for j in i:
                item = ''
                if (j == 0):
                    item = '.'
                elif (j == self.APPLE):
                    item = '@'
                elif (j == 1):
                    item = 'o'
                else:
                    item = '*'
                print(item, end='')
            print()


def test_run():
    env = Environment()
    env.reset()

    env.render()
    while True:
        action = int(input())
        state, reward, done = env.step(action)
        os.system('cls')
        env.render()
        print(state, reward, done)
        if (done):
            break

test_run()