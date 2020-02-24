import ConnectFourRandomAI
import ConnectFourMinimaxAI

import ConnectFourEngine

if __name__ == '__main__':
    # Initialise the game engine
    # Modify these parameters to tweak the game
    app = ConnectFourEngine.ConnectFour(
            rewards = [0, 10, 100, 10000, 100000, 100000, 1000000, 0, 0],
            winscore = 10000,
            ai_delay = 500,
            red_player = ConnectFourMinimaxAI.AIcheck,
            blue_player = ConnectFourMinimaxAI.AIcheck,
            )
    # start the game engine
    app.game_loop()
