import pygame
from AppleGameEnv.AppleGame import AppleGame
from AppleGameEnv.UI import UI


class GameController:
    def __init__(self):
        """Initialize the GameController."""
        self.game = AppleGame()
        self.ui = UI(self.game)
        self.selected_square = []

    def reset(self):
        """Reset the game and UI."""
        self.game.reset()

    def run(self):
        """Main game loop."""
        self.reset()
        running = True

        while running:
            self.ui.render()  # Render the current game state

            # Handle user input
            selected = self.ui.handle_events()
            if selected is False:  # User closed the game
                running = False
            elif selected:  # User clicked on a square
                self.selected_square.append(selected)
                if len(self.selected_square) == 2:
                    # If two squares are selected, perform a game step
                    self.game.step(tuple(self.selected_square))
                    self.selected_square = []  # Reset selected squares

            # Check if the game is over
            if self.game.is_game_over():
                print(f"Game Over! Final Score: {self.game.get_score()}")
                running = False

        pygame.quit()  # Quit PyGame
