import pygame
import numpy as np

class UI:
    def __init__(self, game, cell_size=50):
        """Initialize the UI class.

        Args:
            game (AppleGame): Instance of the AppleGame class.
            cell_size (int, optional): Size of each cell in the grid.
        """
        self.game = game
        self.cell_size = cell_size
        self.width = game.n * cell_size
        self.height = game.m * cell_size

        # Initialize PyGame
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Apple Game")

        # Font for displaying text
        self.font = pygame.font.Font(None, 36)

    def draw_grid(self):
        """Draw the game grid on the screen."""
        for row in range(self.game.m):
            for col in range(self.game.n):
                # Get the value in the grid
                value = int(self.game.grid[row, col])
                color = (255, 255, 255) if value == 0 else (0, 255, 0)  # Green for apples, white for empty
                pygame.draw.rect(
                    self.screen, color,
                    pygame.Rect(col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size)
                )
                # Draw the value if it's non-zero
                if value > 0:
                    text = self.font.render(str(value), True, (0, 0, 0))
                    self.screen.blit(text, (col * self.cell_size + 15, row * self.cell_size + 10))

    def draw_info(self):
        """Draw additional information like score and remaining steps."""
        score_text = self.font.render(f"Score: {self.game.get_score()}", True, (255, 255, 255))
        steps_text = self.font.render(f"Steps Left: {self.game.max_steps - self.game.steps}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, self.height + 10))
        self.screen.blit(steps_text, (200, self.height + 10))

    def render(self):
        """Render the game state."""
        self.screen.fill((0, 0, 0))  # Clear screen
        self.draw_grid()  # Draw grid
        self.draw_info()  # Draw score and steps
        pygame.display.flip()  # Update the display

    def handle_events(self):
        """Handle user input events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Handle user clicking to select a square
                x, y = event.pos
                row = y // self.cell_size
                col = x // self.cell_size
                return (row, col)  # Return the selected cell
        return None

