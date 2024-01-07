import argparse

from snake_project.game import GameBase
from snake_project.helper import plot
from snake_project.abel import Abel
from snake_project.logs import logger

import hashlib
import datetime

import pandas as pd
    

def run_abel(seed: int, how_many_seeds: int, speed: int, how_many_games: int,
             rewards = list):
    
    
    seed = int(seed)
    seeds = []
    for i in range(0, int(how_many_seeds)):
        seeds.append(seed)
        seed += 1
        
    agent = Abel(games_to_play=int(how_many_seeds) * int(how_many_games),
                 model_from_file='stage5_maxmean.pth',
                 hidden_layers=512)
    agent_timestamp = datetime.datetime.now().timestamp()
    agent_timestamp_as_bytes = str.encode(str(agent_timestamp))
    h = hashlib.sha3_512()
    h.update(agent_timestamp_as_bytes)
    agent_hash = h.hexdigest()
    
    plot_scores = []
    plot_mean_scores = []
    timestamps = []
    total_score = 0
    record = 0
    n_games = 0
    
    for seed in seeds:
        
        game = GameBase(randomseed=seed, 
                        speed=speed, 
                        neg_reward=-10,
                        pos_reward=27)
        
        starting_timestamp = datetime.datetime.now().timestamp()
        starting_timestamp_as_bytes = str.encode(str(starting_timestamp))
        h = hashlib.sha3_512()
        h.update(starting_timestamp_as_bytes)
        game_hash = h.hexdigest()
        
        logger.info(f'Abel playing game using rewards: -10, 27')
        
        for current_game in range(0, int(how_many_games)):
            
            logger.info(f'Abel playing game using seed: {seed}. Game number: {current_game}')

            game.randomseed = seed
            game.setup_game()
            
            while True:
                
                #  Make moves
                current_state = game.get_state()
                final_move = agent.get_move_from_model(current_state)
                reward, game_over, score = game.play_step(final_move)
                
                if game_over:
                    n_games += 1
        
                    if score > record:
                        record = score
        
                    logger.info(f'Game score: {score}. Record: {record}')
        
                    plot_scores.append(score)
                    total_score += score
                    mean_score = total_score / n_games
                    plot_mean_scores.append(mean_score)
                    current_timestamp = datetime.datetime.now().timestamp()
                    timestamps.append(current_timestamp)
                    plot(plot_scores, plot_mean_scores)   
                    break
    data = {'ts': timestamps, 'scores': plot_scores, 'mean_scores': plot_mean_scores} 
    training_results = pd.DataFrame(data)
    training_results['game_hash'] = game_hash
    training_results['starting_timestamp'] = starting_timestamp
    training_results['negative_reward'] = -10
    training_results['positive_reward'] = 27
    training_results['seed'] = seed
    training_results['how_many_seeds'] = how_many_seeds
    training_results['how_many_games'] = how_many_games
    training_results['speed'] = speed
    training_results.to_csv(f'{agent_hash}.csv')
    print(training_results)
    input("Press button to continue...")
    return


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--seed', help='Seed to begin with.', default=1)
    parser.add_argument('--how-many-seeds', help='How many seeds to use', default=1)
    parser.add_argument('--speed', help='Seed to begin with.', default=20)
    parser.add_argument('--how-many-games', help='How many games to play for each seed', default=1)
    args = parser.parse_args()
    run_abel(args.seed, args.how_many_seeds, args.speed, args.how_many_games)
