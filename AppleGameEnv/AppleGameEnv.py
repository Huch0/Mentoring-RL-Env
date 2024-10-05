import gymnasium as gym
import numpy as np
import AppleGameEnv.AppleGame as AppleGame


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


        # self.action_space = gym.spaces.Box(low=0, high=1, shape=(2,))
        # self.observation_space = gym.spaces.Box(low=0, high=10, shape=(m, n))