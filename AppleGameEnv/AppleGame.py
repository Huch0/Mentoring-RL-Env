import numpy as np
import matplotlib.pyplot as plt


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
        pass

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
            square (_type_): 플레이어가 지정한 사각형의 좌표(좌상단, 우하단)
        """
        # 배열 행, 열 순서라 x, y 반대로 해줘야..
        (x1, y1), (x2, y2) = square
        selected = self.grid[y1:y2+1, x1:x2+1] 
        selected_sum = np.sum(selected)
        
        if selected_sum == 10:
            self.score += np.count_nonzero(selected)
            self.grid[y1:y2+1, x1:x2+1] = 0 
            
        self.steps += 1    

    def is_game_over(self):
        """ 게임이 종료 여부 반환
        1. 현재 턴이 최대 턴 수에 도달했을 때
        2. 게임판에 남아있는 사과의 합이 10 미만일 때
        """
        if self.steps == self.max_steps:
            return True
        # 전체합이 아니라 더 이상 가능한 경우가 없을 때 종료시켜야하지 않나?
        # 그럼 스텝마다 검사하나? 그건 좀..
        if np.sum(self.grid) < 10:
            return True
        
        return False
        
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
        if render_mode == 'text':
            for row in self.grid:
                print(" ".join(map(str, row)))
            print()
        
        # 이미지로 하는 법 모르겠음
        elif render_mode == 'image':
            # 이미지를 사용한 게임판 출력
            plt.imshow(self.grid, cmap='viridis', interpolation='nearest')
            plt.colorbar()  # 값의 범위를 확인할 수 있도록 컬러바 추가
            plt.title("Apple Game Board")
            plt.show()
        else:
            raise ValueError("Invalid render_mode. Choose 'text' or 'image'.")


if __name__ == "__main__":
    game = AppleGame()
    game.reset()

    done = False
    while not done:
        game.render('text') # 일단 텍스트로

        try:
            print(f"현재 점수: {game.get_score()}, 진행된 스텝: {game.steps}")
            x1, y1 = map(int, input("좌상단 좌표 (x1 y1): ").split())
            x2, y2 = map(int, input("우하단 좌표 (x2 y2): ").split())

            x1, y1, x2, y2 = x1 - 1, y1 - 1, x2 - 1, y2 - 1

            if x1 > x2 or y1 > y2:
                x1, x2 = x2, x1
                y1, y2 = y2, y1

            # 좌표가 유효한 범위 내에 있는지 확인
            if not (0 <= x1 <= x2 < game.m and 0 <= y1 <= y2 < game.n):
                print("잘못된 좌표입니다. 좌표는 게임판의 크기 내에서 올바르게 입력되어야 합니다.")
                continue

        except ValueError:
            print("잘못된 입력입니다. 좌표는 정수로 입력해야 합니다.")
            continue

        # 게임 진행
        game.step(((x1, y1), (x2, y2)))

        # 게임 종료 여부 확인
        done = game.is_game_over()

    print("게임 종료!")
    print(f"최종 점수: {game.get_score()}")

