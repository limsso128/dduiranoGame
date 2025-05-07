import tkinter as tk  # GUI 라이브러리
from tkinter import messagebox #확인창
from collections import deque
from tkinter import colorchooser #그 뭐냐 컬러 팔레트래

root = tk.Tk()  # 창 생성
root.geometry("1100x800")  # 창 크기
root.resizable(False, False)
root.title("Draw Image")

PIXEL_SIZE = 15
#44*47
CANVAS_WIDTH = 44
CANVAS_HEIGHT = 47

HEAD_HEIGHT = 17
BODY_HEIGHT = 22
FOOT_HEIGHT = 8

grid_colors = [['#d4d5d6' for _ in range(CANVAS_WIDTH)] for _ in range(CANVAS_HEIGHT)]
drag_log = [] #현재 진행상황

fill_mode = False #채우기

start_drag = False
end_drag = False

is_there_pixel_head = False
is_there_pixel_body = False
is_there_pixel_foot = False

linked_line = False

current_color = 'black' #현재 색상

#============================================프레임==============================================

#오른쪽 프레임 (캔버스)
right_frame = tk.Frame(root, bg='#447d38', width=CANVAS_WIDTH * PIXEL_SIZE)
right_frame.grid(row=1, column=1)
right_frame.grid_propagate(False)

#위 프레임
top_frame = tk.Frame(root, height=40, bg="#97ff82")
top_frame.grid(row=0, column=0, columnspan=2, sticky="ew") #es -> 양옆으로, ns -> 위아래로

#아래 프레임
bottom_frame = tk.Frame(root, height=40, bg="#97ff82")
bottom_frame.grid(row=2, column=0, columnspan=2, sticky="ew")

#왼 프레임
left_frame = tk.Frame(root, width=400, bg="#97ff82")
left_frame.grid(row=1, column=0, sticky="ns")
left_frame.grid_propagate(False)  # 크기 고정

#가이드 프레임
guide_frame = tk.Frame(left_frame, bg="white", width=340, height=250)
guide_frame.place(x=30)
guide_frame.pack_propagate(False)

#툴 프레임
color_frame = tk.Frame(left_frame, bg="white", width=340, height=400)
color_frame.place(x=30, y= 290)
color_frame.pack_propagate(False)

text1 = tk.StringVar()
text2 = tk.StringVar()
text3 = tk.StringVar()
text4 = tk.StringVar()
text5 = tk.StringVar()

text5.set("⭐검은색 테두리 추천!")
label1 = tk.Label(guide_frame, textvariable=text1, font=("HY헤드라인M", 15), fg="red", bg="white")
label1.place(x=16, y=15)
label2 = tk.Label(guide_frame, textvariable=text2, font=("HY헤드라인M", 15), fg="red", bg="white")
label2.place(x=16, y=65)
label3 = tk.Label(guide_frame, textvariable=text3, font=("HY헤드라인M", 15), fg="red", bg="white")
label3.place(x=16, y=115)
label4 = tk.Label(guide_frame, textvariable=text4, font=("HY헤드라인M", 15), fg="red", bg="white")
label4.place(x=16, y=165)
label5 = tk.Label(guide_frame, textvariable=text5, font=("HY헤드라인M", 15), fg="pink", bg="white")
label5.place(x=14, y=210)

#가이드 텍스트
def cheak_text(str1, c1, str2, c2, str3, c3, str4, c4):
    text1.set(str1)
    label1.config(fg=c1)
    text2.set(str2)
    label2.config(fg=c2)
    text3.set(str3)
    label3.config(fg=c3)
    text4.set(str4)
    label4.config(fg=c4)

# 캔버스 (중앙 프레임 안에)
canvas = tk.Canvas(right_frame, width=CANVAS_WIDTH * PIXEL_SIZE, height=CANVAS_HEIGHT * PIXEL_SIZE, bg='light gray', bd=0, highlightthickness=0)
canvas.pack(padx=20, pady=5)

root.grid_columnconfigure(0, weight=0)  # 왼쪽 프레임
root.grid_columnconfigure(1, weight=1)  # 캔버스

#그리드 생성
def show_grid():
    for i in range(CANVAS_WIDTH):
        for j in range(CANVAS_HEIGHT):
            canvas.create_rectangle(i * PIXEL_SIZE, j * PIXEL_SIZE,
                                     (i + 1) * PIXEL_SIZE, (j + 1) * PIXEL_SIZE,
                                     outline='', fill='#d4d5d6')
#그림 그리기(클릭, 드래그)
def drawing_grid(event):
    x = event.x // PIXEL_SIZE
    y = event.y // PIXEL_SIZE  #이거 주석 아님
    if 0 <= x < CANVAS_WIDTH and 0 <= y < CANVAS_HEIGHT:
        if fill_mode:  # 채우기 모드일 때만 flood fill
            target_color = grid_colors[y][x]
            if target_color != current_color:
                flood_fill(x, y, target_color, current_color)
        else:
            grid_colors[y][x] = current_color
            canvas.create_rectangle(
                x * PIXEL_SIZE, y * PIXEL_SIZE,
                (x + 1) * PIXEL_SIZE, (y + 1) * PIXEL_SIZE,
                fill=current_color, outline=""
            )

#선 연결 확인
def cheak_linked_line(start_y, end_y):
    for y in range(start_y, end_y):
        has_pixel = False
        for x in range(CANVAS_WIDTH):
            if grid_colors[y][x] != '#d4d5d6':
                has_pixel = True
                break  #픽셀이 있으면 멈춤
        if not has_pixel:
            return False  #한 행이라도 비어 있으면 False
    return True  #모든 행에 픽셀이 있음

#모두삭제
def entrie_del():
    for y in range(CANVAS_HEIGHT):
        for x in range(CANVAS_WIDTH):
            grid_colors[y][x] = '#d4d5d6'
            canvas.create_rectangle(
                x * PIXEL_SIZE, y * PIXEL_SIZE,
                (x + 1) * PIXEL_SIZE, (y + 1) * PIXEL_SIZE,
                fill='#d4d5d6', outline=""
            )


#채우기 로직
def flood_fill(x, y, target_color, fill_color):
    if target_color == fill_color:
        return   #이미 갘은 색

    queue = deque()
    queue.append((x, y))

    while queue:
        cx, cy = queue.popleft()

        # 범위 체크
        if cx < 0 or cx >= CANVAS_WIDTH or cy < 0 or cy >= CANVAS_HEIGHT:
            continue
        # 다른 색이면 무시
        if grid_colors[cy][cx] != target_color:
            continue

        # 색 칠하기
        grid_colors[cy][cx] = fill_color
        canvas.create_rectangle(
            cx * PIXEL_SIZE, cy * PIXEL_SIZE,
            (cx + 1) * PIXEL_SIZE, (cy + 1) * PIXEL_SIZE,
            fill=fill_color, outline=""
        )
        #4방
        queue.append((cx + 1, cy))
        queue.append((cx - 1, cy))
        queue.append((cx, cy + 1))
        queue.append((cx, cy - 1))

#행에 픽셀이 그려져 있는지 확인
def check_y_properly_drawn(start_y, end_y):
    for y in range(start_y, end_y):
        for x in range(CANVAS_WIDTH):
            if grid_colors[y][x] != '#d4d5d6':
                return True
    return False

def check_x_properly_drawn(x):
    for y in range(CANVAS_HEIGHT):
        if grid_colors[y][x] != '#d4d5d6':
             return True
    return False

# 적절한 그림 조절 루프
def ccc():
    global is_there_pixel_head, is_there_pixel_body, is_there_pixel_foot, linked_line #전역 변수 사용
    #is_there_pixel_head = check_properly_drawn(0, 16)

    if cheak_linked_line(5, 45):
        linked_line = True
        str4 = "✓ 선이 잘 연결되어 있습니다!"
        c4 = "green"
    else:
        linked_line = False
        str4 = "✕ 선이 연결되야 합니다!"
        c4 = "red"

    if check_y_properly_drawn(0, 4):
        is_there_pixel_head = True
        str1 = "✓ 키가 적당합니다!"
        c1 = "green"
    else:
        is_there_pixel_head = False
        str1 = "✕ 키가 너무 작습니다!"
        c1 = "red"
    if check_x_properly_drawn(8) and check_x_properly_drawn(36):
        is_there_pixel_body = True
        str2 = "✓ 적당한 두께!"
        c2 = "green"
    else:
        is_there_pixel_body = False
        str2 = "✕ 가로로 넓히세요!"
        c2 = "red"

    if check_y_properly_drawn(45, 47):
        is_there_pixel_foot = True
        str3 = "✓ 다리가 충분히 깁니다!"
        c3 = "green"
    else:
        is_there_pixel_foot = False
        str3 = "✕ 다리를 밑에 까지 그려 주세요!"
        c3 = "red"

    # 최종적으로 한 번만 호출
    cheak_text(str1, c1, str2, c2, str3, c3, str4, c4)
    root.after(100, ccc)

ccc()
#클릭 캔버스랑 연결
canvas.bind("<B1-Motion>", drawing_grid)#
canvas.bind("<Button-1>", drawing_grid)


#머리, 몸통, 다리
def grid_part():
    head_part = {'x1': 0, 'y1': 0, 'x2': CANVAS_WIDTH, 'y2': HEAD_HEIGHT}
    body_part = {'x1': 0, 'y1': HEAD_HEIGHT, 'x2': CANVAS_WIDTH, 'y2': HEAD_HEIGHT + BODY_HEIGHT}
    foot_part = {'x1': 0, 'y1': HEAD_HEIGHT + BODY_HEIGHT, 'x2': CANVAS_WIDTH, 'y2': CANVAS_HEIGHT}

    # 각 영역을 시스템에서 나누어서 작업
    return head_part, body_part, foot_part
#팔레트 열기
def choose_color():
    global current_color #전역 사용
    current_color = colorchooser.askcolor(title="팔레트 열기")[1]  # [1]은 헥사코드
    return
def choose_eraser():
    global current_color
    current_color = '#d4d5d6'

def on_fill_mode():
    global fill_mode
    fill_mode = not fill_mode
    if fill_mode:
        fill_button.config(bg="gray")
    else:
        fill_button.config(bg="SystemButtonFace")

def cheaking_reset():
    response = messagebox.askyesno("잠시만요!", "그린것을 모두 초기화합니까?")
    if response:
        entrie_del()

# 버튼 여러 개 넣기 (예: 6개를 2행 3열로)
colors = ["#ffb0b0", "#ff5959", "#ff0000", "#b50000", "#6b0000",
          "#ffc99e", "#ff9947", "#ff7200", "#b55100", "#662e00",
          "#fff7b3", "#fff066", "#ffe600", "#c7b300", "#8c7e00",
          "#b0ffab", "#69ff5e", "#11ff00", "#00a600", "#005e00",
          "#9cf5ff", "#00e5ff", "#0080ff", "#0033ff", "#0c0091",
          "#e4a1ff", "#d261ff", "#b700ff", "#7700a6", "#4f006e",
          "#000000", "#5e5e5e", "#a6a6a6", "#ffffff"]

for i, color in enumerate(colors):
    btn = tk.Button(color_frame, bg=color, width=7, height=2,
                    command=lambda c=color: click_color_button(c))  # 클릭 시 해당 색상 전달
    row = i // 5
    col = i % 5
    btn.grid(row=row, column=col, padx=5, pady=5)


def click_color_button(color):
    global current_color
    current_color = color

button = tk.Button(color_frame, text="지우개", command=choose_eraser, width=7, height=2)
button.grid(row=6, column=4, padx=5, pady=5)
button = tk.Button(color_frame, text="팔레트", command=choose_color, width=7, height=2)
button.grid(row=7, column=0, padx=5, pady=5)
fill_button = tk.Button(color_frame, text="채우기", command=on_fill_mode, width=7, height=2)
fill_button.grid(row=7, column=1, padx=5, pady=5)
button = tk.Button(color_frame, text="초기화", command=cheaking_reset, width=7, height=2)
button.grid(row=7, column=2, padx=5, pady=5)


#나누어진 각 영역 출력
head_part, body_part, foot_part = grid_part()
print(f"Head part: {head_part}")
print(f"Body part: {body_part}")
print(f"Foot part: {foot_part}")




# 그리드 그리기
show_grid()
root.mainloop()