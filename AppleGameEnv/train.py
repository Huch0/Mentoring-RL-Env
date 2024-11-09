import gymnasium as gym
from stable_baselines3 import PPO  
from AppleGameEnv.AppleGameEnv import AppleGameEnv  
from stable_baselines3.common.callbacks import CheckpointCallback

def train_agent():
    # 1. AppleGameEnv 환경 생성
    env = AppleGameEnv(m=10, n=10, max_steps=100)
    
    # 2. PPO 에이전트 설정 (여기서는 MLP 정책 사용)
    model = PPO("MlpPolicy", env, verbose=1)
    
    # 3. 체크포인트 콜백 설정 (1000 스텝마다 모델 저장)
    checkpoint_callback = CheckpointCallback(save_freq=1000, save_path="./agents/", name_prefix="ppo_apple_game")
    
    # 4. 학습 시작 (여기서는 10,000 타임스텝 동안 학습)
    model.learn(total_timesteps=10000, callback=checkpoint_callback)
    
    # 5. 최종 모델 저장
    model.save("ppo_apple_game_final")

if __name__ == "__main__":
    train_agent()
