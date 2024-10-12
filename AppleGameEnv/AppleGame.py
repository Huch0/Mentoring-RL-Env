import numpy as np

class AppleGame():
    def __init__(self, m=5, n=5, max_steps=100):
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
        self.steps = 0
        self.grid = np.random.randint(1, 10, size=(self.m, self.n))  # 1~9 사이의 숫자로 게임판 초기화
        print("게임이 초기화되었습니다.")

    def get_obs(self) -> np.ndarray:
        """ 게임판의 상태를 반환

        Returns:
            self.grid (np.ndarray): 게임판의 상태
        """
        return self.grid

    def step(self, square):
        """ 플레이어의 행동을 받아 게임을 진행

        플레이어가 지정한 사각형 내의 숫자의 합이 10인지 확인
        10이라면 해당 사각형안의 사과의 개수를 점수로 추가하고 사과를 제거
        10이 아니라면 아무일도 일어나지 않음

        Args:
            square (tuple): 플레이어가 지정한 사각형의 좌표(좌상단, 우하단)
        """
        top_left, bottom_right = square
        x1, y1 = top_left
        x2, y2 = bottom_right

        # 선택된 사각형 내의 숫자 합 계산
        selected_region = self.grid[x1:x2+1, y1:y2+1]
        total_sum = np.sum(selected_region)

        # 10이라면 해당 사과 제거 후 점수 추가
        if total_sum == 10:
            apples_count = np.count_nonzero(selected_region)
            self.score += apples_count
            self.grid[x1:x2+1, y1:y2+1] = 0  # 사과 제거 (0으로 만들기)
            print(f"{square} 사각형의 합이 10입니다. {apples_count}개의 사과가 제거되었습니다. 점수에 추가됨.")
        else:
            print(f"{square} 사각형의 합이 {total_sum}입니다. 아무 일도 일어나지 않았습니다.")

        # 한 턴이 진행되었으므로 steps 증가
        self.steps += 1

    def check_possible_ten(self):
        """ 가능한 모든 사각형에서 합이 10이 되는 경우가 있는지 확인 """
        for x1 in range(self.m):
            for y1 in range(self.n):
                for x2 in range(x1, self.m):
                    for y2 in range(y1, self.n):
                        selected_region = self.grid[x1:x2+1, y1:y2+1]
                        total_sum = np.sum(selected_region)
                        # 합이 10이 되는 사각형이 있다면 True 반환
                        if total_sum == 10:
                            return True
        return False

    def is_game_over(self):
        """ 게임 종료 여부 반환
        1. 현재 턴이 최대 턴 수에 도달했을 때
        2. 게임판에 남아있는 사과의 합이 10 미만일 때
        3. 더 이상 10을 만들 수 있는 사각형이 없을 때
        """
        if self.steps >= self.max_steps:
            print("최대 턴 수에 도달했습니다. 게임 종료!")
            return True
        elif np.sum(self.grid) < 10:
            print("게임판에 남은 사과의 합이 10 미만입니다. 게임 종료!")
            return True
        elif not self.check_possible_ten():
            print("더 이상 10을 만들 수 있는 사각형이 없습니다. 게임 종료!")
            return True
        else:
            return False

    def get_score(self):
        """ 현재 에피소드의 현재 점수 반환

        Returns:
            self.score (int): 현재 에피소드의 현재 점수
        """
        return self.score

    def render(self, render_mode="text"):
        """ 현재 게임판의 상태를 이미지로 리턴
        render_mode에 따라 다른 이미지를 리턴
        """
        if render_mode == "text":
            print(self.grid)  # 텍스트로 게임판 출력


if __name__ == "__main__":
    game = AppleGame(m=5, n=5)
    game.reset()
    game.render()  # 게임판 출력

    done = False
    while not done:
        # 좌상단 좌표 입력
        print("좌상단 좌표 (x1, y1)를 입력하세요: ")
        square_1 = tuple(map(int, input().split()))
        
        # 우하단 좌표 입력
        print("우하단 좌표 (x2, y2)를 입력하세요: ")
        square_2 = tuple(map(int, input().split()))
        
        game.step((square_1, square_2))

        game.render()

        done = game.is_game_over()
        print(f"현재 점수: {game.get_score()}")