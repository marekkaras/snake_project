import random

class Kain:
    
    def __init__(self):
        pass
    
    def make_move_from_state(self, state, smartness_level: int = 3):
        
        danger_straight = state[0]
        danger_right = state[1]
        danger_left = state[2]
        dir_left = state[3]
        dir_right = state[4]
        dir_up = state[5]
        dir_down = state[6]
        food_left = state[7]
        food_right = state[8]
        food_up = state[9]
        food_down = state[10]
        food_state = food_left + food_right + food_up + food_down
        
        #  Prioritize avoiding danger
        if smartness_level >= 1:
            if danger_straight:
                if not danger_left and not danger_right:
                    return random.choice([[0 , 0, 1], [0 , 1, 0]])
                if not danger_left:
                    return [0 , 0, 1]
                else:
                    return [0 , 1, 0]
        #  Then move towards food
        if smartness_level >= 2:
            if food_state == 2:
                if dir_left:
                    if food_right:
                        if food_up and not danger_right:
                            return [0 , 1, 0]
                        if food_down and not danger_left:
                            return [0 , 0, 1]
                if dir_right:
                    if food_left:
                        if food_up and not danger_left:
                            return [0 , 0, 1]
                        if food_down and not danger_right:
                            return [0 , 1, 0]
                if dir_up:
                    if food_down:
                        if food_left and not danger_left:
                            return [0 , 0, 1]
                        if food_right and not danger_right:
                            return [0 , 1, 0]
                if dir_down:
                    if food_up:
                        if food_left and not danger_right:
                            return [0 , 1, 0]
                        if food_right and not danger_left:
                            return [0 , 0, 1]
        #  But dont get stuck in the loop
        #  if only one possible direction turn
        if smartness_level >= 3:
            if food_state == 1:
                if food_left:
                    if dir_left:
                        return [1 , 0, 0]
                    if dir_right:
                        return [1 , 0, 0]
                    if dir_up:
                        return [0 , 0, 1]
                    if dir_down:
                        return [0 , 1, 0]
            else:
                return [1 , 0, 0]
        return [1 , 0, 0]
