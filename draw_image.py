# 공룡 커스텀 그리는 창 (지연)
import tkinter as tk  # GUI 라이브러리
from tkinter import messagebox  # 확인창
from tkinter import colorchooser  # 그 뭐냐 컬러 팔레트래
from PIL import Image, ImageTk
import subprocess
import sys
import time

from file_management import show_choice_slot


def show_drawing_screen():
    is_there_pixel_head = False
    is_there_pixel_body = False
    is_there_pixel_foot = False
    linked_line = False

    window = tk.Toplevel()  # 새 창 생성 (메인 window 위에 뜨는 서브 창)
    window.geometry("1100x765+0+0")
    window.overrideredirect(False)
    window.title("Draw Image")
    window.resizable(False, False)

    # 44*47인데 흰 외곽선 고려해서
    CANVAS_WIDTH = 42
    CANVAS_HEIGHT = 45
    PIXEL_SIZE = 15

    grid_colors = [["empty" for _ in range(CANVAS_WIDTH)] for _ in range(CANVAS_HEIGHT)]
    draw_log = []  # 선 저장 (x, y, 색) -> 이제 액션 단위로 저장
    # 수정: 현재 드래그 세션에서 변경된 픽셀들을 임시 저장
    current_action_log = []  # 현재 클릭/드래그 액션에서 변경된 픽셀들
    is_dragging = False  # 드래그 상태 추적

    start_drag = False
    end_drag = False

    fill_mode = False  # 채우기
    isOnEraser = False
    isOnGuide = True

    current_color = 'black'  # 현재 색상

    perfect = False
    # 기본 공룡 이미지 가져오기
    nomal_dino_image = Image.open("./images/image_guide_dino.png").convert("RGBA")
    scale = 2
    resized_image = nomal_dino_image.resize(
        (42 * PIXEL_SIZE, 45 * PIXEL_SIZE),
        Image.NEAREST
    )
    nomal_dino_image = ImageTk.PhotoImage(resized_image)
    # ============================================프레임==============================================

    # 오른쪽 프레임 (캔버스)
    right_frame = tk.Frame(window, bg='#d4be00', width=(CANVAS_WIDTH + 2) * PIXEL_SIZE)
    right_frame.grid(row=1, column=1)
    right_frame.grid_propagate(False)

    # 위 프레임
    top_frame = tk.Frame(window, height=40, bg="#fff86e")
    top_frame.grid(row=0, column=0, columnspan=2, sticky="ew")  # es -> 양옆으로, ns -> 위아래로

    # 아래 프레임
    bottom_frame = tk.Frame(window, height=40, bg="#fff86e")
    bottom_frame.grid(row=2, column=0, columnspan=2, sticky="ew")

    # 왼 프레임
    left_frame = tk.Frame(window, width=400, bg="#fff86e")
    left_frame.grid(row=1, column=0, sticky="ns")
    left_frame.grid_propagate(False)  # 크기 고정

    # 가이드 프레임
    guide_frame = tk.Frame(left_frame, bg="white", width=340, height=250)
    guide_frame.place(x=30)
    guide_frame.pack_propagate(False)

    # 툴 프레임
    color_frame = tk.Frame(left_frame, bg="white", width=340, height=400)
    color_frame.place(x=30, y=275)
    color_frame.pack_propagate(False)

    text1 = tk.StringVar()
    text2 = tk.StringVar()
    text3 = tk.StringVar()
    text4 = tk.StringVar()
    text5 = tk.StringVar()

    # 캔버스 (중앙 프레임 안에)
    canvas = tk.Canvas(right_frame, width=CANVAS_WIDTH * PIXEL_SIZE, height=(CANVAS_HEIGHT) * PIXEL_SIZE,
                       bg='light gray', bd=0, highlightthickness=0)
    canvas.pack(padx=20, pady=5)

    canvas.image = nomal_dino_image
    text5.set("⭐가이드에 맞춰 그리세요!")
    label1 = tk.Label(guide_frame, textvariable=text1, font=("HY헤드라인M", 15), fg="red", bg="white")
    label1.place(x=16, y=15)
    label2 = tk.Label(guide_frame, textvariable=text2, font=("HY헤드라인M", 15), fg="red", bg="white")
    label2.place(x=16, y=65)
    label3 = tk.Label(guide_frame, textvariable=text3, font=("HY헤드라인M", 15), fg="red", bg="white")
    label3.place(x=16, y=115)
    label4 = tk.Label(guide_frame, textvariable=text4, font=("HY헤드라인M", 15), fg="red", bg="white")
    label4.place(x=16, y=165)
    label5 = tk.Label(guide_frame, textvariable=text5, font=("HY헤드라인M", 15), fg="black", bg="white")
    label5.place(x=14, y=210)

    # 가이드 텍스트
    def check_text(str1, c1, str2, c2, str3, c3, str4, c4):
        text1.set(str1)
        label1.config(fg=c1)
        text2.set(str2)
        label2.config(fg=c2)
        text3.set(str3)
        label3.config(fg=c3)
        text4.set(str4)
        label4.config(fg=c4)

    image_id = canvas.create_image(0, 0, image=nomal_dino_image, anchor="nw")

    window.grid_columnconfigure(0, weight=0)  # 왼쪽 프레임
    window.grid_columnconfigure(1, weight=1)  # 캔버스

    # ========================================UI============================================================
    def exiting():
        subprocess.Popen([sys.executable, "main.py"])
        time.sleep(0.5)
        window.destroy()

    exit_button = tk.Button(window, text="EXIT", command=exiting, width=5, height=1, font=("HY헤드라인M", 13), fg="white",
                            bg="red")
    exit_button.place(x=1040, y=5)

    # ========================================화면===========================================================

    # 그리드 생성
    def show_grid():
        for i in range(CANVAS_WIDTH):
            for j in range(CANVAS_HEIGHT):
                canvas.create_rectangle(i * PIXEL_SIZE, j * PIXEL_SIZE,
                                        (i + 1) * PIXEL_SIZE, (j + 1) * PIXEL_SIZE,
                                        outline='', fill='#d4d5d6')

    #마우스 버튼이 눌렸을 때
    def start_drawing(event):
        nonlocal is_dragging, current_action_log
        is_dragging = True
        current_action_log = []  # 새로운 액션 시작
        drawing_grid(event)  # 첫 번째 픽셀 그리기

    #마우스 버튼이 떼어졌을 때
    def end_drawing(event):
        nonlocal is_dragging, current_action_log, draw_log
        if is_dragging and current_action_log:
            # 현재 액션의 모든 변경사항을 draw_log에 추가
            draw_log.append(current_action_log.copy())
            current_action_log = []
        is_dragging = False

    # 그림 그리기(클릭, 드래그) - 수정됨
    def drawing_grid(event):
        nonlocal current_color, fill_mode, current_action_log  # nonlocal 사용
        x = event.x // PIXEL_SIZE
        y = event.y // PIXEL_SIZE

        if not (0 <= x < CANVAS_WIDTH and 0 <= y < CANVAS_HEIGHT):  # 캔버스 밖에 시도하면 끝
            return

        if fill_mode:  # 색 채우기 flood fill호출
            target_color = grid_colors[y][x]
            if current_color != '#d4d5d6':  # 현재 지우개가 선택되지 않았으면
                if target_color != current_color:
                    flood_fill(x, y, target_color, current_color, "draw")
            else:  # 현재 지우개면
                checking_cantFill_box()
        else:
            if current_color == '#d4d5d6':  # 지우개
                # 수정: f grid_colors[y][x] != "empty" and not any(log[0] == x and log[1] == y for log in current_action_log):
                    current_action_log.append((x, y, grid_colors[y][x]))

                grid_colors[y][x] = "empty"
                # 그린 도형만 delete
                overlapping = canvas.find_overlapping(
                    x * PIXEL_SIZE, y * PIXEL_SIZE,
                    (x + 1) * PIXEL_SIZE, (y + 1) * PIXEL_SIZE
                )
                for item in overlapping:
                    if "draw" in canvas.gettags(item):
                        canvas.delete(item)
                grid_colors[y][x] = "empty"
            # 기본 그리기 모드
            else:
                #색상이 다를 때만 로그에 추가
                if grid_colors[y][x] != current_color and not any(
                        log[0] == x and log[1] == y for log in current_action_log):
                    current_action_log.append((x, y, grid_colors[y][x]))  # 변경 전 색상 저장

                grid_colors[y][x] = current_color
                canvas.create_rectangle(
                    x * PIXEL_SIZE, y * PIXEL_SIZE,
                    (x + 1) * PIXEL_SIZE, (y + 1) * PIXEL_SIZE,
                    fill=current_color, outline="",
                    tags="draw"
                )

    # 선 연결 확인
    def check_linked_line(start_y, end_y):
        for y in range(start_y, end_y):
            has_pixel = False
            for x in range(CANVAS_WIDTH):
                if grid_colors[y][x] != "empty":
                    has_pixel = True
                    break  # 픽셀이 있으면 멈춤
            if not has_pixel:
                return False  # 한 행이라도 비어 있으면 False
        return True  # 모든 행에 픽셀이 있음

    # 모두삭제
    def entrie_del():
        for y in range(CANVAS_HEIGHT):
            for x in range(CANVAS_WIDTH):
                grid_colors[y][x] = "empty"
                canvas.create_rectangle(
                    x * PIXEL_SIZE, y * PIXEL_SIZE,
                    (x + 1) * PIXEL_SIZE, (y + 1) * PIXEL_SIZE,
                    fill='#d4d5d6', outline=""
                )
        canvas.tag_raise(image_id)

    # 수정: Undo 함수 - 액션 단위로 되돌리기
    def undo():
        nonlocal draw_log
        if not draw_log:
            return

        # 마지막 액션의 모든 변경사항을 되돌리기
        last_action = draw_log.pop()
        for x, y, old_color in reversed(last_action):  # 역순으로 되돌리기
            grid_colors[y][x] = old_color
            # 기존 드로우 제거
            overlapping = canvas.find_overlapping(
                x * PIXEL_SIZE, y * PIXEL_SIZE,
                (x + 1) * PIXEL_SIZE, (y + 1) * PIXEL_SIZE
            )
            for item in overlapping:
                if "draw" in canvas.gettags(item):
                    canvas.delete(item)

            # 이전 색상으로 복원 (empty가 아닌 경우)
            if old_color != "empty":
                canvas.create_rectangle(
                    x * PIXEL_SIZE, y * PIXEL_SIZE,
                    (x + 1) * PIXEL_SIZE, (y + 1) * PIXEL_SIZE,
                    fill=old_color, outline="",
                    tags="draw"
                )

    window.bind("<Control-z>", lambda event: undo())

    #채우기
    def flood_fill(x, y, target_color, replacement_color, tags):
        nonlocal current_action_log
        if target_color == replacement_color:
            return

        stack = [(x, y)]
        drawn_points = set()
        fill_action_log = []  # 채우기 액션을 위한 별도 로그

        while stack:
            cx, cy = stack.pop()
            if not (0 <= cx < CANVAS_WIDTH and 0 <= cy < CANVAS_HEIGHT):
                continue
            if grid_colors[cy][cx] != target_color:
                continue

            if (cx, cy) not in drawn_points:
                fill_action_log.append((cx, cy, grid_colors[cy][cx]))  # 수정: fill_action_log에 추가
                drawn_points.add((cx, cy))

            grid_colors[cy][cx] = replacement_color
            canvas.create_rectangle(
                cx * PIXEL_SIZE, cy * PIXEL_SIZE,
                (cx + 1) * PIXEL_SIZE, (cy + 1) * PIXEL_SIZE,
                fill=replacement_color, outline="",
                tags="draw"
            )

            stack.extend([
                (cx + 1, cy), (cx - 1, cy),
                (cx, cy + 1), (cx, cy - 1)
            ])

        #채우기 액션을 draw_log에 즉시 추가
        if fill_action_log:
            draw_log.append(fill_action_log)

    # 행에 픽셀이 그려져 있는지 확인
    def check_y_properly_drawn(start_y, end_y):
        for y in range(start_y, end_y):
            for x in range(CANVAS_WIDTH):
                if grid_colors[y][x] != "empty":
                    return True
        return False

    def check_x_properly_drawn(x):
        for y in range(CANVAS_HEIGHT):
            if grid_colors[y][x] != "empty":
                return True
        return False

    # 수정: 이벤트 바인딩 변경 - 마우스 버튼 누름/뗌을 별도로 처리
    canvas.bind("<Button-1>", start_drawing)  # 마우스 버튼 누를 때
    canvas.bind("<B1-Motion>", drawing_grid)  # 드래그할 때
    canvas.bind("<ButtonRelease-1>", end_drawing)  # 마우스 버튼 뗄 때

    def save_and_show():
        show_choice_slot(grid_colors)

    save_button = tk.Button(window, text="저장!", command=save_and_show, width=5, height=1, font=("HY헤드라인M", 15),
                            fg="green")

    # 적절한 그림 조절 루프
    def step1():
        nonlocal is_there_pixel_head, is_there_pixel_body, is_there_pixel_foot, linked_line  # nonlocal 사용

        if (is_there_pixel_head and is_there_pixel_body and is_there_pixel_foot and linked_line):
            save_button.place(x=292, y=52)  # 화면에 띄우기 forget()
        else:
            save_button.place_forget()

        if check_linked_line(5, 43):
            linked_line = True
            str4 = "✓ 선이 잘 연결되어 있습니다!"
            c4 = "green"
        else:
            linked_line = False
            str4 = "✕ 선이 연결되어야 합니다!"
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

        if check_y_properly_drawn(43, 45):
            is_there_pixel_foot = True
            str3 = "✓ 다리가 충분히 깁니다!"
            c3 = "green"
        else:
            is_there_pixel_foot = False
            str3 = "✕ 다리를 밑에 까지 그려 주세요!"
            c3 = "red"

        # 최종적으로 한 번만 호출
        check_text(str1, c1, str2, c2, str3, c3, str4, c4)
        window.after(80, step1)

    # 팔레트 열기
    def choose_color():
        nonlocal current_color  # nonlocal 사용
        color_result = colorchooser.askcolor(title="팔레트 열기")
        if color_result[1]:  # 색상이 선택되었을 때만
            current_color = color_result[1]  # [1]은 헥사코드
        return

    def choose_eraser():
        nonlocal current_color
        current_color = '#d4d5d6'

    def on_fill_mode():
        nonlocal fill_mode
        fill_mode = not fill_mode
        if fill_mode:
            fill_button.config(bg="gray")
        else:
            fill_button.config(bg="SystemButtonFace")

    def on_guide():
        nonlocal isOnGuide
        isOnGuide = not isOnGuide
        if isOnGuide:
            guide_button.config(bg="gray")
            canvas.itemconfigure(image_id, state='normal')
        else:
            guide_button.config(bg="SystemButtonFace")
            canvas.itemconfigure(image_id, state='hidden')

    def checking_reset_box():
        response = messagebox.askyesno("잠시만요!", "그린것을 모두 초기화합니까?")
        if response:
            entrie_del()

    def checking_cantFill_box():
        messagebox.showinfo("잠시만요!", "지우개는 채울 수 없어요")  # showinfo로 변경


    # 버튼 여러 개 넣기 (예: 6개를 2행 3열로)
    colors = ["#ffb0b0", "#ff5959", "#ff0000", "#b50000", "#6b0000",
              "#ffc99e", "#ff9947", "#ff7200", "#b55100", "#662e00",
              "#fff7b3", "#fff066", "#ffe600", "#c7b300", "#8c7e00",
              "#b0ffab", "#69ff5e", "#11ff00", "#00a600", "#005e00",
              "#9cf5ff", "#00e5ff", "#0080ff", "#0033ff", "#0c0091",
              "#e4a1ff", "#d261ff", "#b700ff", "#7700a6", "#4f006e",
              "#000000", "#5e5e5e", "#a6a6a6", "#ffffff"]

    def click_color_button(color):
        nonlocal current_color
        current_color = color

    for i, color in enumerate(colors):
        btn = tk.Button(color_frame, bg=color, width=7, height=2,
                        command=lambda c=color: click_color_button(c))  # 클릭 시 해당 색상 전달
        row = i // 5
        col = i % 5
        btn.grid(row=row, column=col, padx=5, pady=5)

    eraser_button = tk.Button(color_frame, text="지우개", command=choose_eraser, width=7, height=2)
    eraser_button.grid(row=6, column=4, padx=5, pady=5)

    button = tk.Button(color_frame, text="팔레트", command=choose_color, width=7, height=2)
    button.grid(row=7, column=0, padx=5, pady=5)

    fill_button = tk.Button(color_frame, text="채우기", command=on_fill_mode, width=7, height=2)
    fill_button.grid(row=7, column=1, padx=5, pady=5)

    button = tk.Button(color_frame, text="초기화", command=checking_reset_box, width=7, height=2)
    button.grid(row=7, column=2, padx=5, pady=5)

    guide_button = tk.Button(color_frame, text="가이드", command=on_guide, width=7, height=2, bg="gray")
    guide_button.grid(row=7, column=3, padx=5, pady=5)

    show_grid()  # 그리드 그리기
    canvas.tag_raise(image_id)  # 가이드 이미지
    step1()  # step1 함수 호출 추가

    return window