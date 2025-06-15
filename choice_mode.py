import tkinter as tk
from tkinter import messagebox
from game_screen import starting_game
def open_choice_mode(game_data):
    choiceMode = tk.Tk()
    choiceMode.geometry("700x700+0+0")
    choiceMode.resizable(False, False)
    choiceMode.title("뛰라노 - Main Menu")
    choiceMode.configure(bg="#2E7D32")  # 초록색 배경

    def start_nomal_mode():
        messagebox.showinfo("게임 시작!", f"{game_data['p1_name']} vs {game_data['p2_name']}\n게임을 시작합니다!")
        starting_game(game_data, itemMode=False)
        choiceMode.destroy()

    def start_item_mode():
        messagebox.showinfo("게임 시작!", f"{game_data['p1_name']} vs {game_data['p2_name']}\n게임을 시작합니다!")
        starting_game(game_data, itemMode=True)
        choiceMode.destroy()
    # 기본 배틀모드 버튼
    nomal_button = tk.Button(choiceMode,
                             text="기본 배틀모드",
                             font=("HY헤드라인M", 20, "bold"),
                             width=15,
                             height=2,
                             bg="#4CAF50",
                             fg="white",
                             activebackground="#45a049",
                             activeforeground="white",
                             relief="raised",
                             bd=4,
                             command=start_nomal_mode)
    nomal_button.place(relx=0.5, rely=0.4, anchor="center")

    # 아이템전 배틀모드 버튼
    item_button = tk.Button(choiceMode,
                            text="아이템전 배틀모드",
                            font=("HY헤드라인M", 20, "bold"),
                            width=15,
                            height=2,
                            bg="#4CAF50",
                            fg="white",
                            activebackground="#45a049",
                            activeforeground="white",
                            relief="raised",
                            bd=4,
                            command=start_item_mode)
    item_button.place(relx=0.5, rely=0.55, anchor="center")

    choiceMode.mainloop()
