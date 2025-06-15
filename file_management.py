from PIL import Image, ImageDraw, ImageFilter
import os
import copy
from check_custom_Dino import show_dino_popup
import tkinter as tk
import json

def save_image(grid_colors, slot_folder, block_size=1):
    def draw_image(grid, filename):
        height = len(grid)
        width = len(grid[0])
        original_w = width * block_size
        original_h = height * block_size
        expanded_w = original_w + 2
        expanded_h = original_h + 2

        img = Image.new("RGBA", (original_w, original_h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        for y in range(height):
            for x in range(width):
                color = grid[y][x]
                if color == "empty":
                    continue
                x0 = x * block_size
                y0 = y * block_size
                x1 = x0 + block_size - 1
                y1 = y0 + block_size - 1
                draw.rectangle([x0, y0, x1, y1], fill=color)

        expanded = Image.new("RGBA", (expanded_w, expanded_h), (0, 0, 0, 0))
        expanded.paste(img, (1, 1))
        alpha = expanded.split()[3]
        outline_mask = alpha.filter(ImageFilter.MaxFilter(3))
        outline_mask = Image.eval(outline_mask, lambda px: 255 if px > 0 else 0)
        outline = Image.new("RGBA", expanded.size, (255, 255, 255, 0))
        outline.putalpha(outline_mask)
        final = Image.alpha_composite(outline, expanded)

        # 슬롯 폴더 경로 생성
        full_dir = os.path.join("dino_image", slot_folder)
        if not os.path.exists(full_dir):
            os.makedirs(full_dir)

        save_path = os.path.join(full_dir, filename)
        final.save(save_path)
        print(f"저장 완료: {save_path} (크기: {final.size[0]} x {final.size[1]})")

    # 원본
    draw_image(grid_colors, "custom1.png")

    # 왼발 위로
    moved_grid1 = copy.deepcopy(grid_colors)
    for y in range(41, 45):
        for x in range(0, 24):
            moved_grid1[y - 1][x] = grid_colors[y][x]
    for x in range(0, 24):
        moved_grid1[44][x] = "empty"

    draw_image(moved_grid1, "custom1_1.png")

    # 오른발 위로
    moved_grid2 = copy.deepcopy(grid_colors)
    for y in range(41, 45):
        for x in range(24, 42):
            moved_grid2[y - 1][x] = grid_colors[y][x]
    for x in range(24, 42):
        moved_grid2[44][x] = "empty"

    draw_image(moved_grid2, "custom1_2.png")
    show_dino_popup(slot_folder)

def show_choice_slot(grid_colors):
    popup = tk.Toplevel()
    popup.title("슬롯 선택")
    popup.geometry("300x150")
    popup.resizable(False, False)

    label = tk.Label(popup, text="저장할 슬롯을 선택하세요", font=("HY헤드라인M", 14))
    label.pack(pady=15)

    def slot1_click():
        popup.destroy()
        save_image(grid_colors, "slot1")
        print("슬롯1 선택됨")

    def slot2_click():
        popup.destroy()
        save_image(grid_colors, "slot2")
        print("슬롯2 선택됨")

    btn1 = tk.Button(popup, text="슬롯 1", width=10, height=2, command=slot1_click)
    btn1.pack(side="left", padx=40, pady=20)

    btn2 = tk.Button(popup, text="슬롯 2", width=10, height=2, command=slot2_click)
    btn2.pack(side="right", padx=40, pady=20)

    popup.mainloop()


SETTING_DIR = "./settings"
SETTING_FILE = os.path.join(SETTING_DIR, "settings.txt")

import os
import json

SETTING_DIR = "settings"
SETTING_FILE = os.path.join(SETTING_DIR, "settings.json")

def save_settings(volume, bgm_on, is_dark):
    if not os.path.exists(SETTING_DIR):
        os.makedirs(SETTING_DIR)

    settings = {
        'volume': volume,
        'bgm_on': bgm_on,
        'is_dark': is_dark
    }

    with open(SETTING_FILE, 'w', encoding='utf-8') as f:
        json.dump(settings, f, ensure_ascii=False, indent=4)
    print(f"설정 저장 완료: {SETTING_FILE}")

def load_settings():
    """저장된 설정을 JSON 형식으로 불러와서 딕셔너리로 반환"""
    if not os.path.exists(SETTING_FILE):
        print("설정 파일이 없어 기본값을 불러옵니다.")
        return {
            'volume': 50,
            'bgm_on': True,
            'is_dark': False
        }

    try:
        with open(SETTING_FILE, "r", encoding="utf-8") as f:
            settings = json.load(f)
            return settings
    except Exception as e:
        print(f"설정 파일 읽기 오류: {e}")
        return {
            'volume': 50,
            'bgm_on': True,
            'is_dark': False
        }



