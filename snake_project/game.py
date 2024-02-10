import pygame
import random
import numpy as np

from snake_project.colors import WHITE, RED1, RED2, GREEN1, GREEN2, BLACK, GRAY1, GRAY2, BLUE1, BLUE2
from snake_project.misc import Direction, Point

pygame.init()
font = pygame.font.SysFont(None, 25)

class GameBase:
    
    def __init__(self, w=640, h=480, randomseed=1, speed=20, block_size=20,
                 neg_reward=-10, pos_reward=10,):
        
        #  Set random seed for replayability
        random.seed(randomseed)
        self.randomseed = int(randomseed)
        self.neg_reward = neg_reward
        self.pos_reward = pos_reward
        self.w = w
        self.h = h
        self.speed = int(speed)
        self.block_size = int(block_size)
        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        
        self.snake_color = 'green'
        self.body_1 = BLUE1
        self.body_2 = BLUE2
            
        # init game state
        self.setup_game()
        
    def setup_game(self, snake_color='green'):
        
        self.snake_color = snake_color
        random.seed(self.randomseed)
        # init game state
        self.direction = Direction.RIGHT

        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head,
                      Point(self.head.x-self.block_size, self.head.y),
                      Point(self.head.x-(2*self.block_size), self.head.y)]

        self.score = 0
        self.max_moves = 999
        self.food = None
        self.walls = []
        self.insert_walls()
        self.insert_food()
        self.frame_iteration = 0
        
    def insert_food(self):
        x = random.randint(0, (self.w-self.block_size )//self.block_size )*self.block_size 
        y = random.randint(0, (self.h-self.block_size )//self.block_size )*self.block_size
        self.food = Point(x, y)
        if self.food in self.walls:
            self.insert_food()
        if self.food in self.snake:
            self.insert_food()
            
    def insert_walls(self):
        
        #  Base walls
        low_x = 0
        high_x = self.w
        low_y = 0
        high_y = self.h
        for i in range(low_x, high_x, self.block_size):
            new_wall = Point(i, 0)
            self.walls.append(new_wall)
            new_wall = Point(i, high_y - self.block_size)
            self.walls.append(new_wall)
        for i in range(low_y, high_y, self.block_size):
            new_wall = Point(0, i)
            self.walls.append(new_wall)
            new_wall = Point(high_x - self.block_size, i)
            self.walls.append(new_wall)
        
        #  Random walls but not in snake
        #  And not on snake's line of sight
        inserted_walls = 0
        while not inserted_walls == 10:
            x = random.randint(0, (self.w-self.block_size )//self.block_size )*self.block_size 
            y = random.randint(0, (self.h-self.block_size )//self.block_size )*self.block_size
            new_wall = Point(x, y)
            if new_wall.y == self.h/2:
                continue
            if new_wall in self.snake:
                continue
            self.walls.append(new_wall)
            inserted_walls += 1
        return

    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head
        # hits boundary
        if pt.x > self.w - self.block_size or pt.x < 0 or pt.y > self.h - self.block_size or pt.y < 0:
            return True
        # hits itself
        if pt in self.snake[1:]:
            return True
        if pt in self.walls:
            return True
        return False
        
    def update_ui(self):
        
        #  Fill background
        self.display.fill(BLACK)
        
        if self.snake_color == 'green':
            self.body_1 = GREEN1
            self.body_2 = GREEN2
        else:
            self.body_1 = BLUE1
            self.body_2 = BLUE2
        
        #  Draw snake
        for pt in self.snake:
            pygame.draw.rect(self.display, self.body_1, 
                             pygame.Rect(pt.x, pt.y, self.block_size, self.block_size))
            pygame.draw.rect(self.display, self.body_2, 
                             pygame.Rect(pt.x+4, pt.y+4, 12, 12))
        
        #  Draw walls
        for w in self.walls:
            pygame.draw.rect(self.display, GRAY2, 
                             pygame.Rect(w.x, w.y, self.block_size, self.block_size))
            pygame.draw.rect(self.display, GRAY1, 
                             pygame.Rect(w.x+4, w.y+4, 12, 12))
            
        #  Draw food
        pygame.draw.rect(self.display, RED1, 
                         pygame.Rect(self.food.x, self.food.y, self.block_size, self.block_size))
        pygame.draw.rect(self.display, RED2, 
                         pygame.Rect(self.food.x+4, self.food.y+4, 12, 12))
        
        #  Draw score
        text_score = font.render("Score: " + str(self.score), True, WHITE)
        text_moves = font.render("Moves left: " + str(self.max_moves), True, WHITE)
        self.display.blit(text_score, [self.w/2 - 6 * self.block_size, 0])
        self.display.blit(text_moves, [self.w/2 + 2 * self.block_size, 0])
        pygame.display.flip()
        
    def input_from_human(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN:
                    self.direction = Direction.DOWN
        return
        
    def human_moves(self, direction):
        x = self.head.x
        y = self.head.y
        if direction == Direction.RIGHT:
            x += self.block_size
        elif direction == Direction.LEFT:
            x -= self.block_size
        elif direction == Direction.DOWN:
            y += self.block_size
        elif direction == Direction.UP:
            y -= self.block_size
        self.head = Point(x, y)
        return
        
    def ai_moves(self, action):
        # [straight, right, left]
        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)
        
        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx] # no change
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx] # right turn r -> d -> l -> u
        else: # [0, 0, 1]
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx] # left turn r -> u -> l -> d
        self.direction = new_dir
        self.human_moves(new_dir)
        return

        
    def play_step(self, action=None):
        
        self.max_moves -= 1
        
        if self.max_moves < 0:
            game_over = True
            reward = -20
            return reward, game_over, self.score
        
        #  If human moves take input from human
        #  otherwise process input from AI
        if not action:
            self.input_from_human()
            self.human_moves(self.direction)
        else:
            self.ai_moves(action=action)
        
        #  Make a move
        self.snake.insert(0, self.head)
        
        #  Check for collision
        reward = 0
        game_over = False
        if self.is_collision() or self.frame_iteration > 100*len(self.snake):
            game_over = True
            reward = self.neg_reward
            return reward, game_over, self.score
            
        #  Insert food if coords == head, else make move for render
        if self.head == self.food:
            self.score += 1
            reward = self.pos_reward
            self.insert_food()
        else:
            self.snake.pop()
        
        #  Update ui
        self.update_ui()
        self.clock.tick(self.speed)
        return reward, game_over, self.score
    
    def get_state(self):
        head = self.snake[0]
        point_l = Point(head.x - 20, head.y)
        point_r = Point(head.x + 20, head.y)
        point_u = Point(head.x, head.y - 20)
        point_d = Point(head.x, head.y + 20)
        
        dir_l = self.direction == Direction.LEFT
        dir_r = self.direction == Direction.RIGHT
        dir_u = self.direction == Direction.UP
        dir_d = self.direction == Direction.DOWN

        state = [
            # Danger straight
            (dir_r and self.is_collision(point_r)) or 
            (dir_l and self.is_collision(point_l)) or 
            (dir_u and self.is_collision(point_u)) or 
            (dir_d and self.is_collision(point_d)),

            # Danger right
            (dir_u and self.is_collision(point_r)) or 
            (dir_d and self.is_collision(point_l)) or 
            (dir_l and self.is_collision(point_u)) or 
            (dir_r and self.is_collision(point_d)),

            # Danger left
            (dir_d and self.is_collision(point_r)) or 
            (dir_u and self.is_collision(point_l)) or 
            (dir_r and self.is_collision(point_u)) or 
            (dir_l and self.is_collision(point_d)),
            
            # Move direction
            dir_l,
            dir_r,
            dir_u,
            dir_d,
            
            # Food location 
            self.food.x < self.head.x,  # food left
            self.food.x > self.head.x,  # food right
            self.food.y < self.head.y,  # food up
            self.food.y > self.head.y  # food down
            ]
        return np.array(state, dtype=int)
        