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

    def draw_apple(self, x, y, value):
        """Draw an apple at the specified position with a number on it."""
        # Draw the stem (rectangle on top)
        stem_color = (100, 50, 10)  # Brown
        stem_width = self.cell_size // 8
        stem_height = self.cell_size // 4
        pygame.draw.rect(
            self.screen, stem_color,
            pygame.Rect(
                x + self.cell_size // 2 - stem_width // 2,
                y + 1,  # Slightly above the circle
                stem_width, stem_height
            )
        )
        
        # Draw the apple (circle for the body)
        apple_color = (255, 0, 0)  # Red
        pygame.draw.circle(
            self.screen, apple_color,
            (x + self.cell_size // 2, y + self.cell_size // 2),  # Center of the cell
            self.cell_size // 2 - 5  # Radius
        )


        # Draw the leaf (small green ellipse)
        leaf_color = (0, 255, 0)  # Green
        pygame.draw.ellipse(
            self.screen, leaf_color,
            pygame.Rect(
                x + self.cell_size // 2 + 5,
                y,  # Next to the stem
                self.cell_size // 4, self.cell_size // 8
            )
        )

        # Draw the value if it's non-zero
        if value > 0:
            text = self.font.render(str(value), True, (255, 255, 255))  # White number
            text_rect = text.get_rect(center=(x + self.cell_size // 2, y + self.cell_size // 2))
            self.screen.blit(text, text_rect)

    def draw_grid(self):
        """Draw the game grid."""
        for row in range(self.game.m):
            for col in range(self.game.n):
                value = self.game.grid[row][col]
                x = col * self.cell_size
                y = row * self.cell_size
                if value > 0:
                    self.draw_apple(x, y, value)  # Draw apple if value > 0
                else:
                    # Draw empty cell background
                    pygame.draw.rect(
                        self.screen, (0, 0, 0),  # White background
                        pygame.Rect(x, y, self.cell_size, self.cell_size)
                    )

    def draw_info(self):
        """Draw additional information like score and remaining steps."""
        score_text = self.font.render(f"Score: {self.game.get_score()}", True, (255, 255, 255))
        steps_text = self.font.render(f"Steps Left: {self.game.max_steps - self.game.steps}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, self.height + 10))
        self.screen.blit(steps_text, (200, self.height + 10))

    def render(self):
        """Render the game state."""
        self.screen.fill((0, 0, 0))  # Clear screen with black background
        self.draw_grid()  # Draw grid with apples
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
