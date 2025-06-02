#설정창입니다(시작 화면에서 설정 버튼 누르면 나오는 창, 민채)
import tkinter as tk  # GUI 라이브러리

root = tk.Tk()  # 창 생성
root.geometry("1300x700")
root.overrideredirect(False)  # True : 창의 기본 타이틀바 없애기
root.resizable(False, False)
root.title("Setting")

root.resizable(False, False)  #창 크기 조정 불가

#============================여기 밑에 코드 작성ㄱㄱㄱㄱ


#필요한것.
#음량 조절(BGM on off)
#화이트 모드/ 다크모드 설정
#나가기
#키 변경(아직 게임이 안 만들어져서 버튼만 둬도 됨)


root.mainloop() #이 코드 절대로 지우지 말고 맨밑에두셈