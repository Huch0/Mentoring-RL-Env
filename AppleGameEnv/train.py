import gymnasium as gym
from AppleGameEnv import AppleGameEnv
from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import EvalCallback
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.logger import configure
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.callbacks import CheckpointCallback
from stable_baselines3.common.vec_env import DummyVecEnv

def train_agent():
    
    env = DummyVecEnv([lambda: Monitor(AppleGameEnv(m=36, n=36, max_steps=10000))])
    model = PPO('CnnPolicy', env, verbose =1)

    log_dir = "./tmp/logs"
    

# Separate evaluation env
    
    eval_env = DummyVecEnv([lambda: Monitor(AppleGameEnv(m=36, n=36, max_steps=10000))])


# $ tensorboard --logdir ./examples/tmp/logs/eval 로 tensorboard 실행
    new_logger = configure(log_dir, ["stdout", "csv", "tensorboard"])
    model.set_logger(new_logger)

# Use deterministic actions for evaluation
    eval_callback = EvalCallback(eval_env, best_model_save_path=log_dir,
                                log_path=log_dir, eval_freq=500, n_eval_episodes=5,
                                deterministic=True, render=False)

    model.learn(total_timesteps=10000, callback=eval_callback)

    #checkpoint_callback = CheckpointCallback(save_freq=1000, save_path="./agents/",name_prefix='ppo_apple_game')

    #model.learn(total_timesteps=100000,callback=checkpoint_callback)

    model.save(log_dir + "/ppo_apple_game")

if __name__ == '__main__':
    train_agent()
    