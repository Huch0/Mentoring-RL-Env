import gymnasium as gym
import pygame
import numpy as np

# Initialize pygame and the environment
pygame.init()
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Pusher Manual Control")

# Create the environment
env = gym.make("Pusher-v4", render_mode="human")

# Initialize a variable to keep track of which joint to control
selected_joint = 0  # Start with controlling the first joint

# Define action mappings for 7 joints
def get_action():
    global selected_joint

    action = np.zeros(env.action_space.shape)  # 7-dimensional action space
    keys = pygame.key.get_pressed()

    # Select joint using keys 1 to 7, and apply torque with Z and X keys
    if keys[pygame.K_1]:
        selected_joint = 0  # Control r_shoulder_pan_joint
    if keys[pygame.K_2]:
        selected_joint = 1  # Control r_shoulder_lift_joint
    if keys[pygame.K_3]:
        selected_joint = 2  # Control r_upper_arm_roll_joint
    if keys[pygame.K_4]:
        selected_joint = 3  # Control r_elbow_flex_joint
    if keys[pygame.K_5]:
        selected_joint = 4  # Control r_forearm_roll_joint
    if keys[pygame.K_6]:
        selected_joint = 5  # Control r_wrist_flex_joint
    if keys[pygame.K_7]:
        selected_joint = 6  # Control r_wrist_roll_joint

    # Control the torque for the selected joint using Z (decrease) and X (increase)
    if keys[pygame.K_z]:
        action[selected_joint] = -0.5  # Min torque
    if keys[pygame.K_x]:
        action[selected_joint] = 0.5  # Max torque

    return action


if __name__ == "__main__":
    done = False
    env.reset()

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        # Get manual action
        action = get_action()

        # Step the environment with manual action
        obs, reward, terminated, truncated, info = env.step(action)

        # Check if the episode is done
        done = terminated  # or truncated

        # Render the environment
        env.render()

    env.close()
    pygame.quit()
