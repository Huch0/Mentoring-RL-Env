import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

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
        self.steps = 0
        self.score = 0
        self.grid = np.random.randint(1, 10, size=(self.m, self.n))

    def get_obs(self) -> np.ndarray:
        """ 게임판의 상태를 반환

        Returns:
            self.grid (np.ndarray): 게임판의 상태
        """
        return self.grid

    def step(self, square):
        """ 플레이어의 행동을 받아 게임을 진행

        플레이어가 지정한 사각형 내의 숫자의 합이 10인지 확인
        10이라면 해당 사각형 안의 사과의 개수를 점수로 추가하고 사과를 제거
        10이 아니라면 아무 일도 일어나지 않음

        Args:
            square (_type_): 플레이어가 지정한 사각형의 좌표(좌상단, 우하단)
        """
        (top_left, bottom_right) = square
        row_start, col_start = top_left
        row_end, col_end = bottom_right

        if row_start > row_end or col_start > col_end:
            print("잘못된 좌표 범위입니다.")
            return

        # 선택된 영역의 숫자 합을 계산
        selected_area = self.grid[row_start:row_end+1, col_start:col_end+1]
        total = np.sum(selected_area)

        if total == 10:
            # 점수 추가 및 해당 영역 사과 제거 (0으로 설정)
            self.score += np.count_nonzero(selected_area)
            self.grid[row_start:row_end+1, col_start:col_end+1] = 0
            print(f"10점이 맞습니다! {np.count_nonzero(selected_area)}개의 사과를 먹었습니다.")
        else:
            print(f"합계가 {total}입니다. 사과를 먹지 못했습니다.")

        self.steps += 1

    def is_game_over(self):
        """ 게임이 종료 여부 반환
        1. 현재 턴이 최대 턴 수에 도달했을 때
        2. 게임판에 남아있는 사과의 합이 10 미만일 때
        """
        if self.steps >= self.max_steps:
            print("최대 턴 수에 도달했습니다.")
            return True
        elif np.sum(self.grid) < 10:
            print("게임판에 남은 숫자의 합이 10 미만입니다.")
            return True
        return False

    def get_score(self):
        """ 현재 에피소드의 현재 점수 반환

        Returns:
            self.score (int): 현재 에피소드의 현재 점수
        """
        return self.score

    def render(self, render_mode="plot"):
        """ 현재 게임판의 상태를 이미지로 리턴
        render_mode에 따라 다른 이미지를 리턴
        """
        if render_mode == "text":
            print(self.grid)
        elif render_mode == "plot":
            fig, ax = plt.subplots()
            ax.matshow(self.grid, cmap='cool')

            for i in range(self.m):
                for j in range(self.n):
                    c = self.grid[i, j]
                    ax.text(j, i, str(int(c)), va='center', ha='center')

            plt.show()


if __name__ == "__main__":
    game = AppleGame()
    game.reset()
    game.render(render_mode="text")  # 초기 게임판 상태 출력

    done = False
    while not done:
        print("좌상단 좌표를 입력하세요 (예: 0 0): ")
        square_1 = tuple(map(int, input().split()))
        print("우하단 좌표를 입력하세요 (예: 1 1): ")
        square_2 = tuple(map(int, input().split()))

        game.step((square_1, square_2))
        game.render(render_mode="text")  # 상태 업데이트 후 출력

        done = game.is_game_over()
        print(f"현재 점수: {game.get_score()}")
        if done:
            print("게임 종료!")
