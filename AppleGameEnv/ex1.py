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
        self.score = 0
        self.grid = np.zeros((m, n))  # 게임판 10x10 배열
        self.circles = []  # 동그라미 저장 리스트
        self.texts = []  # 텍스트 저장 리스트
        self.selected_coords = []  # 선택한 좌표 저장 리스트

    def reset(self):
        """ 게임 초기화 """
        self.steps = 0
        self.score = 0
        self.grid = np.random.randint(1, 10, size=(self.m, self.n))  # 1~9 랜덤 숫자 생성

    def step(self, square):
        """ 선택된 영역의 숫자 합이 10인지 확인하고, 10이면 해당 사각형 내부 숫자 삭제 """
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
            # 점수 추가 및 해당 영역 사과 제거
            self.score += np.count_nonzero(selected_area)
            self.grid[row_start:row_end+1, col_start:col_end+1] = 0
            print(f"10점이 맞습니다! {np.count_nonzero(selected_area)}개의 사과를 먹었습니다.")
        else:
            print(f"합계가 {total}입니다. 사과를 먹지 못했습니다.")

        self.steps += 1

    def is_game_over(self):
        """ 게임 종료 여부 확인 """
        if self.steps >= self.max_steps:
            print("최대 턴 수에 도달했습니다.")
            return True
        elif np.sum(self.grid) < 10:
            print("게임판에 남은 숫자의 합이 10 미만입니다.")
            return True
        return False

    def get_score(self):
        """ 현재 점수 반환 """
        return self.score

    def render(self, render_mode="text"):
        """ 게임판의 상태를 플롯으로 표시 """
        if render_mode == "text":
            print(self.grid)
        elif render_mode == "plot":
            fig, ax = plt.subplots(figsize=(8, 8))
            self.circles = []
            self.texts = []

            # 동그라미와 숫자 추가
            for i in range(self.grid.shape[0]):
                row_circles = []
                row_texts = []
                for j in range(self.grid.shape[1]):
                    circle = plt.Circle((j, 9 - i), 0.4, color='black', fill=False, lw=2)  # y 좌표 반전
                    ax.add_patch(circle)
                    row_circles.append(circle)  # 원 저장

                    text = plt.text(j, 9 - i, int(self.grid[i, j]), ha='center', va='center', color='black')  # 숫자 추가
                    row_texts.append(text)  # 텍스트 저장

                self.circles.append(row_circles)
                self.texts.append(row_texts)

            # 그리드와 플롯 설정
            ax.set_xticks(np.arange(-.5, 10, 1), minor=True)
            ax.set_yticks(np.arange(-.5, 10, 1), minor=True)
            ax.grid(which='minor', color='w', linestyle='-', linewidth=2)

            def onclick(event):
                if event.xdata is None or event.ydata is None or event.inaxes is None or event.inaxes == ax_button:
                    return

                x_click = int(event.xdata + 0.5)
                y_click = int(event.ydata + 0.5)

                if 0 <= x_click < 10 and 0 <= y_click < 10:
                    value = self.grid[9 - y_click, x_click]  # y 좌표 변환
                    print(f"Clicked Value: {value}, Coordinates: ({x_click}, {y_click})")
                    
                    if len(self.selected_coords) < 2:
                        self.selected_coords.append((x_click, y_click))
                        self.circles[9 - y_click][x_click].set_edgecolor('red')
                        fig.canvas.draw()

                    if len(self.selected_coords) == 2:
                        x1, y1 = self.selected_coords[0]
                        x2, y2 = self.selected_coords[1]

                        xmin, xmax = sorted([x1, x2])
                        ymin, ymax = sorted([y1, y2])

                        for i in range(ymin, ymax + 1):
                            for j in range(xmin, xmax + 1):
                                self.circles[9 - i][j].set_edgecolor('red')

                        fig.canvas.draw()

            fig.canvas.mpl_connect('button_press_event', onclick)

            ax_button = plt.axes([0.4, 0.01, 0.2, 0.05])
            button = Button(ax_button, 'Submit')

            def submit(event):
                for i in range(self.grid.shape[0]):
                    for j in range(self.grid.shape[1]):
                        if self.circles[i][j].get_edgecolor() == (1.0, 0.0, 0.0, 1.0):  # 빨간색 원 삭제
                            self.circles[i][j].remove()
                            self.texts[i][j].remove()
                self.selected_coords.clear()
                fig.canvas.draw()
                print("Removed selected apples.")

            button.on_clicked(submit)

            plt.show()


if __name__ == "__main__":
    game = AppleGame()
    game.reset()
    game.render(render_mode="text")  # 초기 게임판 상태 출력

    done = False
    while not done:
        done = game.is_game_over()
        print(f"현재 점수: {game.get_score()}")
        if done:
            print("게임 종료!")
