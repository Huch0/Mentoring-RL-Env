import numpy as np

class AppleGame():
    def __init__(self, m=36, n=36, max_steps=100):
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
        self.grid = np.zeros((1, m, n), dtype=np.uint8)

    def reset(self):
        """ 게임 초기화
        """
        self.score = 0

        self.steps = 0
        self.grid = np.random.randint(1, 10, size=(1, self.m, self.n), dtype=np.uint8)

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
            sqaure (_type_): 플레이어가 지정한 사각형의 좌표(좌상단, 우하단)
        """
        (x1,y1), (x2,y2) = square

        left, right = sorted((x1, x2))
        top, bottom = sorted((y1, y2))



        selected = self.grid[0, left:right+1, top:bottom+1]

        total = np.sum(selected)
        
        if total == 10:
            self.score += np.count_nonzero(selected)
            self.grid[0, left:right+1, top:bottom+1]=0
            
        self.steps += 1
        self.render()


    def is_game_over(self):
        """ 게임이 종료 여부 반환
        1. 현재 턴이 최대 턴 수에 도달했을 때
        2. 게임판에 남아있는 사과의 합이 10 미만일 때
        """
        if self.steps >= self.max_steps or np.sum(self.grid) < 10:
            return True
        return False

    def get_score(self):
        """ 현재 에피소드의 현재 점수 반환

        Returns:
            self.score (int): 현재 에피소드의 현재 점수
        """
        return self.score

    def render(self, render_mode='console'):
        """ 현재 게임판의 상태를 이미지로 리턴
        render_mode에 따라 다른 이미지를 리턴
        """
        # 열 번호 출력
        if render_mode == 'console':
            print("     " + " ".join([f"{i:2}" for i in range(self.n)]))  # 열 번호
            print("   " + "-" * (self.n * 3))  # 구분선
        
        # 행 번호와 함께 각 행 출력
            for i, row in enumerate(self.grid):
                print(f"{i:2} | " + " ".join([f"{int(x):2}" for x in row]))  # 각 행에 행 번호 추가
            remaining_steps = self.max_steps - self.steps
            print('남은 스텝: ',remaining_steps)
            print('점수: ',self.score)


if __name__ == "__main__":
    game = AppleGame()
    game.reset()
    game.render()

    done = False
    while not done:
        square_1 = tuple(map(int, input().split()))
        square_2 = tuple(map(int, input().split()))
        game.step((square_1, square_2))
        game.render()

        done = game.is_game_over()
        print(game.get_score())