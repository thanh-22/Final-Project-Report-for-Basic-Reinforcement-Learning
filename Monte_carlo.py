import numpy as np
from collections import defaultdict
import pickle
import pygame
import matplotlib.pyplot as plt
from snake import SnakeGame

class MonteCarloAgent:
    def __init__(self, epsilon=0.1, min_epsilon=0.01, decay_rate=0.9999):
        self.q_values = defaultdict(lambda: np.zeros(4))  # 4 possible actions
        self.returns = defaultdict(list)  # To store returns for each state-action pair
        self.epsilon = epsilon
        self.min_epsilon = min_epsilon
        self.decay_rate = decay_rate

    def get_action(self, state):
        if np.random.random() < self.epsilon:
            return np.random.randint(4)  # Explore
        else:
            return np.argmax(self.q_values[state])  # Exploit

    def update(self, episode):
        # Calculate returns for each state-action pair in the episode
        G = 0
        for state, action, reward in reversed(episode):
            G = reward + G  # Discounting not applied in Monte Carlo for simplicity
            self.returns[(state, action)].append(G)  # Store the return
            self.q_values[state][action] = np.mean(self.returns[(state, action)])  # Update Q-value

        # Decay epsilon
        self.epsilon = max(self.min_epsilon, self.epsilon * self.decay_rate)

# Update the train_agent function
def train_agent(n_episodes):
    env = SnakeGame()
    agent = MonteCarloAgent()
    scores = []
    food_counts = []
    clock = pygame.time.Clock()
    pygame.init()
    pygame.font.init()
    font = pygame.font.Font(None, 36)

    for episode in range(n_episodes):
        state = env.reset_game()
        done = False
        total_score = 0
        food = 0
        episode_data = []  # Collect state, action, reward tuples

        while not done:
            action = agent.get_action(state)
            next_state, reward, done, food_eaten, food_point = env.step(action)

            # Store the state, action, reward in the episode data
            episode_data.append((state, action, reward))

            state = next_state
            total_score += reward
            food += food_eaten

            if episode % 1000 == 0:  
                env.render()
                text_surface = font.render(f'Food: {food_point}', True, (0, 0, 0))
                env.screen.blit(text_surface, (10, 10)) 
                text_surface = font.render(f'Episode: {episode + 1}/{n_episodes}', True, (0, 0, 0)) 
                env.screen.blit(text_surface, (10, 50)) 
                text_surface = font.render(f'Reward: {total_score:.2f}', True, (0, 0, 0)) 
                env.screen.blit(text_surface, (10, 30)) 
                pygame.display.flip() 
                clock.tick(10) 
        
        scores.append(total_score)
        food_counts.append(food)
        
        agent.update(episode_data) 

    mean_score = sum(scores) / n_episodes
    mean_food = sum(food_counts) / n_episodes
    print(f'Mean rewards after {n_episodes} episodes: {mean_score:.2f}')
    print(f'Mean food eaten after {n_episodes} episodes: {mean_food:.2f}')


    fig, axs = plt.subplots(2, 1, figsize=(12, 14))
    # Plot Rewards
    axs[0].plot(range(1, n_episodes + 1), scores, label='Rewards per Episode', color='blue')
    axs[0].axhline(y=mean_score, color='r', linestyle='--', label='Mean Score')
    axs[0].set_xlabel('Episode Number')
    axs[0].set_ylabel('Reward')
    axs[0].set_title('Rewards Over Episodes')
    axs[0].legend()
    axs[0].grid()

    # Plot Food Counts
    axs[1].plot(range(1, n_episodes + 1), food_counts, label='Food Eaten per Episode', color='green')
    axs[1].axhline(y=mean_food, color='orange', linestyle='--', label='Mean Food Eaten')
    axs[1].set_xlabel('Episode Number')
    axs[1].set_ylabel('Food Count')
    axs[1].set_title('Food Eaten Over Episodes')
    axs[1].legend()
    axs[1].grid()

    plt.tight_layout()
    plt.show()
    return sum(scores)
if __name__ == "__main__":
    train_agent(10000)
    
    
    
    
    

    
    