import gymnasium as gym
import pygame
from pygame.locals import K_UP, K_DOWN, K_LEFT, K_RIGHT, K_a, K_s, K_d, K_ESCAPE, QUIT

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Assault with Keyboard Control")

# Define a function to map keyboard inputs to actions
def get_action():
    keys = pygame.key.get_pressed()
    if keys[K_LEFT]:  # LEFT
        return 4
    elif keys[K_RIGHT]:  # RIGHT
        return 3
    elif keys[K_UP]:  # UP
        return 2
    elif keys[K_a]:  # LEFT FIRE
        return 6
    elif keys[K_d]:  # RIGHT FIRE
        return 5
    else:
        return 0

if __name__ == "__main__":
    env = gym.make("ALE/Assault-v5", render_mode="human")

    # Set a consistent FPS for rendering
    env.metadata['render_fps'] = 20  # You can adjust this value as needed

    env.reset()
    done = False
    clock = pygame.time.Clock()

    while not done:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == pygame.KEYDOWN and event.key == K_ESCAPE):
                done = True

        action = get_action()
        _, _, terminated, truncated, _ = env.step(action)
        done = terminated or truncated

        env.render()
        clock.tick(env.metadata.get('render_fps', 20))

    env.close()
    pygame.quit()