import gymnasium as gym
import numpy as np
from AppleGameEnv.AppleGame import AppleGame


class AppleGameEnv(gym.Env):
    def __init__(self, m=10, n=10, max_steps=100):
        """ AppleGame 환경 생성

        Args:
            m (int, optional): 게임판의 행 수
            n (int, optional): 게임판의 열 수
            max_steps (int, optional): 게임의 최대 턴 수
        """
        self.m = m
        self.n = n

        self.steps = 0
        self.max_steps = max_steps

        self.game = AppleGame(m, n, max_steps)

        # m x n 크기의 게임판 0 ~ 1
        self.observation_space = gym.spaces.Box(low=1, high=9, shape=(m, n), dtype=np.int8)

        # 가능한 행동: (x1, y1), (x2, y2) 0 ~ 1
        # self.action_space = gym.spaces.MultiDiscrete([m, n, m, n])

    def reset(self):
        """ 게임 초기화
        """
        self.steps = 0
        self.game.reset()
        return self.game.get_obs(), self._get_info()

    def _get_obs(self):
        return self.game.get_obs()

    def _get_info(self):
        return {"score": self.game.score, "steps": self.game.steps}

    def step(self, action):
        """ 행동을 받아 게임을 진행

        Args:
            action (_type_): 플레이어가 지정한 사각형의 좌표(좌상단, 우하단)
        """
        self.game.step(action)

        terminated = self.game.is_game_over()
        truncated = self.game.steps >= self.game.max_steps

        reward = self.game.score

        return self.game.get_obs(), reward, terminated, truncated, self._get_info()
