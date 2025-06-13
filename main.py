#메인화면창입니다 (민채) - 쉬운 픽셀 스타일
import tkinter as tk
import subprocess

def open_setting():
    subprocess.Popen(["python", "setting.py"])

# 메인 윈도우 만들기
root = tk.Tk()
root.geometry("1300x700")
root.resizable(False, False)
root.title("뛰라노 - Main Menu")
root.configure(bg="#2E7D32")  # 초록색 배경

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
                        bd=4)             # 테두리 두께
start_button.place(relx=0.5, rely=0.45, anchor="center")

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
                           command=open_setting)
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