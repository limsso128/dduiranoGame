#설정창입니다(시작 화면에서 설정 버튼 누르면 나오는 창, 민채)
import tkinter as tk  # GUI 라이브러리
from tkinter import ttk
import pygame

# =========== 사운드 초기화 =============
pygame.mixer.init()
pygame.mixer.music.load("--BGM 파일 경로--")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.5)

root = tk.Tk()  # 창 생성
root.geometry("1300x700")
root.overrideredirect(False)  # True : 창의 기본 타이틀바 없애기
root.resizable(False, False)
root.title("Setting")

root.resizable(False, False)  #창 크기 조정 불가

#============================여기 밑에 코드 작성ㄱㄱㄱㄱ


#필요한것.

#음량 조절(BGM on off)
#=============== BGM 볼륨 조절 ==========================
def set_volume(val):
    volume = float(val) / 100
    pygame.mixer.music.set_vloume(volume)
tk.Label(root, text="BGM 볼륨", font=("Arial", 14)).place(x=100, y=50)
volume_slider = ttk.Scale(root, from_=0, to=100, orient="horixontal", command=set_volume, length=200)
volume_slider.set(50)
volume_slider.place(x=100, y=80)
#BGM on/off 버튼
bgm_on = True
def toggle_bgm():
    global bgm_on
    if bgm_on:
        pygame.mixer.music.pause()
        bgm_button.config(text="BGM 켜기")
    else:
        pygame.mixer.music.unpause()
        bgm_button.config(text="BGM 끄기")
    bgm_on = not bgm_on
bgm_button = tk.Button(root, text="BFM 끄기", command=toggle_bgm, width=10)
bgm_button.place(x=320, y=75)

#화이트 모드/ 다크모드 설정
# =========================== 다크모드/화이트모드 ===================
is_dark = False
def toggle_theme():
    global is_dark
    if is_dark:
        root.config(bg="white")
        theme_button.config(text="다크 모드")
    else:
        root.config(bg="black")
        theme_button.config(test="화이트 모드")
    is_dark = not is_dark
theme_button = tk.Button(root, text="다크 모드", command=toggle_theme, width=12)
theme_button.place(x=100, y=150)

#나가기
#========================= 나가기 버튼 ============================
def close_setting():
    root.destroy()
exit_button = tk.Button(root, text="나가기", command=close_setting, width=10, bg="red", fg="white")
exit_button.place(x=1100, y=600)

#키 변경(아직 게임이 안 만들어져서 버튼만 둬도 됨)
#=============== 키 설정 버튼(임심) ======================
tk.Label(root, text="키 설정", font=("Arial", 14)).place(x=100, y=220)
key_setting_button = tk.Button(root, text="키 변경", width=20)
key_setting_button.place(s=100, y=250)


root.mainloop() #이 코드 절대로 지우지 말고 맨밑에두셈