import argparse
import pygame
from AppleGameEnv.GameController import GameController
from AppleGameEnv.AppleGameEnv import AppleGameEnv
from stable_baselines3 import PPO  # Assuming PPO is the algorithm used for training


def main():
    # Parse command-line arguments to choose game mode
    parser = argparse.ArgumentParser(description="Play the Apple Game with or without a trained agent.")
    parser.add_argument("--agent", type=str, default=None,
                        help="Path to the trained agent model file (.zip). If not specified, play manually.")
    args = parser.parse_args()

    # Initialize GameController
    controller = GameController()

    # If agent path is provided, load the agent
    agent = None
    if args.agent:
        print(f"Loading trained agent from {args.agent}...")
        agent = PPO.load(args.agent)
        env = AppleGameEnv()
    else:
        print("No agent specified. Playing manually.")

    # Main game loop
    controller.reset()  # Initialize the game
    running = True
    manual_mode = agent is None
    selected_square = []

    while running:
        controller.ui.render()  # Render the game

        if manual_mode:
            # Handle manual play
            selected = controller.ui.handle_events()
            if selected is False:  # Quit the game
                running = False
            elif selected:  # User selected a square
                selected_square.append(selected)
                if len(selected_square) == 2:
                    controller.game.step(tuple(selected_square))
                    selected_square = []  # Clear selected squares
        else:
            # Handle agent play
            obs = env.get_obs()  # Get the current observation
            action, _ = agent.predict(obs, deterministic=True)  # Get action from the agent
            controller.game.step(action)  # Execute the agent's action

        # Check if the game is over
        if controller.game.is_game_over():
            print(f"Game Over! Final Score: {controller.game.get_score()}")
            running = False

        # Limit the frame rate
        pygame.time.delay(100)

    pygame.quit()  # Clean up the game


if __name__ == "__main__":
    main()
