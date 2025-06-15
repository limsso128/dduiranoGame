import tkinter as tk
from tkinter import ttk
import pygame

from file_management import save_settings
from file_management import load_settings


def open_settings():
    settingRoot = tk.Tk()
    settingRoot.geometry("700x350")
    settingRoot.overrideredirect(False)
    settingRoot.resizable(False, False)
    settingRoot.title("Setting")

    # JSON에서 설정값 로드
    SETTING_JSON = load_settings()
    currentVolume = SETTING_JSON["volume"]
    currentBGM = SETTING_JSON["bgm_on"]
    currentDark = SETTING_JSON["is_dark"]

    # 전역 변수로 현재 설정값들 초기화
    bgm_on = currentBGM
    is_dark = currentDark

    # 볼륨 설정 함수
    def set_volume(val):
        volume = float(val) / 100
        # BGM이 재생 중이면 볼륨 즉시 적용
        if bgm_on and pygame.mixer.get_init():
            pygame.mixer.music.set_volume(volume)

    # 볼륨 슬라이더 설정
    tk.Label(settingRoot, text="BGM 볼륨", font=("Arial", 14)).place(x=100, y=50)
    volume_slider = ttk.Scale(settingRoot, from_=0, to=100, orient="horizontal", command=set_volume, length=200)
    volume_slider.set(currentVolume)  # JSON에서 불러온 볼륨값 설정
    volume_slider.place(x=100, y=80)

    # BGM 토글 함수
    def toggle_bgm():
        nonlocal bgm_on
        if bgm_on:
            pygame.mixer.music.stop()
            bgm_button.config(text="BGM 켜기")
        else:
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(volume_slider.get() / 100)
            bgm_button.config(text="BGM 끄기")
        bgm_on = not bgm_on

    # BGM 버튼 생성 (JSON 설정값에 따라 초기 텍스트 설정)
    bgm_button = tk.Button(settingRoot, text="BGM 끄기" if bgm_on else "BGM 켜기",
                           command=toggle_bgm, width=10)
    bgm_button.place(x=320, y=75)

    # 테마 토글 함수
    def toggle_theme():
        nonlocal is_dark
        if is_dark:
            # 라이트 모드로 변경
            settingRoot.config(bg="white")
            # 모든 라벨의 텍스트 색상 변경
            for widget in settingRoot.winfo_children():
                if isinstance(widget, tk.Label):
                    widget.config(bg="white", fg="black")
            theme_button.config(text="다크 모드", bg="SystemButtonFace", fg="black")
        else:
            # 다크 모드로 변경
            settingRoot.config(bg="black")
            # 모든 라벨의 텍스트 색상 변경
            for widget in settingRoot.winfo_children():
                if isinstance(widget, tk.Label):
                    widget.config(bg="black", fg="white")
            theme_button.config(text="화이트 모드", bg="gray20", fg="white")
        is_dark = not is_dark

    # 테마 버튼 생성 (JSON 설정값에 따라 초기 텍스트 설정)
    theme_button = tk.Button(settingRoot, text="화이트 모드" if is_dark else "다크 모드",
                             command=toggle_theme, width=12)
    theme_button.place(x=100, y=150)

    # 초기 테마 적용 (JSON 설정값 기반)
    if is_dark:
        settingRoot.config(bg="black")
        # 라벨 생성 후 다크 모드 스타일 적용
        settingRoot.after(10, lambda: apply_dark_theme())
        theme_button.config(bg="gray20", fg="white")
    else:
        settingRoot.config(bg="white")
        theme_button.config(bg="SystemButtonFace", fg="black")

    def apply_dark_theme():
        """다크 테마 스타일을 모든 라벨에 적용"""
        for widget in settingRoot.winfo_children():
            if isinstance(widget, tk.Label):
                widget.config(bg="black", fg="white")

    # 저장 버튼 함수
    def save_button():
        volume = volume_slider.get()
        save_settings(volume, bgm_on, is_dark)
        # 저장 완료 피드백 (선택사항)
        confirm_button.config(text="저장완료!")
        settingRoot.after(1000, lambda: confirm_button.config(text="확인"))

    # 확인 버튼
    confirm_button = tk.Button(settingRoot, text="확인", command=save_button,
                               width=10, bg="green", fg="white")
    confirm_button.place(x=320, y=150)

    # 창 닫기 함수
    def close_setting():
        settingRoot.destroy()

    # 나가기 버튼
    exit_button = tk.Button(settingRoot, text="나가기", command=close_setting,
                            width=10, bg="red", fg="white")
    exit_button.place(x=550, y=290)

    # 초기 BGM 상태 적용 (JSON 설정값 기반)
    if bgm_on and pygame.mixer.get_init():
        pygame.mixer.music.set_volume(currentVolume / 100)
        # BGM이 이미 재생 중이 아니라면 재생 시작
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play(-1)

    settingRoot.mainloop()