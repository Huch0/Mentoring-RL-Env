import argparse
import pygame
from AppleGameEnv.UI import UI
from AppleGameEnv.AppleGame import AppleGame
from AppleGameEnv.AppleGameEnv import AppleGameEnv
from stable_baselines3 import PPO  # Assuming PPO is the algorithm used for training


def main():
    # Parse command-line arguments to choose game mode
    parser = argparse.ArgumentParser(description="Play the Apple Game with or without a trained agent.")
    parser.add_argument("--agent", type=str, default=None,
                        help="Path to the trained agent model file (.zip). If not specified, play manually.")
    args = parser.parse_args()

    # Initialize UI
    game = AppleGame()
    ui = UI(game)

    # If agent path is provided, load the agent
    agent = None
    with_agent = False
    if args.agent:
        print(f"Loading trained agent from {args.agent}...")
        agent = PPO.load(args.agent)
        env = AppleGameEnv()
        with_agent = True
    else:
        print("No agent specified. Playing manually.")

    # Main game loop
    game.reset()  # Initialize the game
    running = True

    while running:
        ui.render()  # Render the game
        running = ui.handle_events()

        if with_agent:
            # Handle agent play
            obs = env.get_obs()  # Get the current observation
            action, _ = agent.predict(obs, deterministic=True)  # Get action from the agent
            game.step(action)  # Execute the agent's action

        # Check if the game is over
        if game.is_game_over():
            print(f"Game Over! Final Score: {game.get_score()}")
            running = False

        # Limit the frame rate
        pygame.time.delay(100)

    pygame.quit()  # Clean up the game


if __name__ == "__main__":
    main()
