import pygame


class UI:
    def __init__(self, game, cell_size=50):
        self.game = game
        self.cell_size = cell_size
        self.width = game.n * cell_size
        self.height = game.m * cell_size
        self.screen = pygame.display.set_mode((self.width, self.height + 50))  # Add extra space for info
        pygame.font.init()  # Initialize the font module
        self.font = pygame.font.SysFont(None, 36)  # Initialize font

        self.selected_square = []  # for user input

    def draw_grid(self):
        """Draw the game grid."""
        for row in range(self.game.m):
            for col in range(self.game.n):
                value = self.game.grid[row][col]
                color = (255, 255, 255) if value == 0 else (0, 255, 0)
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
                coord = (row, col)

                self.selected_square.append(coord)
                if len(self.selected_square) == 2:
                    self.game.step(tuple(self.selected_square))
                    self.selected_square = []  # Clear selected squares

        return True
