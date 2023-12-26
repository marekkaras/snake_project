import pygame
from snake_project.game import GameBase


if __name__ == '__main__':
    game = GameBase()
    
    # game loop
    while True:
        reward, game_over, score = game.play_step()
        
        if game_over == True:
            break
        
    print('Final Score', score)
    pygame.quit()
