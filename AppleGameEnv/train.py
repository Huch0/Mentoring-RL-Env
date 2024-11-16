import gymnasium as gym
from stable_baselines3 import PPO
from AppleGameEnv.AppleGameEnv import AppleGameEnv
from stable_baselines3.common.callbacks import CheckpointCallback
from stable_baselines3 import SAC
from stable_baselines3.common.callbacks import EvalCallback
from stable_baselines3.common.logger import configure
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.monitor import Monitor


def train_agent():
    # 1. AppleGameEnv 환경 생성
    env = AppleGameEnv(m=36, n=36, max_steps=10000)

    # check_env(env)

    # 2. PPO 에이전트 설정 (여기서는 MLP 정책 사용)
    model = PPO("CnnPolicy", env, verbose=1)

    log_dir = "./tmp/logs"

    # $ tensorboard --logdir ./examples/tmp/logs/eval 로 tensorboard 실행
    new_logger = configure(log_dir, ["stdout", "csv", "tensorboard"])
    model.set_logger(new_logger)

    eval_env = AppleGameEnv(m=36, n=36, max_steps=10000)
    eval_env = Monitor(eval_env, log_dir)

    # Use deterministic actions for evaaluation
    eval_callback = EvalCallback(eval_env, best_model_save_path=log_dir,
                                 log_path=log_dir, eval_freq=500, n_eval_episodes=5,
                                 deterministic=True, render=False)

    model.learn(total_timesteps=100_000, callback=eval_callback)

    # # 3. 체크포인트 콜백 설정 (1000 스텝마다 모델 저장)
    # checkpoint_callback = CheckpointCallback(save_freq=1000, save_path="./agents/", name_prefix="ppo_apple_game")

    # # 4. 학습 시작 (여기서는 10,000 타임스텝 동안 학습)
    # model.learn(total_timesteps=100000, callback=checkpoint_callback)

    # 5. 최종 모델 저장
    model.save(log_dir + "ppo_apple_game_final")


if __name__ == "__main__":
    train_agent()
