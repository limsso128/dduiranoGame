#메인화면창입니다 (민채)
import tkinter as tk  # GUI 라이브러리

root = tk.Tk()  # 창 생성
root.geometry("1300x700")
root.overrideredirect(False)  # True : 창의 기본 타이틀바 없애기
root.resizable(False, False)
root.title("Main menu")

root.resizable(False, False)  #창 크기 조정 불가

#============================여기 밑에 코드 작성ㄱㄱㄱㄱ


root.mainloop() #이 코드 절대로 지우지 말고 맨밑에두셈