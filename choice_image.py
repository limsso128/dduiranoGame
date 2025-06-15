import tkinter as tk
from PIL import Image, ImageTk
import os

from choice_mode import open_choice_mode
def show_player_select():
    window = tk.Toplevel()
    window.geometry("800x600")
    window.resizable(False, False)
    window.title("뛰라노 - Player Select")
    window.configure(bg="green")


    # 현재 선택된 공룡 슬롯 (기본값: 각각 슬롯1의 첫 번째 공룡)
    current_p1_slot = 1
    current_p1_dino = 1
    current_p2_slot = 1
    current_p2_dino = 1

    # 공룡 이미지를 표시할 라벨들
    p1_dino_display = None
    p2_dino_display = None

    def load_dino_image(slot, dino_num):
        """슬롯과 공룡 번호에 따른 이미지 로드"""
        try:
            # 슬롯 3의 경우 특별 경로 사용
            if slot == 3:
                image_path = "./image/뛰라노_공룡(기본).png"
            else:
                image_path = f"./dino_image/slot{slot}/custom{dino_num}.png"

            if os.path.exists(image_path):
                # 이미지 로드 및 리사이즈
                img = Image.open(image_path).convert("RGBA")
                img = img.resize((200, 200), Image.NEAREST)  # 픽셀아트이므로 NEAREST 사용
                return ImageTk.PhotoImage(img)
            else:
                # 기본 공룡 이미지 로드 (없을 경우)
                default_path = "./images/뛰라노_공룡(기본).png"
                if os.path.exists(default_path):
                    img = Image.open(default_path).convert("RGBA")
                    img = img.resize((200, 200), Image.NEAREST)
                    return ImageTk.PhotoImage(img)
                return None
        except Exception as e:
            print(f"이미지 로드 오류: {e}")
            return None

    def update_p1_display():
        """플레이어 1 공룡 디스플레이 업데이트"""
        nonlocal p1_dino_display
        img = load_dino_image(current_p1_slot, current_p1_dino)
        if img and p1_dino_display:
            p1_dino_display.configure(image=img)
            p1_dino_display.image = img  # 참조 유지

    def update_p2_display():
        """플레이어 2 공룡 디스플레이 업데이트"""
        nonlocal p2_dino_display
        img = load_dino_image(current_p2_slot, current_p2_dino)
        if img and p2_dino_display:
            p2_dino_display.configure(image=img)
            p2_dino_display.image = img  # 참조 유지

    def select_p1_dino():
        """플레이어 1 공룡 선택 (순환)"""
        nonlocal current_p1_slot, current_p1_dino

        # 슬롯 3인 경우 특별 처리 (단일 이미지)
        if current_p1_slot == 3:
            current_p1_slot = 1
            current_p1_dino = 1
        # 다음 공룡으로 순환
        elif os.path.exists(f"./dino_image/slot{current_p1_slot}/custom{current_p1_dino + 1}.png"):
            current_p1_dino += 1
        elif current_p1_slot == 1 and os.path.exists(f"./dino_image/slot2/custom1.png"):
            current_p1_slot = 2
            current_p1_dino = 1
        elif current_p1_slot == 2:
            current_p1_slot = 3
            current_p1_dino = 1
        else:
            # 처음으로 돌아가기
            current_p1_slot = 1
            current_p1_dino = 1

        update_p1_display()

    def select_p2_dino():
        """플레이어 2 공룡 선택 (순환)"""
        nonlocal current_p2_slot, current_p2_dino

        # 슬롯 3인 경우 특별 처리 (단일 이미지)
        if current_p2_slot == 3:
            current_p2_slot = 1
            current_p2_dino = 1
        # 다음 공룡으로 순환
        elif os.path.exists(f"./dino_image/slot{current_p2_slot}/custom{current_p2_dino + 1}.png"):
            current_p2_dino += 1
        elif current_p2_slot == 1 and os.path.exists(f"./dino_image/slot2/custom1.png"):
            current_p2_slot = 2
            current_p2_dino = 1
        elif current_p2_slot == 2:
            current_p2_slot = 3
            current_p2_dino = 1
        else:
            # 처음으로 돌아가기
            current_p2_slot = 1
            current_p2_dino = 1

        update_p2_display()

    def start_game():
        """게임 시작"""
        p1_name = p1_name_entry.get().strip()
        p2_name = p2_name_entry.get().strip()

        if not p1_name:
            p1_name = "이름1"
        if not p2_name:
            p2_name = "이름2"

        # 게임 시작 로직 (이름과 슬롯 경로만 전달)
        game_data = {
            'p1_name': p1_name,
            'p2_name': p2_name,
            'p1_slot_path': f"./dino_image/slot{current_p1_slot}" if current_p1_slot != 3 else "./image",
            'p2_slot_path': f"./dino_image/slot{current_p2_slot}" if current_p2_slot != 3 else "./image"
        }

        window.destroy()
        open_choice_mode(game_data)


    def go_back():
        window.destroy()

    # ===== 상단 타이틀 =====
    title_label = tk.Label(window, text="플레이어 선택", font=("HY헤드라인M", 24), bg="green", fg="white")
    title_label.pack(pady=20)

    # ===== 플레이어 프레임 =====
    player_frame = tk.Frame(window, bg="#2E7D32")
    player_frame.pack(pady=30)

    # -------- 플레이어 1 --------
    p1_frame = tk.Frame(player_frame, bg="#2E7D32")
    p1_frame.pack(side="left", padx=60)

    p1_label = tk.Label(p1_frame, text="player1", font=("HY헤드라인M", 16), bg="#2E7D32", fg="white")
    p1_label.pack(pady=10)

    p1_name_entry = tk.Entry(p1_frame, font=("Arial", 14), width=15)
    p1_name_entry.pack(pady=5)
    p1_name_entry.insert(0, "name1")  # 기본 이름

    p1_dino_button = tk.Button(p1_frame, text="공룡 선택", font=("Arial", 12), bg="#81C784", fg="white", width=15,
                               command=select_p1_dino)
    p1_dino_button.pack(pady=5)

    # 공룡 이미지 표시
    p1_dino_display = tk.Label(p1_frame, bg="#2E7D32", width=200, height=200)
    p1_dino_display.pack(pady=5)

    # -------- 플레이어 2 --------
    p2_frame = tk.Frame(player_frame, bg="#2E7D32")
    p2_frame.pack(side="right", padx=60)

    p2_label = tk.Label(p2_frame, text="player2", font=("HY헤드라인M", 16), bg="#2E7D32", fg="white")
    p2_label.pack(pady=10)

    p2_name_entry = tk.Entry(p2_frame, font=("Arial", 14), width=15)
    p2_name_entry.pack(pady=5)
    p2_name_entry.insert(0, "name2")  # 기본 이름

    p2_dino_button = tk.Button(p2_frame, text="공룡 선택", font=("Arial", 12), bg="#81C784", fg="white", width=15,
                               command=select_p2_dino)
    p2_dino_button.pack(pady=5)

    # 공룡 이미지 표시
    p2_dino_display = tk.Label(p2_frame, bg="#2E7D32", width=200, height=200)
    p2_dino_display.pack(pady=5)

    # ===== 하단 버튼들 =====
    button_frame = tk.Frame(window, bg="green")
    button_frame.pack(side="bottom", pady=30)

    back_button = tk.Button(button_frame, text="돌아가기", font=("HY헤드라인M", 16), bg="blue", fg="white", width=15,
                            height=2, command=go_back)
    back_button.pack(side="left", padx=20)

    start_button = tk.Button(button_frame, text="게임 시작!", font=("HY헤드라인M", 16), bg="blue", fg="white", width=15,
                             height=2, command=start_game)
    start_button.pack(side="right", padx=20)

    # 초기 공룡 이미지 로드
    update_p1_display()
    update_p2_display()

    return window


# 테스트용 - 실제로는 다른 파일에서 import해서 사용
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # 메인 윈도우 숨기기
    show_player_select()
    root.mainloop()