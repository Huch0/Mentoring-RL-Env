import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

# 13x13의 1부터 9까지의 숫자로 이루어진 랜덤 행렬 생성
matrix = np.random.randint(1, 10, size=(10, 10))

# 각 셀에 동그라미와 숫자 추가
circles = []  # 원을 저장할 리스트
texts = []    # 텍스트를 저장할 리스트
fig, ax = plt.subplots(figsize=(8, 8))
input_10 = []  # 빨간색으로 칠해진 원들의 좌표를 저장할 리스트
selected_coords = []  # 선택한 두 좌표를 저장할 리스트

for i in range(matrix.shape[0]):
    row_circles = []
    row_texts = []
    for j in range(matrix.shape[1]):
        # 동그라미 추가
        circle = plt.Circle((j, 12 - i), 0.4, color='black', fill=False, lw=2)  # y 좌표 반전
        ax.add_patch(circle)
        row_circles.append(circle)  # 원을 리스트에 저장

        # 동그라미 안에 숫자 추가
        text = plt.text(j, 12 - i, matrix[i, j], ha='center', va='center', color='black')  # y 좌표 반전
        row_texts.append(text)  # 텍스트를 리스트에 저장

    circles.append(row_circles)
    texts.append(row_texts)

# 그리드와 플롯 설정
ax.set_xticks(np.arange(-.5, 13, 1), minor=True)
ax.set_yticks(np.arange(-.5, 13, 1), minor=True)
ax.grid(which='minor', color='w', linestyle='-', linewidth=2)

# 클릭 이벤트 핸들러 함수
def onclick(event):
    global selected_coords

    # 클릭이 플롯 영역 밖에서 발생한 경우 무시
    if event.xdata is None or event.ydata is None or event.inaxes is None or event.inaxes == ax_button:
        return
    
    x_click = int(event.xdata + 0.5)
    y_click = int(event.ydata + 0.5)

    # 좌표 변환
    if 0 <= x_click < 13 and 0 <= y_click < 13:
        value = matrix[12 - y_click, x_click]  # y 좌표 반전 적용
        x_coord = x_click + 1
        y_coord = y_click + 1
        print(f"Clicked Value: {value}, Coordinates: ({x_coord}, {y_coord})")
        
        # 좌표 저장 및 원 색상 변경
        if len(selected_coords) < 2:
            selected_coords.append((x_click, y_click))
            circles[12 - y_click][x_click].set_edgecolor('red')
            fig.canvas.draw()  # 화면 업데이트

        # 두 번째 좌표 선택 완료 시 사각형 내 원들을 빨간색으로 변경
        if len(selected_coords) == 2:
            x1, y1 = selected_coords[0]
            x2, y2 = selected_coords[1]

            # 사각형 범위 계산
            xmin, xmax = sorted([x1, x2])
            ymin, ymax = sorted([y1, y2])

            # 사각형 내부에 있는 원들을 빨간색으로 변경
            for i in range(ymin, ymax + 1):
                for j in range(xmin, xmax + 1):
                    circles[12 - i][j].set_edgecolor('red')

            fig.canvas.draw()  # 화면 업데이트
            selected_coords.clear()  # 선택 좌표 초기화하여 새로운 사각형 선택 가능하게 함

 # 제출 버튼 클릭 이벤트 핸들러
def submit(event):
    global input_10, selected_coords
    input_10.clear()  # 리스트 초기화
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            if circles[i][j].get_edgecolor() == (1.0, 0.0, 0.0, 1.0):  # 빨간색 원인 경우
                x_coord = j + 1
                y_coord = 13 - i
                input_10.append([x_coord, y_coord])  # 좌표 저장

                # 원이 아직 존재하는지 확인한 후 삭제
                if circles[i][j] in ax.patches:  # patches에서 확인
                    circles[i][j].remove()  # 원 삭제
                if texts[i][j] in ax.texts:  # 텍스트도 동일하게 확인
                    texts[i][j].remove()    # 숫자 삭제
    selected_coords.clear()  # 좌표 초기화
    fig.canvas.draw()  # 화면 업데이트
    print(f"Submitted Coordinates: {input_10}")


# 제출 버튼 생성
ax_button = plt.axes([0.4, 0.01, 0.2, 0.05])
button = Button(ax_button, 'Submit')
button.on_clicked(submit)

# 클릭 이벤트 연결
cid = fig.canvas.mpl_connect('button_press_event', onclick)

plt.show()
