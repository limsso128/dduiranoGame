from PIL import Image, ImageDraw, ImageFilter
import os
import copy
from check_custom_Dino import show_dino_popup

def save_image(grid_colors, block_size=1):
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

        if not os.path.exists("dino_image"):
            os.makedirs("dino_image")
        if not os.path.exists("current_image"):
            os.makedirs("current_image")
        final.save(f"dino_image/{filename}")
        print(f"저장 완료: dino_image/{filename} (크기: {final.size[0]} x {final.size[1]})")

    #원본
    draw_image(grid_colors, "custom1.png")

    #왼발 위로
    moved_grid1 = copy.deepcopy(grid_colors)
    for y in range(41, 45): #3칸을 한칸 위로
        for x in range(0, 18): #가로 0~18
            moved_grid1[y - 1][x] = grid_colors[y][x]
    #아래 공백
    for x in range(0, 18):
        moved_grid1[44][x] = "empty"

    #왼발 올라간 그림 저장
    draw_image(moved_grid1, "custom1_1.png")

    #오른발 위로
    moved_grid2 = copy.deepcopy(grid_colors)
    for y in range(41, 45):  #3칸을 한칸 위로
        for x in range(18, 42):  #가로 19~42
            moved_grid2[y - 1][x] = grid_colors[y][x]
    #아래 공백
    for x in range(18, 42):
        moved_grid2[44][x] = "empty"

    draw_image(moved_grid2, "custom1_2.png")

    show_dino_popup()
