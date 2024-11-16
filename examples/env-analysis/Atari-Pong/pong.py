import gymnasium as gym
import pygame
from pygame.locals import K_UP, K_DOWN, K_LEFT, K_RIGHT, K_ESCAPE, QUIT

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Pong with Keyboard Control")

# Define a function to map keyboard inputs to actions
def get_action():
    keys = pygame.key.get_pressed()
    if keys[K_UP]:
        return 2  # Move up
    elif keys[K_DOWN]:
        return 3  # Move down
    else:
        return 0  # No action

if __name__ == "__main__":
    env = gym.make("ALE/Pong-v5", render_mode="human")

    # Set a consistent FPS for rendering
    env.metadata['render_fps'] = 20  # You can adjust this value as needed

    env.reset()
    done = False
    clock = pygame.time.Clock()

    while not done:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == pygame.KEYDOWN and event.key == K_ESCAPE):
                done = True

        env.render()
        action = get_action()
        _, _, terminated, truncated, _ = env.step(action)
        done = terminated or truncated

        clock.tick(env.metadata['render_fps'])

    env.close()
    pygame.quit()