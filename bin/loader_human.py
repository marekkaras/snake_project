import pygame
from snake_project.game import GameBase
from snake_project.logs import logger


if __name__ == '__main__':
    game = GameBase()
    
    # game loop
    while True:
        reward, game_over, score = game.play_step()
        
        if game_over == True:
            break
        
    logger.info(f'Final Score: {score}')
    input("Press button to continue...")
    pygame.quit()
