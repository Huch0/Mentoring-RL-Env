import gymnasium as gym
import numpy as np
from AppleGame import AppleGame


class AppleGameEnv(gym.Env):
    def __init__(self, m=36, n=36, max_steps=1000):
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

        self.reward = 0
        self.cur_score = 0

        self.game = AppleGame(m, n, max_steps)

        # m x n 크기의 게임판 [1, 9]
        self.observation_space = gym.spaces.Box(low=0, high=255, shape=(1, m, n), dtype=np.uint8)

        # 가능한 행동: (x1, y1), (x2, y2) [-1, 1]
        self.action_space = gym.spaces.Box(low=-1, high=1, shape=(4,), dtype=np.float32)

    def reset(self, seed=None, options=None):
        """ 게임 초기화
        """
        if options is not None:
            raise ValueError(f"options: {options}")

        self.steps = 0

        self.reward = 0
        self.cur_score = 0
        self.game.reset(seed)
        return self.game.get_obs(), self._get_info()

    def _get_obs(self):
        return self.game.get_obs()

    def _get_info(self):
        return {
            "score": self.game.score,
            "steps": self.game.steps,
            "reward": self.reward
        }

    def step(self, action):
        """ 행동을 받아 게임을 진행

        Args:
            action (_type_): 플레이어가 지정한 사각형의 좌표(좌상단, 우하단)
        """
        # [-1. 1] -> [0, 1]
        action = (action + np.ones(4)) / 2

        # [0, 1] -> [0, m - 1] / [0, n - 1]
        # e.g. mxn = 10x10
        # [0, 0.1) -> 0
        # [0.1, 0.2) -> 1
        # [0.2, 0.3) -> 2
        # [0.9, 1) -> 9

        action = (action * np.array([self.m, self.n, self.m, self.n])).astype(np.int8)

        self.game.step(action)

        terminated = self.game.is_game_over()
        truncated = self.game.steps >= self.game.max_steps

        self.reward = self.game.score - self.cur_score
        self.cur_score = self.game.score

        return self.game.get_obs(), self.reward, terminated, truncated, self._get_info()

    def render(self, render_mode="console"):
        """ 게임판을 출력
        """
        if render_mode == "console":
            return self.game.render()
        else:
            raise NotImplementedError
