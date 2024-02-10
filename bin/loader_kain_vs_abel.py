# -*- coding: utf-8 -*-
import argparse

from snake_project.game import GameBase
from snake_project.abel import Abel
from snake_project.kain import Kain


def run_kain_vs_abel(seed: int, how_many_seeds: int, speed: int, ):
    seed = int(seed)
    seeds = []
    for i in range(0, int(how_many_seeds)):
        seeds.append(seed)
        seed += 1
        
    abel = Abel(games_to_play=int(how_many_seeds),
                 model_from_file='final_model.pth',
                 hidden_layers=512)
    kain = Kain()
    
    game = GameBase(randomseed=seeds[1], 
                    speed=speed)
    for seed in seeds[1:]:
        for agent in (abel, kain):
            game.randomseed = seed
            snake_color = 'green' if type(agent) == Abel else 'blue'
            game.setup_game(snake_color=snake_color)
            while True:
                current_state = game.get_state()
                if type(agent) == Abel:
                    final_move = agent.get_move_from_model(current_state)
                else:
                    final_move = agent.make_move_from_state(current_state)
                reward, game_over, score = game.play_step(final_move)
                if game_over:
                    break              
                

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--seed', help='Seed to begin with.', default=1)
    parser.add_argument('--how-many-seeds', help='How many seeds to use', default=10)
    parser.add_argument('--speed', help='Seed to begin with.', default=20)
    args = parser.parse_args()
    run_kain_vs_abel(args.seed, args.how_many_seeds, args.speed)
