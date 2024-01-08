import argparse

from snake_project.game import GameBase
from snake_project.helper import plot
from snake_project.abel import Abel
from snake_project.logs import logger

import hashlib
import datetime

import pandas as pd
    

def train_params(seed: int, how_many_seeds: int, speed: int, how_many_games: int,
                 tt: str):
        
    """
    batch_size: int = 1000,
    learning_rate: float = 0.001,
    gamma: float = 0.9,
    """
    if tt == 'gm':
        whats_being_trained = 'granular_gamma'
        batch_sizes = [1000]
        learning_rates = [0.001]
        gammas = [0.7, 0.71, 0.72, 0.73, 0.74, 0.75, 0.76, 0.77, 0.78, 0.79, 0.8,
                  0.81, 0.82, 0.83, 0.84, 0.85, 0.86, 0.87, 0.88, 0.89,
                  0.9, 0.91, 0.92, 0.93, 0.94, 0.95, 0.96, 0.97, 0.98, 0.99, 1.0]
    elif tt == 'lr':
        whats_being_trained = 'granular_lr'
        batch_sizes = [1000]
        learning_rates = [0.0001, 0.0002, 0.0003, 0.0004, 0.0005, 0.0006, 
                          0.0007, 0.0008, 0.0009, 0.001, 0.0011, 0.0012, 0.0013, 
                          0.0014, 0.0015]
        gammas = [0.9]
    elif tt == 'bs':
        whats_being_trained = 'granular_bs'
        batch_sizes = [500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000,
                       5500, 6000, 6500, 7000, 7500, 8000, 8500, 9000, 9500, 10000]
        learning_rates = [0.001]
        gammas = [0.9]
    elif tt == 'final':
        whats_being_trained = 'final_model_long'
        batch_sizes = [8000]
        learning_rates = [0.0007]
        gammas = [0.82]
    else:
        raise Exception('Unknown parameter to train')
    
    
    import itertools
    parameters = [batch_sizes, learning_rates, gammas]
    parameters = list(itertools.product(*parameters))
    for param_set in parameters:
        batch_size = param_set[0]
        learning_rate = param_set[1]
        gamma = param_set[2]
        print(batch_size, learning_rate, gamma)
        
        run_abel(seed=seed,
                 how_many_seeds=how_many_seeds,
                 speed=speed,
                 how_many_games=how_many_games,
                 number_of_layers=512,
                 batch_size=batch_size,
                 learning_rate=learning_rate,
                 gamma=gamma,
                 whats_being_trained=whats_being_trained)
    


def run_abel(seed: int, how_many_seeds: int, speed: int, how_many_games: int,
             number_of_layers: int, batch_size: int, learning_rate: float,
             gamma: float, whats_being_trained: str):
    
    number_of_layers = int(number_of_layers)

    seed = int(seed)
    seeds = []
    for i in range(0, int(how_many_seeds)):
        seeds.append(seed)
        seed += 1
        
    agent = Abel(games_to_play=int(how_many_seeds) * int(how_many_games),
                 hidden_layers=number_of_layers,
                 batch_size=batch_size,
                 learning_rate=learning_rate,
                 gamma=gamma)
    agent_timestamp = datetime.datetime.now().timestamp()
    agent_timestamp_as_bytes = str.encode(str(agent_timestamp))
    h = hashlib.sha3_512()
    h.update(agent_timestamp_as_bytes)
    agent_hash = h.hexdigest()
    
    plot_scores = []
    plot_mean_scores = []
    timestamps = []
    best_mean = 0
    total_score = 0
    record = 0
    n_games = 0
    
    for seed in seeds:
        
        game = GameBase(randomseed=seed, 
                        speed=speed, 
                        neg_reward=-10,
                        pos_reward=27)
        
        for current_game in range(0, int(how_many_games)):
            
            logger.info(f'Abel playing game using seed: {seed}. Game number: {current_game}')

            game.randomseed = seed
            game.setup_game()
            
            while True:
                
                #  Make moves
                current_state = game.get_state()
                final_move = agent.get_action(current_state)
                reward, game_over, score = game.play_step(final_move)
                state_after_move = game.get_state()
                agent.train_short_memory(current_state, 
                                         final_move, 
                                         reward, 
                                         state_after_move, 
                                         game_over)
                agent.remember(current_state, 
                               final_move, 
                               reward, 
                               state_after_move, 
                               game_over)
                
                if game_over:
                    n_games += 1
                    agent.n_games += 1
                    #agent.train_long_memory()
        
                    if score > record:
                        agent.train_long_memory()
                        record = score
                        agent.model.save(file_name=f'{whats_being_trained}_{batch_size}_{learning_rate}_{gamma}_maxscore.pth')
        
                    logger.info(f'Game score: {score}. Record: {record}')
        
                    plot_scores.append(score)
                    total_score += score
                    mean_score = total_score / n_games
                    if mean_score > best_mean:
                        best_mean = mean_score
                        agent.model.save(file_name=f'{whats_being_trained}_{batch_size}_{learning_rate}_{gamma}_maxmean.pth')
                    plot_mean_scores.append(mean_score)
                    current_timestamp = datetime.datetime.now().timestamp()
                    timestamps.append(current_timestamp)
                    plot(plot_scores, plot_mean_scores)   
                    break
    agent.model.save(file_name=f'{whats_being_trained}_{batch_size}_{learning_rate}_{gamma}_final.pth')
    data = {'ts': timestamps, 'scores': plot_scores, 'mean_scores': plot_mean_scores} 
    training_results = pd.DataFrame(data)
    training_results['agent_hash'] = agent_hash
    training_results['agent_timestamp'] = agent_timestamp
    training_results['batch_size'] = batch_size
    training_results['learning_rate'] = learning_rate
    training_results['gamma'] = gamma
    training_results.to_csv(f'{whats_being_trained}_{batch_size}_{learning_rate}_{gamma}.csv')
    print(training_results)
    return


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--seed', help='Seed to begin with.', default=1)
    parser.add_argument('--how-many-seeds', help='How many seeds to use', default=1)
    parser.add_argument('--speed', help='Seed to begin with.', default=20)
    parser.add_argument('--how-many-games', help='How many games to play for each seed', default=1)
    parser.add_argument('--tt', help='What to train')
    args = parser.parse_args()
    train_params(args.seed, args.how_many_seeds, args.speed, args.how_many_games, args.tt)
