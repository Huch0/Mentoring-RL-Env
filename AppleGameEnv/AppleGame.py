import numpy as np


class AppleGame():
    def __init__(self, m=10, n=10, max_steps=100):
        """ AppleGame 객체 생성

        Args:
            m (int, optional): 게임판의 행 수
            n (int, optional): 게임판의 열 수
            max_steps (int, optional): 게임의 최대 턴 수
        """
        self.m = m
        self.n = n

        self.steps = 0
        self.max_steps = max_steps

        # 현재 에피소드의 총 점수
        self.score = 0
        # 게임판
        self.grid = np.zeros((m, n))

    def reset(self):
        """ 게임 초기화
        """
        self.score = 0
        self.grid = np.random.randint(1, 10, size=(self.m, self.n))
        pass

    def get_obs(self) -> np.ndarray:
        """ 게임판의 상태를 반환

        Returns:
            self.grid (np.ndarray): 게임판의 상태
        """
        return self.grid

    def step(self, sqaure):
        """ 플레이어의 행동을 받아 게임을 진행

        플레이어가 지정한 사각형 내의 숫자의 합이 10인지 확인
        10이라면 해당 사각형안의 사과의 개수를 점수로 추가하고 사과를 제거
        10이 아니라면 아무일도 일어나지 않음

        Args:
            sqaure (_type_): 플레이어가 지정한 사각형의 좌표(좌상단, 우하단)
        """
        pass

    def is_game_over(self):
        """ 게임이 종료 여부 반환
        1. 현재 턴이 최대 턴 수에 도달했을 때
        2. 게임판에 남아있는 사과의 합이 10 미만일 때
        """
        pass

    def get_score(self):
        """ 현재 에피소드의 현재 점수 반환

        Returns:
            self.score (int): 현재 에피소드의 현재 점수
        """
        return self.score

    def render(self, render_mode):
        """ 현재 게임판의 상태를 이미지로 리턴
        render_mode에 따라 다른 이미지를 리턴
        """
        pass


if __name__ == "__main__":
    game = AppleGame()
    game.reset()
    print(game.get_obs())

    done = False
    while not done:
        square_1 = tuple(map(int, input().split()))
        sqaure_2 = tuple(map(int, input().split()))
        game.step((square_1, sqaure_2))

        print(game.get_obs())
        done = game.is_game_over()
        print(game.get_score())
        print(done)