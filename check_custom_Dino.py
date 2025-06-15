import tkinter as tk
from PIL import Image, ImageTk

def show_dino_popup(slot):
    dinoCheckPopup = tk.Toplevel()
    dinoCheckPopup.geometry("400x400")
    dinoCheckPopup.resizable(False, False)
    dinoCheckPopup.title("Draw Image")

    canvasWidth = 310
    canvasHeight = 280

    canvas = tk.Canvas(dinoCheckPopup, width=canvasWidth, height=canvasHeight, bg='light gray', bd=0, highlightthickness=0)
    canvas.pack(padx=20, pady=5)

    checkText = tk.StringVar()
    checkText.set("⭐당신의 공룡은 준비 되었습니다!⭐")
    textLabel = tk.Label(dinoCheckPopup, textvariable=checkText, font=("HY헤드라인M", 15))
    textLabel.place(x=27, y=275)

    def OK():
        dinoCheckPopup.destroy()

    OK_button = tk.Button(dinoCheckPopup, text="완벽해요!", command=OK, width=10, height=1,
                          font=("HY헤드라인M", 15), fg="white", bg="green")
    OK_button.place(x=140, y=330)

    # 배경 이미지
    dino_bg_image = Image.open("./images/checkBG.png").convert("RGBA")
    resized_image = dino_bg_image.resize((canvasWidth, canvasHeight), Image.NEAREST)
    dino_bg_image_tk = ImageTk.PhotoImage(resized_image)
    canvas.create_image(0, 0, image=dino_bg_image_tk, anchor="nw")

    # 사용자 공룡 이미지 — 슬롯 폴더 경로 반영
    custom_dino_path = f"./dino_image/{slot}/custom1.png"
    custom_dino_image = Image.open(custom_dino_path).convert("RGBA")
    resized_image = custom_dino_image.resize((130, 145), Image.NEAREST)
    custom_dino_image_tk = ImageTk.PhotoImage(resized_image)
    canvas.create_image(30, 110, image=custom_dino_image_tk, anchor="nw")

    # 이미지 참조 유지 (중요)
    dinoCheckPopup.bg_image = dino_bg_image_tk
    dinoCheckPopup.custom_image = custom_dino_image_tk


