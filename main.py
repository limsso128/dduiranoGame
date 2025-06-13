#메인화면창입니다 (민채)
import tkinter as tk  # GUI 라이브러리

root = tk.Tk()  # 창 생성
root.geometry("1300x700")
root.overrideredirect(False)  # True : 창의 기본 타이틀바 없애기
root.resizable(False, False)
root.title("Main menu")

root.resizable(False, False)  #창 크기 조정 불가

#============================여기 밑에 코드 작성ㄱㄱㄱㄱ
#타이틀
title_label = tk.Label(root, text="뛰라노", font=("Arial", 60), fg="black")
title_label.place(relx=0.5, rely=0.3, anchor="center")

#시작하기 버튼
start_button = tk.Button(root, text="시작하기", font=("Arial",20), width=15, height=2)
start_button.place(relx=0.5, rely=0.4, anchor="center")

#설정 버튼(오른쪽 아래)
settings_button = tk.Button(root, text="설정", font="")
root.mainloop() #이 코드 절대로 지우지 말고 맨밑에두셈