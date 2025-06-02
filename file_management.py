#커스텀 이미지 외곽선 추가해서 저장및 불러오는 기능 (지연)
from PIL import Image, ImageDraw, ImageFilter
import os

from check_custom_Dino import show_dino_popup

def save_image(grid_colors, block_size=1):
    height = len(grid_colors)
    width = len(grid_colors[0])

    original_w = width * block_size  # 42
    original_h = height * block_size  # 45

    expanded_w = original_w + 2  # 44
    expanded_h = original_h + 2  # 47

    # 1. 원본 그림 (투명 배경)
    img = Image.new("RGBA", (original_w, original_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    for y in range(height):
        for x in range(width):
            color = grid_colors[y][x]
            if color == "empty":
                continue
            fill_color = color
            x0 = x * block_size
            y0 = y * block_size
            x1 = x0 + block_size - 1
            y1 = y0 + block_size - 1
            draw.rectangle([x0, y0, x1, y1], fill=fill_color)

    # 2. 확장된 캔버스 (투명 배경)
    expanded = Image.new("RGBA", (expanded_w, expanded_h), (0, 0, 0, 0))
    # 3. 원본 그림을 (1,1)에 붙여넣기 (중앙 배치)
    expanded.paste(img, (1, 1))

    # 4. 확장된 캔버스에서 외곽선 마스크 생성
    alpha = expanded.split()[3]
    outline_mask = alpha.filter(ImageFilter.MaxFilter(3))
    outline_mask = Image.eval(outline_mask, lambda px: 255 if px > 0 else 0)

    # 5. 흰색 외곽선 이미지 생성
    outline = Image.new("RGBA", expanded.size, (255, 255, 255, 0))
    outline.putalpha(outline_mask)

    # 6. 외곽선과 원본 그림 합성
    final = Image.alpha_composite(outline, expanded)

    # 7. 저장
    if not os.path.exists("dino_image"):
        os.makedirs("dino_image")
    final.save("dino_image/custom1.png")
    print(f"저장 완료: dino_image/custom1.png (크기: {final.size[0]} x {final.size[1]})")
    show_dino_popup()


