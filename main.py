#메인화면창입니다 (민채)
import tkinter as tk
from PIL import Image, ImageTk

def show_main_screen():
    from file_management import load_settings
    from draw_image import show_drawing_screen
    from choice_image import show_player_select
    from setting import open_settings

    # 메인 윈도우 만들기
    root = tk.Tk()
    root.geometry("1300x700+0+0")
    root.resizable(False, False)
    root.title("뛰라노 - Main Menu")

    try:
        # 이미지 파일 열기 (JPG, PNG, GIF 등 지원)
        image = Image.open("./images/background.png")  # 또는 .png, .gif 등

        # 윈도우 크기에 맞게 이미지 크기 조정
        image = image.resize((1300, 700), Image.Resampling.LANCZOS)

        # Tkinter에서 사용할 수 있는 형태로 변환
        bg_image = ImageTk.PhotoImage(image)

        # Canvas를 사용해서 배경이미지 설정
        canvas = tk.Canvas(root, width=800, height=600)
        canvas.pack(fill="both", expand=True)
        canvas.create_image(0, 0, image=bg_image, anchor="nw")

        # 이미지 참조 유지 (중요!)
        canvas.image = bg_image

    except FileNotFoundError:
        tk.Label(root, text="background.png 파일을 찾을 수 없습니다").pack()
    except Exception as e:
        tk.Label(root, text=f"오류: {str(e)}").pack()

    def open_custom_screen():
        show_drawing_screen()  # 직접 함수 호출로 새 창 열기

    def open_choice_screen():
        show_player_select()

    def show_setting():
        open_settings()
    #============================여기 밑에 코드 작성ㄱㄱㄱㄱ

    # 타이틀 (큰 글씨, 테두리 효과)
    title_main = tk.Label(root, text="뛰라노", font=("HY헤드라인M", 60),
                         fg="white", bg="#2E7D32")  # 메인 텍스트
    title_main.place(relx=0.5, rely=0.3, anchor="center")

    # 시작하기 버튼
    start_button = tk.Button(root,
                            text="▶ 시작하기",
                            font=("HY헤드라인M", 20, "bold"),
                            width=12,
                            height=2,
                            bg="#4CAF50",      # 초록색
                            fg="white",        # 흰 글씨
                            activebackground="#45a049",  # 클릭했을 때 색
                            activeforeground="white",
                            relief="raised",   # 입체감
                            bd=4,
                            command=open_choice_screen)             # 테두리 두께
    start_button.place(relx=0.5, rely=0.45, anchor="center")

    # 커스터마이징 버튼
    customize_button = tk.Button(root,
                                text="🛠 커스터마이징",
                                font=("HY헤드라인M", 18, "bold"),
                                width=14,
                                height=2,
                                bg="#2196F3",      # 파란색
                                fg="white",
                                activebackground="#1976D2",
                                activeforeground="white",
                                relief="raised",
                                bd=4,
                                command=open_custom_screen)  # 커스터마이징 함수 연결
    customize_button.place(relx=0.5, rely=0.6, anchor="center")

    # 설정 버튼 (기어 모양 문자 사용)
    settings_button = tk.Button(root,
                               text="⚙ 설정",
                               font=("HY헤드라인M", 14, "bold"),
                               width=8,
                               height=1,
                               bg="#757575",     # 회색
                               fg="white",       # 흰 글씨
                               activebackground="#616161",  # 클릭했을 때 색
                               activeforeground="white",
                               relief="raised",  # 입체감
                               bd=3,            # 테두리 두께
                               command=show_setting)
    settings_button.place(relx=0.95, rely=0.9, anchor="center")

    # 버튼 호버 효과 (마우스 올렸을 때 색 바뀜)
    def on_start_hover(event):
        start_button.config(bg="#45a049")

    def on_start_leave(event):
        start_button.config(bg="#4CAF50")

    def on_settings_hover(event):
        settings_button.config(bg="#616161")

    def on_settings_leave(event):
        settings_button.config(bg="#757575")

    # 호버 효과 연결
    start_button.bind("<Enter>", on_start_hover)      # 마우스 올렸을 때
    start_button.bind("<Leave>", on_start_leave)      # 마우스 뗐을 때

    settings_button.bind("<Enter>", on_settings_hover)
    settings_button.bind("<Leave>", on_settings_leave)

    root.mainloop() #이 코드 절대로 지우지 말고 맨밑에두셈

if __name__ == "__main__":
    show_main_screen()