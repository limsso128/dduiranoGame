#공룡 그림 확인창 (없어도 되는데 퀄리티 업을 위해 존재 (지연))
import tkinter as tk
from PIL import Image, ImageTk, ImageOps

def show_dino_popup():
    dinoCheckPopup = tk.Toplevel()  # ✅ 반드시 Toplevel 사용
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
    dino_bg_image = ImageTk.PhotoImage(resized_image)
    canvas.create_image(0, 0, image=dino_bg_image, anchor="nw")

    # 사용자 공룡 이미지
    custom_dino_image = Image.open("./dino_image/custom1.png").convert("RGBA")
    resized_image = custom_dino_image.resize((130, 145), Image.NEAREST)
    mirrored_image = ImageOps.mirror(resized_image)
    custom_dino_image = ImageTk.PhotoImage(mirrored_image)
    canvas.create_image(30, 110, image=custom_dino_image, anchor="nw")

    # 이미지가 사라지지 않도록 참조 유지
    canvas.image1 = dino_bg_image
    canvas.image2 = custom_dino_image

