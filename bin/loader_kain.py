import argparse

from snake_project.game import GameBase
from snake_project.helper import plot
from snake_project.kain import Kain
from snake_project.logs import logger
    

def run_kain(seed: int, speed: int, how_many_games: int):
    
    seed = int(seed)
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    n_games = 0
    
    agent = Kain()
    game = GameBase(randomseed=seed, speed=speed)
    
    #  Set seeds
    seeds = []
    for i in range(0, int(how_many_games)):
        seeds.append(seed)
        seed += 1
    
    for seed, current_game in zip(seeds, range(0, int(how_many_games))):
        
        if not agent and not game:
            agent = Kain()
            game = GameBase(randomseed=seed, speed=speed)
        
        logger.info(f'Kain playing game using seed: {seed}. Game number: {current_game}')
        
        game.randomseed = seed
        game.setup_game()
        
        while True:
            
            #  Make moves
            current_state = game.get_state()
            final_move = agent.make_move_from_state(current_state)
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
                plot(plot_scores, plot_mean_scores)   
                break
    input("Press button to continue...")
    return


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--seed', help='Seed to begin with.', default=1)
    parser.add_argument('--speed', help='Seed to begin with.', default=20)
    parser.add_argument('--how-many-games', help='How many games to play', default=1)
    args = parser.parse_args()
    run_kain(args.seed, args.speed, args.how_many_games)
