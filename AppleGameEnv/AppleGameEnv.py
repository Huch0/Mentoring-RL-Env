import gymnasium as gym
import numpy as np
from AppleGameEnv.AppleGame import AppleGame


class AppleGameEnv(gym.Env):
    def __init__(self, m=36, n=36, max_steps=100):
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

        # m x n 크기의 게임판
        self.observation_space = gym.spaces.Box(low=0, high=255, shape=(1, m, n), dtype=np.uint8)

        # 가능한 행동: (x1, y1), (x2, y2) 0 ~ 1
        self.action_space = gym.spaces.MultiDiscrete([m, n, m, n])

    def reset(self, seed=None):
        """ 게임 초기화
        """
        self.steps = 0
        self.game.reset()
        return self.game.get_obs(), self._get_info()

    # 0~1 정규화
    def _get_obs(self):
        return (self.game.get_obs() - 1) / 8

    def _get_info(self):
        return {"score": self.game.score, "steps": self.game.steps}

    def step(self, action):
        """ 행동을 받아 게임을 진행

        Args:
            action (_type_): 플레이어가 지정한 사각형의 좌표(좌상단, 우하단)
        """
        x1, y1, x2, y2 = action
        # 0~1 정규화
        x1_normalized = x1 / (self.m - 1)
        y1_normalized = y1 / (self.n - 1)
        x2_normalized = x2 / (self.m - 1)
        y2_normalized = y2 / (self.n - 1)

        self.steps += 1

        self.game.step(((x1, y1), (x2, y2)))
        terminated = self.game.is_game_over()
        truncated = self.game.steps >= self.game.max_steps

        # if terminated or truncated:
        #     raise ValueError(
        #         f"terminated: {terminated}, truncated: {truncated}, max_step: {self.game.max_steps}, steps: {self.game.steps}")

        reward = self.game.score

        return self.game.get_obs(), reward, terminated, truncated, self._get_info()
