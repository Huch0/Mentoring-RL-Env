import pygame
import os


class UI:
    def __init__(self, game, cell_size=50):
        self.game = game
        self.cell_size = cell_size
        self.width = game.n * cell_size
        self.height = game.m * cell_size
        self.screen = pygame.display.set_mode((self.width, self.height + 50))  # Add extra space for info
        pygame.font.init()  # Initialize the font module
        self.font = pygame.font.SysFont(None, 30)  # Initialize font

        self.selected_square = []  # for user input
        apple_image_path="/home/jihyeon/Mentoring-RL-Env/AppleGameEnv/apples.png"
        self.apple_image=None

        if os.path.exists(apple_image_path):
            self.apple_image = pygame.image.load(apple_image_path).convert_alpha()
        else:
            print(f'Error: Image file not found at {apple_image_path}')

    def draw_grid(self):
        """Draw the game grid."""
        pygame.draw.rect(
            self.screen, (255, 255, 204),
            pygame.Rect(0, 0, self.width, self.height)
        )

        for row in range(self.game.m):
            for col in range(self.game.n):
                value = self.game.grid[0,row,col]
                """color = (255, 244, 204)
                pygame.draw.rect(
                    self.screen, color,
                    pygame.Rect(col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size)
                )"""
                
                if value != 0 and self.apple_image :
                    scaled_image = pygame.transform.scale(self.apple_image,(self.cell_size - 10, self.cell_size - 10))
                    self.screen.blit(scaled_image,(col*self.cell_size, row*self.cell_size))

                # Draw the value if it's non-zero
                if value > 0:
                    text = self.font.render(str(value), True, (0, 0, 0))
                    self.screen.blit(text, (col * self.cell_size + 15, row * self.cell_size + 15))

    def draw_info(self):
        """Draw additional information like score and remaining steps."""
        score_text = self.font.render(f"Score: {self.game.get_score()}", True, (0, 0, 0))
        steps_text = self.font.render(f"Steps Left: {self.game.max_steps - self.game.steps}", True, (0, 0, 0))
        self.screen.blit(score_text, (10, self.height + 10))
        self.screen.blit(steps_text, (200, self.height + 10))

    def render(self):
        """Render the game state."""
        self.screen.fill((255, 255, 255))  # Clear screen
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
