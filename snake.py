import pygame
import random

class SnakeGame:
    def __init__(self, width=400, height=400, grid_size=20):
        # Initialize pygame
        pygame.init()

        # Constants
        self.WIDTH = width
        self.HEIGHT = height
        self.GRID_SIZE = grid_size
        self.GRID_WIDTH = width // grid_size
        self.GRID_HEIGHT = height // grid_size
        self.SNAKE_COLOR = (0, 0, 0)
        self.FOOD_COLOR = (255, 0, 0)
        self.BACKGROUND_COLOR = (255, 255, 255)
        self.food_eat=0
        # Create screen
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption('Snake Game')
        self.font = pygame.font.Font(None, 36)  # Initialize font

        self.reset_game()

    def reset_game(self):
        self.snake = [(self.GRID_WIDTH // 2, self.GRID_HEIGHT // 2)]
        self.direction = (1, 0)  
        self.score = 0
        self.food = self.place_food() 
        self.clock = pygame.time.Clock()
        self.food_eat = 0
        return self.get_state()
    
    def move_snake(self):
        head_x, head_y = self.snake[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])

        # Insert the new head into the snake
        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.score += 1  
            self.food = self.place_food()
        else:
            self.snake.pop()  
            
    def step(self, action):
        prev_distance_to_food = self.get_distance_to_food()

        if action == 0 and self.direction != (0, 1):  # Up
            self.direction = (0, -1)
        elif action == 1 and self.direction != (0, -1):  # Down
            self.direction = (0, 1)
        elif action == 2 and self.direction != (1, 0):  # Left
            self.direction = (-1, 0)
        elif action == 3 and self.direction != (-1, 0):  # Right
            self.direction = (1, 0)

        head_x, head_y = self.snake[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])
        self.snake.insert(0, new_head)

        reward = 0
        done = False
        new_distance_to_food = self.get_distance_to_food()
        self.food_eat=0
        
        if self.check_collision():
            done = True
            reward = -50
        elif new_head == self.food:
            reward += 30
            self.food_eat +=1
            self.score +=1
            self.food = self.place_food()

        else:
            if new_distance_to_food < prev_distance_to_food:
                reward += 0.01
            elif new_distance_to_food > prev_distance_to_food:
                reward -= 0.5
            self.snake.pop() 


        return self.get_state(), reward, done, self.food_eat, self.score

    def get_distance_to_food(self):
        head_x, head_y = self.snake[0]
        food_x, food_y = self.food
        return abs(head_x - food_x) + abs(head_y - food_y)

    def get_state(self):
        head_x, head_y = self.snake[0]
        food_x, food_y = self.food
        rel_food_x = food_x - head_x
        rel_food_y = food_y - head_y
        snake_length = len(self.snake)

        return (self.direction, rel_food_x, rel_food_y, snake_length)

    def place_food(self):
        while True:
            food = (random.randint(0, self.GRID_WIDTH - 1), random.randint(0, self.GRID_HEIGHT - 1))
            if food not in self.snake:
                return food

    def draw_grid(self):
        for x in range(0, self.WIDTH, self.GRID_SIZE):
            for y in range(0, self.HEIGHT, self.GRID_SIZE):
                pygame.draw.rect(self.screen, self.BACKGROUND_COLOR, (x, y, self.GRID_SIZE, self.GRID_SIZE), 1)

    def draw_snake(self):
        for segment in self.snake:
            pygame.draw.rect(self.screen, self.SNAKE_COLOR, (segment[0] * self.GRID_SIZE, segment[1] * self.GRID_SIZE, self.GRID_SIZE, self.GRID_SIZE))

    def draw_food(self):
        pygame.draw.rect(self.screen, self.FOOD_COLOR, (self.food[0] * self.GRID_SIZE, self.food[1] * self.GRID_SIZE, self.GRID_SIZE, self.GRID_SIZE))

    def check_collision(self):
        head_x, head_y = self.snake[0]
        return (head_x < 0 or head_x >= self.GRID_WIDTH or
                head_y < 0 or head_y >= self.GRID_HEIGHT or
                self.snake[0] in self.snake[1:])
        
    def state_size(self):
        return 5
    
    def render(self):
        self.screen.fill(self.BACKGROUND_COLOR)
        self.draw_grid()
        self.draw_snake()
        self.draw_food()
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and self.direction != (0, 1):
                        self.direction = (0, -1)
                    elif event.key == pygame.K_DOWN and self.direction != (0, -1):
                        self.direction = (0, 1)
                    elif event.key == pygame.K_LEFT and self.direction != (1, 0):
                        self.direction = (-1, 0)
                    elif event.key == pygame.K_RIGHT and self.direction != (-1, 0):
                        self.direction = (1, 0)

            self.move_snake()
            score_surface = self.font.render(f'Food eaten: {self.score}', True, self.SNAKE_COLOR)
            self.screen.blit(score_surface, (10, 10))  
            
            if self.check_collision():
                print(f'Game Over! Your score: {self.score}')
                running = False

            self.render()
            self.clock.tick(8)

        pygame.quit()

if __name__ == "__main__":
    game = SnakeGame()
    game.run()
