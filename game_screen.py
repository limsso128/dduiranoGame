# 일반 게임 화면 (소영)
import pygame
import sys
import random

class Obstacle:
    def __init__(self, img, x, y, speed, img2=None):
        self.img = img
        self.original_img = img  # 추가
        self.alt_img = img2  # 날갯짓 이미지
        self.x = x
        self.y = y
        self.speed = speed

    def update(self, dt):
        self.x -= self.speed * dt + speedUp

    def draw(self, screen):
        screen.blit(self.img, (int(self.x), self.y))

    def is_off_screen(self):
        return self.x + self.img.get_width() < 0

    def animate(self, swap_flag):
        if self.alt_img:
            self.img = self.alt_img if swap_flag else self.original_img

    def get_rect(self):
        width = self.img.get_width()
        height = self.img.get_height()
        padding_x = 25  # 좌우에서 10씩 줄이기
        padding_y = 15  # 위아래에서 5씩 줄이기

        return pygame.Rect(
            self.x + padding_x + 2,
            self.y + padding_y,
            width - padding_x * 2,  # 가로 크기 줄이기 (좌우 10씩 총 20 줄임)
            height - padding_y * 2  # 세로 크기 줄이기 (위아래 5씩 총 10 줄임)
        )


def starting_game(game_data=None, itemMode = False):
    from file_management import load_settings
    global items1, items2, p1Item, p2Item
    global beef_timer1, beef_timer2, banana_timer1, banana_timer2, fish_timer1, fish_timer2
    global speedUp,screen
    global gameOver, game_started, countdown, countdown_timer
    global speedUp, real_score, display_score, score_timer, frame_count
    global dino_y, dino2_y, dino_velocity, dino2_velocity
    global is_bottom, is_bottom2, is_shift1, is_shift2
    global leg_swap, leg_swap2
    global birds1, birds2, obstacles1, obstacles2, clouds1, clouds2
    global winner_name, looser_name, running

    pygame.init()
    MAX_WIDTH, MAX_HEIGHT = 1300, 700
    pygame.mixer.init()
    pygame.font.init()  # 폰트 초기화

    font = pygame.font.SysFont('HY헤드라인M', 30)  # 폰트 설정
    big_font = pygame.font.SysFont('malgun gothic', 80)  # 카운트다운용 큰 폰트
    button_font = pygame.font.SysFont('malgun gothic', 25)  # 버튼용 폰트

    # 2. 공룡 보여주기, 점프
    is_shift1 = False
    is_shift2 = False

    pygame.display.set_caption("dduirano")

    dino_velocity = 0
    dino2_velocity = 0

    isOnItemMode = itemMode
    frame_count = 0  # 전역 또는 게임 루프 바깥에 선언

    score_color = "black"

    SETTING_JSON = load_settings()
    volume = SETTING_JSON["volume"] / 100
    if not SETTING_JSON["bgm_on"]: volume = 0
    # 음악 불러오기
    pygame.mixer.music.load("./sounds/BGM.mp3")
    # 음악 재생 (무한 반복: -1)
    pygame.mixer.music.play(-1)
    # 초기 볼륨 설정 (0.0 ~ 1.0)
    pygame.mixer.music.set_volume(volume)

    jumpSound = pygame.mixer.Sound("./sounds/jumping.mp3")
    jumpSound.set_volume(0.5)  # 효과음 볼륨 (0.0 ~ 1.0)

    gameOverSound = pygame.mixer.Sound("./sounds/gameOver.mp3")
    gameOverSound.set_volume(0.5)  # 효과음 볼륨 (0.0 ~ 1.0)

    countSound = pygame.mixer.Sound("./sounds/countDown.mp3")
    countSound.set_volume(0.8)  # 효과음 볼륨 (0.0 ~ 1.0)

    itemSound = pygame.mixer.Sound("./sounds/eating.mp3")
    itemSound.set_volume(0.8)  # 효과음 볼륨 (0.0 ~ 1.0)
    is_dark = SETTING_JSON['is_dark']

    # 게임 데이터에서 커스텀 이미지 경로 설정
    p1_image_path1 = "./images/뛰라노_공룡(기본).png"
    p1_image_path2 = "./images/뛰라노_공룡(움직임).png"
    p2_image_path1 = "./images/뛰라노_공룡(기본).png"
    p2_image_path2 = "./images/뛰라노_공룡(움직임).png"

    p1Name = "Player 1"
    p2Name = "Player 2"
    if game_data:
        if 'p1_slot_path' in game_data:
            p1_image_path1 = f"{game_data['p1_slot_path']}/custom1_1.png"
            p1_image_path2 = f"{game_data['p1_slot_path']}/custom1_2.png"

        if 'p2_slot_path' in game_data:
            p2_image_path1 = f"{game_data['p2_slot_path']}/custom1_1.png"
            p2_image_path2 = f"{game_data['p2_slot_path']}/custom1_2.png"
        if 'p1_name' in game_data:
            p1Name = game_data["p1_name"]
        if 'p2_name' in game_data:
            p2Name = game_data["p2_name"]
    speedUp = 0

    gameOver = False
    running = True
    game_started = False  # 게임 시작 여부
    countdown = 3  # 카운트다운
    countdown_timer = 0  # 카운트다운 타이머

    real_score = 0  # 실제 점수 (1초에 10씩 증가)
    display_score = 0.0  # 화면에 보이는 점수
    score_timer = 0  # 시간 누적용

    # 스크린 세팅, fps
    screen = pygame.display.set_mode((MAX_WIDTH, MAX_HEIGHT), pygame.NOFRAME)
    fps = pygame.time.Clock()
    clock = pygame.time.Clock()  # 화면 업데이트 속도 제어용

    isDay = True
    # 배경 이미지
    if not is_dark:
        screenImageDay = pygame.image.load("./images/뛰라노_배경(기본하늘).png")  # 배경
    else:
        screenImageDay = pygame.image.load("./images/뛰라노_배경(사막하늘).png")  # 배경
    screenImageDay = pygame.transform.scale(screenImageDay, (MAX_WIDTH, MAX_HEIGHT // 2))

    screenImageNight = pygame.image.load("./images/뛰라노_배경(밤하늘).png")  # 배경
    screenImageNight = pygame.transform.scale(screenImageNight, (MAX_WIDTH, MAX_HEIGHT // 2))

    groundImage = pygame.image.load("./images/뛰라노_배경(바닥).png")  # 배경
    groundImage = pygame.transform.scale(groundImage, (MAX_WIDTH, MAX_HEIGHT // 2))

    def scale_transform(path, scale):
        img = pygame.image.load(path)
        return pygame.transform.scale(
            img,
            (int(img.get_width() * scale), int(img.get_height() * scale))
        )

    def shift_transform(path):
        img = pygame.image.load(path)
        return pygame.transform.scale(
            img,
            (int(img.get_width() * 2.4), int(img.get_height() * 1.2))
        )

    sunImage = scale_transform("./images/뛰라노_배경(해).png", 3)
    moonImage = scale_transform("./images/뛰라노_배경(달).png", 3)

    # === 공룡 이미지 ===
    try:
        imgDino1_1 = scale_transform(p1_image_path1, 2)
        imgDino1_2 = scale_transform(p1_image_path2, 2)
        shiftDino1_1 = shift_transform(p1_image_path1)
        shiftDino1_2 = shift_transform(p1_image_path2)
    except:
        # 파일이 없으면 기본 이미지 사용
        imgDino1_1 = scale_transform("./images/뛰라노_공룡(기본).png", 2)
        imgDino1_2 = scale_transform("./images/뛰라노_공룡(움직임).png", 2)
        shiftDino1_1 = shift_transform("./images/뛰라노_공룡(기본).png")
        shiftDino1_2 = shift_transform("./images/뛰라노_공룡(움직임).png")

    try:
        imgDino2_1 = scale_transform(p2_image_path1, 2)
        imgDino2_2 = scale_transform(p2_image_path2, 2)
        shiftDino2_1 = shift_transform(p2_image_path1)
        shiftDino2_2 = shift_transform(p2_image_path2)
    except:
        # 파일이 없으면 기본 이미지 사용
        imgDino2_1 = scale_transform("./images/뛰라노_공룡(기본).png", 2)
        imgDino2_2 = scale_transform("./images/뛰라노_공룡(움직임).png", 2)
        shiftDino2_1 = shift_transform("./images/뛰라노_공룡(기본).png")
        shiftDino2_2 = shift_transform("./images/뛰라노_공룡(움직임).png")

    # === 장애물 이미지 ===
    tree_speed = 400  # 초당 400픽셀 속도
    scale_factor = 2
    imgTree1 = scale_transform("images/뛰라노_장애물(작은선인장).png", scale_factor)
    imgTree2 = scale_transform("images/뛰라노_장애물(중간선인장).png", scale_factor)
    imgTree3 = scale_transform("images/뛰라노_장애물(큰선인장).png", scale_factor)

    imgBird1 = scale_transform("images/뛰라노_익룡(기본).png", scale_factor)
    imgBird2 = scale_transform("images/뛰라노_익룡(팔움직임).png", scale_factor)

    birds1 = []
    birds2 = []
    obstacles1 = []
    obstacles2 = []
    clouds1 = []
    clouds2 = []

    items1 = []
    items2 = []

    # === 구름 이미지 ===
    imgCloud1 = scale_transform("images/뛰라노_배경(구름.1).png", scale_factor)
    imgCloud2 = scale_transform("images/뛰라노_배경(구름.2).png", scale_factor)
    imgCloud3 = scale_transform("images/뛰라노_배경(뛰라노구름).png", 1.8)

    # 이 부분에서 dino_height와 dino2_height를 다시 계산
    dino_height = imgDino1_1.get_size()[1]  # 스케일링된 첫 번째 공룡의 높이
    dino2_height = imgDino2_1.get_size()[1]  # 스케일링된 두 번째 공룡의 높이

    # 공룡1 세팅
    dino_bottom = (MAX_HEIGHT // 2) - dino2_height - 10  # 공룡이 바닥에 딱 붙어있게
    dino_x = 50
    dino_y = dino_bottom
    leg_swap2 = True  # 다리 번걸아 바꾸기 -> true면 1_1, false면 1_2 이미지 사용
    is_bottom2 = True  # 공룡이 바닥에 서있는 상태 -> True 점프 가능, False 점프 중
    gravity2 = 3

    # 공룡2 세팅
    dino2_bottom = MAX_HEIGHT - dino_height - 10  # 공룡이 바닥에 딱 붙어있게
    dino2_x = 50
    dino2_y = dino2_bottom
    leg_swap = True  # 다리 번걸아 바꾸기 -> true면 1_1, false면 1_2 이미지 사용
    is_bottom = True  # 공룡이 바닥에 서있는 상태 -> True 점프 가능, False 점프 중
    gravity = 3

    def jumping(key_pressed, is_bottom, velocity, jump_key):
        max_jump = -150
        if not is_bottom and key_pressed[jump_key]:
            velocity -= 2
            if velocity < max_jump:
                velocity = max_jump
        return velocity

    # 선인장 이미지 리스트
    tree_images = [imgTree1, imgTree2, imgTree3]

    def spawn_obstacle(obstacle_list, is_top, img_options):
        ranNum = random.randint(1, 3)
        ranNum2 = random.randint(1, 3)

        img = img_options[ranNum - 1]
        img_height = img.get_height()
        x = MAX_WIDTH

        if is_top:
            y = (MAX_HEIGHT // 2) - img_height - 10
        else:
            y = MAX_HEIGHT - img_height - 10

        # 장애물 추가 (1개 또는 2개)
        obstacle_list.append(Obstacle(img, x, y, tree_speed))
        if ranNum2 == 1:
            obstacle_list.append(Obstacle(img, x + 40, y, tree_speed))
        elif ranNum2 == 2:
            obstacle_list.append(Obstacle(img, x + 40, y, tree_speed))
            obstacle_list.append(Obstacle(img, x + 80, y, tree_speed))

    # 익룡 생성
    def spawn_Bird(Bird_list, is_top):
        ranNum = random.choice([20, 50, 70, 100, 110])
        ranNum2 = random.choice([60, 75, 100, 110])
        ranNum3 = random.choice([40, 200])
        ranNum4 = random.choice([1, 2])

        img1 = imgBird1
        img2 = imgBird2
        img_height = img1.get_height()
        x = MAX_WIDTH

        if is_top:
            y = (MAX_HEIGHT // 2) - img_height - ranNum
            y2 = (MAX_HEIGHT // 2) - img_height - ranNum2
        else:
            y = MAX_HEIGHT - img_height - ranNum
            y2 = MAX_HEIGHT - img_height - ranNum2

        Bird_list.append(Obstacle(img1, x - 50, y, tree_speed, img2))
        if ranNum4 == 1:
            Bird_list.append(Obstacle(img1, x + ranNum3, y2, tree_speed, img2))

    # 구름 이미지 리스트
    clouds = [imgCloud1, imgCloud2, imgCloud3]
    big_cloud = False

    def spawn_cloud(clouds_list, is_top, img_options, big):
        ranNum = random.randint(1, 2)
        if big:
            img = img_options[2]
        else:
            ranScale = random.randint(2, 4)
            ranY = random.choice([0, -40, -20])
            img = img_options[ranNum - 1]
            img = pygame.transform.scale(
                img,
                (int(img.get_width() * ranScale), int(img.get_height() * ranScale))
            )
        img_height = img.get_height()
        x = MAX_WIDTH
        if big:
            if is_top:
                y = (MAX_HEIGHT // 2) - img_height - 190
            else:
                y = MAX_HEIGHT - img_height - 190
        else:
            if is_top:
                y = (MAX_HEIGHT // 2) - img_height - 190 + ranY
            else:
                y = MAX_HEIGHT - img_height - 190 + ranY

        clouds_list.append(Obstacle(img, x, y, tree_speed))

############################### 아이템 모드 #################################
    beef_timer1 = 0  # 고기 효과 타이머 (디노1)
    beef_timer2 = 0  # 고기 효과 타이머 (디노2)
    banana_timer1 = 0  # 바나나 효과 타이머 (디노1)
    banana_timer2 = 0  # 바나나 효과 타이머 (디노2)
    fish_timer1 = 0
    fish_timer2 = 0
    p1Item = "Null"
    p2Item = "Null"

    item1 = scale_transform("./images/item1.png", 2)
    item2 = scale_transform("./images/item2.png", 2)
    item3 = scale_transform("./images/item3.png", 2)

    itemList = [item1, item2, item3]
    def spawn_item(item_list, is_top):
        ranNum = random.randint(1, 3)
        ramNum2 = random.choice([0, 30, 60, 90])
        img = itemList[ranNum - 1]
        img_height = img.get_height()
        x = MAX_WIDTH

        if is_top:
            y = (MAX_HEIGHT // 2) - img_height - ramNum2
        else:
            y = (MAX_HEIGHT) - img_height - ramNum2

        obstacle = Obstacle(img, x - 50, y, tree_speed)
        obstacle.item_type = ranNum  # 아이템 타입 추가 (1, 2, 3)
        item_list.append(obstacle)

    # 좌우반전된 이미지들 (고기 효과용)
    imgDino1_1_flipped = pygame.transform.flip(imgDino1_1, True, False)
    imgDino1_2_flipped = pygame.transform.flip(imgDino1_2, True, False)
    shiftDino1_1_flipped = pygame.transform.flip(shiftDino1_1, True, False)
    shiftDino1_2_flipped = pygame.transform.flip(shiftDino1_2, True, False)

    imgDino2_1_flipped = pygame.transform.flip(imgDino2_1, True, False)
    imgDino2_2_flipped = pygame.transform.flip(imgDino2_2, True, False)
    shiftDino2_1_flipped = pygame.transform.flip(shiftDino2_1, True, False)
    shiftDino2_2_flipped = pygame.transform.flip(shiftDino2_2, True, False)

        # 얇아진 이미지들 (바나나 효과용)
    def create_thin_images():
        thin_imgDino1_1 = pygame.transform.scale(imgDino1_1,(int(imgDino1_1.get_width() * 0.8), imgDino1_1.get_height() * 0.8))
        thin_imgDino1_2 = pygame.transform.scale(imgDino1_2,(int(imgDino1_2.get_width() * 0.8), imgDino1_2.get_height() * 0.8))
        thin_shiftDino1_1 = pygame.transform.scale(shiftDino1_1,(int(shiftDino1_1.get_width() * 0.8), shiftDino1_1.get_height() * 0.8))
        thin_shiftDino1_2 = pygame.transform.scale(shiftDino1_2,(int(shiftDino1_2.get_width() * 0.8), shiftDino1_2.get_height() * 0.8))

        thin_imgDino2_1 = pygame.transform.scale(imgDino2_1,(int(imgDino2_1.get_width() * 0.8), imgDino2_1.get_height() * 0.8))
        thin_imgDino2_2 = pygame.transform.scale(imgDino2_2,(int(imgDino2_2.get_width() * 0.8), imgDino2_2.get_height() * 0.8))
        thin_shiftDino2_1 = pygame.transform.scale(shiftDino2_1,(int(shiftDino2_1.get_width() * 0.8), shiftDino2_1.get_height() * 0.8))
        thin_shiftDino2_2 = pygame.transform.scale(shiftDino2_2,(int(shiftDino2_2.get_width() * 0.8), shiftDino2_2.get_height() * 0.8))

        return (thin_imgDino1_1, thin_imgDino1_2, thin_shiftDino1_1, thin_shiftDino1_2,
                thin_imgDino2_1, thin_imgDino2_2, thin_shiftDino2_1, thin_shiftDino2_2)

    thin_images = create_thin_images()
    (thin_imgDino1_1, thin_imgDino1_2, thin_shiftDino1_1, thin_shiftDino1_2,
     thin_imgDino2_1, thin_imgDino2_2, thin_shiftDino2_1, thin_shiftDino2_2) = thin_images

    def use_beef(dinoNum):
        global beef_timer1, beef_timer2

        if dinoNum == 1:  # 위공룡이 사용
            beef_timer2 = 5.0  # 아래공룡을 5초동안 뒤로 보냄
        else:  # 아래공룡이 사용
            beef_timer1 = 5.0  # 위공룡을 5초동안 뒤로 보냄

    def use_banana(dinoNum):
        global banana_timer1, banana_timer2

        if dinoNum == 1:  # 위공룡이 사용
            banana_timer1 = 3.0  # 자기 자신이 3초동안 얇아짐
        else:  # 아래공룡이 사용
            banana_timer2 = 3.0  # 자기 자신이 3초동안 얇아짐

    def use_fish(dinoNum):
        global birds1, birds2, obstacles1, obstacles2

        if dinoNum == 1:
            birds1.pop()
            obstacles1.pop()
        else:
            birds2.pop()
            obstacles2.pop()

    # 아이템 효과 업데이트
    def update_item_effects(dt):
        global beef_timer1, beef_timer2, banana_timer1, banana_timer2

        # 타이머 감소
        if beef_timer1 > 0:
            beef_timer1 -= dt
            if beef_timer1 <= 0:
                beef_timer1 = 0

        if beef_timer2 > 0:
            beef_timer2 -= dt
            if beef_timer2 <= 0:
                beef_timer2 = 0

        if banana_timer1 > 0:
            banana_timer1 -= dt
            if banana_timer1 <= 0:
                banana_timer1 = 0

        if banana_timer2 > 0:
            banana_timer2 -= dt
            if banana_timer2 <= 0:
                banana_timer2 = 0

    # 공룡 그리기
    def draw_dinosaurs():
        global dino1_rect, dino2_rect

        # 공룡1 그리기
        if banana_timer1 > 0:  # 바나나 효과 중
            if is_shift1:
                orig_rect = pygame.Rect(dino_x, dino_y +39, thin_shiftDino1_1.get_width(),
                                        thin_shiftDino1_1.get_height())
                dino1_rect = pygame.Rect(orig_rect.x + 4, orig_rect.y + 5, orig_rect.width - 8, orig_rect.height - 10)
                if beef_timer1 > 0:  # 고기 효과도 함께
                    screen.blit(
                        pygame.transform.flip(thin_shiftDino1_1 if leg_swap else thin_shiftDino1_2, True, False),
                        (dino_x, dino_y+50+ 39))
                else:
                    screen.blit(thin_shiftDino1_1 if leg_swap else thin_shiftDino1_2, (dino_x, dino_y + 39))
            else:
                orig_rect = pygame.Rect(dino_x, dino_y, thin_imgDino1_1.get_width(), thin_imgDino1_1.get_height())
                dino1_rect = pygame.Rect(orig_rect.x + 4, orig_rect.y + 5, orig_rect.width - 8, orig_rect.height - 10)
                if beef_timer1 > 0:  # 고기 효과도 함께
                    screen.blit(pygame.transform.flip(thin_imgDino1_1 if leg_swap else thin_imgDino1_2, True, False),
                                (dino_x, dino_y))
                else:
                    screen.blit(thin_imgDino1_1 if leg_swap else thin_imgDino1_2, (dino_x, dino_y))
        else:  # 바나나 효과 없음
            if is_shift1:
                orig_rect = pygame.Rect(dino_x, dino_y + 39, shiftDino1_1.get_width(), shiftDino1_1.get_height())
                dino1_rect = pygame.Rect(orig_rect.x + 8, orig_rect.y + 5, orig_rect.width - 16, orig_rect.height - 10)
                if beef_timer1 > 0:  # 고기 효과
                    screen.blit(shiftDino1_1_flipped if leg_swap else shiftDino1_2_flipped, (dino_x, dino_y + 39))
                else:
                    screen.blit(shiftDino1_1 if leg_swap else shiftDino1_2, (dino_x, dino_y + 39))
            else:
                orig_rect = pygame.Rect(dino_x, dino_y, imgDino1_1.get_width(), imgDino1_1.get_height())
                dino1_rect = pygame.Rect(orig_rect.x + 8, orig_rect.y + 5, orig_rect.width - 16, orig_rect.height - 10)
                if beef_timer1 > 0:  # 고기 효과
                    screen.blit(imgDino1_1_flipped if leg_swap else imgDino1_2_flipped, (dino_x, dino_y))
                else:
                    screen.blit(imgDino1_1 if leg_swap else imgDino1_2, (dino_x, dino_y))

        # 공룡2 그리기
        if banana_timer2 > 0:  # 바나나 효과 중
            if is_shift2:
                orig_rect = pygame.Rect(dino2_x, dino2_y + 39, thin_shiftDino2_1.get_width(),
                                        thin_shiftDino2_1.get_height())
                dino2_rect = pygame.Rect(orig_rect.x + 4, orig_rect.y + 5, orig_rect.width - 8, orig_rect.height - 10)
                if beef_timer2 > 0:  # 고기 효과도 함께
                    screen.blit(
                        pygame.transform.flip(thin_shiftDino2_1 if leg_swap2 else thin_shiftDino2_2, True, False),
                        (dino2_x, dino2_y + 39))
                else:
                    screen.blit(thin_shiftDino2_1 if leg_swap2 else thin_shiftDino2_2, (dino2_x, dino2_y + 39))
            else:
                orig_rect = pygame.Rect(dino2_x, dino2_y, thin_imgDino2_1.get_width(), thin_imgDino2_1.get_height())
                dino2_rect = pygame.Rect(orig_rect.x + 4, orig_rect.y + 5, orig_rect.width - 8, orig_rect.height - 10)
                if beef_timer2 > 0:  # 고기 효과도 함께
                    screen.blit(pygame.transform.flip(thin_imgDino2_1 if leg_swap2 else thin_imgDino2_2, True, False),
                                (dino2_x, dino2_y +500))
                else:
                    screen.blit(thin_imgDino2_1 if leg_swap2 else thin_imgDino2_2, (dino2_x, dino2_y))
        else:  # 바나나 효과 없음
            if is_shift2:
                orig_rect = pygame.Rect(dino2_x, dino2_y + 39, shiftDino2_1.get_width(), shiftDino2_1.get_height())
                dino2_rect = pygame.Rect(orig_rect.x + 8, orig_rect.y + 5, orig_rect.width - 16, orig_rect.height - 10)
                if beef_timer2 > 0:  # 고기 효과
                    screen.blit(shiftDino2_1_flipped if leg_swap2 else shiftDino2_2_flipped, (dino2_x, dino2_y + 39))
                else:
                    screen.blit(shiftDino2_1 if leg_swap2 else shiftDino2_2, (dino2_x, dino2_y + 39))
            else:
                orig_rect = pygame.Rect(dino2_x, dino2_y, imgDino2_1.get_width(), imgDino2_1.get_height())
                dino2_rect = pygame.Rect(orig_rect.x + 8, orig_rect.y + 5, orig_rect.width - 16, orig_rect.height - 10)
                if beef_timer2 > 0:  # 고기 효과
                    screen.blit(imgDino2_1_flipped if leg_swap2 else imgDino2_2_flipped, (dino2_x, dino2_y))
                else:
                    screen.blit(imgDino2_1 if leg_swap2 else imgDino2_2, (dino2_x, dino2_y))


############################### 게임오버시 ###################################
    def go_to_menu():
        global running
        running = False  # 게임 루프 종료를 유도
        pygame.quit()

    def restart_game():
        global items1, items2, p1Item, p2Item
        global beef_timer1, beef_timer2, banana_timer1, banana_timer2, fish_timer1, fish_timer2
        global gameOver, game_started, countdown, countdown_timer
        global speedUp, real_score, display_score, score_timer, frame_count
        global dino_y, dino2_y, dino_velocity, dino2_velocity
        global is_bottom, is_bottom2, is_shift1, is_shift2
        global leg_swap, leg_swap2
        global birds1, birds2, obstacles1, obstacles2, clouds1, clouds2
        global winner_name, looser_name, running

        gameOver = False
        game_started = False
        countdown = 4
        countdown_timer = 0
        speedUp = 0
        real_score = 0
        display_score = 0.0
        score_timer = 0
        frame_count = 0

        dino_y = dino_bottom
        dino2_y = dino2_bottom
        dino_velocity = 0
        dino2_velocity = 0
        is_bottom = True
        is_bottom2 = True
        is_shift1 = False
        is_shift2 = False
        leg_swap = True
        leg_swap2 = True

        birds1.clear()
        birds2.clear()
        obstacles1.clear()
        obstacles2.clear()
        clouds1.clear()
        clouds2.clear()

        winner_name = ""
        looser_name = ""

        SETTING_JSON = load_settings()
        volume = SETTING_JSON["volume"] / 100
        if not SETTING_JSON["bgm_on"]: volume = 0
        # 음악 불러오기
        pygame.mixer.music.load("./sounds/BGM.mp3")
        # 음악 재생 (무한 반복: -1)
        pygame.mixer.music.play(-1)
        # 초기 볼륨 설정 (0.0 ~ 1.0)
        pygame.mixer.music.set_volume(volume)

        countSound.play()

        beef_timer1 = 0  # 고기 효과 타이머 (디노1)
        beef_timer2 = 0  # 고기 효과 타이머 (디노2)
        banana_timer1 = 0  # 바나나 효과 타이머 (디노1)
        banana_timer2 = 0  # 바나나 효과 타이머 (디노2)
        fish_timer1 = 0
        fish_timer2 = 0
        p1Item = "Null"
        p2Item = "Null"

        items1 = []
        items2 = []

    ############################################   루프   ###################################################

    winner_name = ""
    looser_name = ""
    countSound.play()
    while running:
        if not game_started and not gameOver:
            # 카운트다운 화면
            dt = clock.tick(50) / 1000
            countdown_timer += dt

            screen.fill((255, 255, 255))

            # 배경 그리기
            screen.blit(screenImageDay, (0, 0))
            screen.blit(screenImageDay, (0, MAX_HEIGHT // 2))
            screen.blit(groundImage, (0, 0))
            screen.blit(groundImage, (0, MAX_HEIGHT // 2))

            # 공룡들 그리기
            screen.blit(imgDino1_1, (dino_x, dino_y))
            screen.blit(imgDino2_1, (dino2_x, dino2_y))

            # 카운트다운 표시
            if countdown > 0:
                countdown_text = big_font.render(str(countdown), True, (255, 0, 0))
                text_rect = countdown_text.get_rect(center=(MAX_WIDTH // 2, MAX_HEIGHT // 2))
                screen.blit(countdown_text, text_rect)

                if countdown_timer >= 1.0:
                    countdown -= 1
                    countdown_timer = 0
            else:
                start_text = big_font.render("START!", True, (0, 255, 0))
                text_rect = start_text.get_rect(center=(MAX_WIDTH // 2, MAX_HEIGHT // 2))
                screen.blit(start_text, text_rect)

                if countdown_timer >= 1.0:
                    game_started = True
                    countdown_timer = 0

            # 이벤트 처리
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()
        elif game_started and not gameOver:
            dt = clock.tick(50) / 1000  # 초 단위 delta time
            screen.fill((255, 255, 255))
            # 속도 서서히  증가
            speedUp += 0.0018
            ########### 점프 공룡1
            if not is_bottom:  # 땅에 안 닿음(점프)
                dino_y += dino_velocity
                dino_velocity += gravity

                if dino_y >= dino_bottom:  # 땅에 닿아질때 초기화
                    dino_y = dino_bottom
                    is_bottom = True
                    dino_velocity = 0
            ############ 점프 공룡2
            if not is_bottom2:
                dino2_y += dino2_velocity
                dino2_velocity += gravity2

                if dino2_y >= dino2_bottom:
                    dino2_y = dino2_bottom
                    is_bottom2 = True
                    dino2_velocity = 0

            ############ 키 이벤트 처리 (모든 이벤트를 하나의 루프에서 처리)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # 점프 키 누름
                if event.type == pygame.KEYDOWN:
                    # 점프 처리
                    if event.key == pygame.K_w and is_bottom:  # 위 (w)
                        jumpSound.play()
                        is_bottom = False
                        dino_velocity = -17  # 최소 점프

                    elif event.key == pygame.K_UP and is_bottom2:  # 아래 (화살표 위)
                        jumpSound.play()
                        is_bottom2 = False
                        dino2_velocity = -17  # 최소 점프

                    # 웅크림 시작
                    elif event.key == pygame.K_s:
                        is_shift1 = True
                    elif event.key == pygame.K_DOWN:
                        is_shift2 = True

                    # 아이템 사용 (아이템 모드일 때만)
                    elif isOnItemMode:
                        if event.key == pygame.K_q:
                            if p1Item == 1:
                                use_beef(1)  # 고기 사용
                                itemSound.play()
                                p1Item = "Null"
                            elif p1Item == 2:
                                use_banana(1)  # 바나나 사용
                                itemSound.play()
                                p1Item = "Null"
                            elif p1Item == 3:
                                use_fish(1)  # 물고기 사용
                                itemSound.play()
                                p1Item = "Null"

                        elif event.key == pygame.K_LEFT:
                            if p2Item == 1:
                                use_beef(2)  # 고기 사용
                                itemSound.play()
                                p2Item = "Null"
                            elif p2Item == 2:
                                use_banana(2)  # 바나나 사용
                                itemSound.play()
                                p2Item = "Null"
                            elif p2Item == 3:
                                use_fish(2)  # 물고기 사용
                                itemSound.play()
                                p2Item = "Null"

                if event.type == pygame.KEYUP:
                    # Shift에서 손 뗐을 때 웅크리기 해제
                    if event.key == pygame.K_s:
                        is_shift1 = False
                    elif event.key == pygame.K_DOWN:
                        is_shift2 = False
            # 꾹누르면 높게 점프
            keys = pygame.key.get_pressed()
            dino_velocity = jumping(keys, is_bottom, dino_velocity, pygame.K_w)
            dino2_velocity = jumping(keys, is_bottom2, dino2_velocity, pygame.K_UP)

            # 배경(하늘)
            if int(display_score) % 500 == 0 and real_score >= 20:
                isDay = not isDay

            if isDay:
                screen.blit(screenImageDay, (0, 0))
                screen.blit(screenImageDay, (0, MAX_HEIGHT // 2))

                screen.blit(sunImage, (MAX_WIDTH - 300 - speedUp * 7, MAX_HEIGHT - 300))
                screen.blit(sunImage, (MAX_WIDTH - 300 - speedUp * 7, MAX_HEIGHT // 2 - 300))
            else:
                screen.blit(screenImageNight, (0, 0))
                screen.blit(screenImageNight, (0, MAX_HEIGHT // 2))

                screen.blit(moonImage, (MAX_WIDTH - 300 - speedUp * 7, MAX_HEIGHT - 300))
                screen.blit(moonImage, (MAX_WIDTH - 300 - speedUp * 7, MAX_HEIGHT // 2 - 300))
            # 배경(땅)
            screen.blit(groundImage, (0, 0))
            screen.blit(groundImage, (0, MAX_HEIGHT // 2))

            # 프레임 카운트
            frame_count += 1

            # 큰 구름 생성
            if frame_count == 700:
                spawn_cloud(clouds_list=clouds1, is_top=True, img_options=clouds, big=True)
                spawn_cloud(clouds_list=clouds2, is_top=False, img_options=clouds, big=True)
                big_cloud = True
            if frame_count == 740:
                big_cloud = False

            # 큰 구름 생성중이 아닐 때 작은 구름 생성
            if (frame_count % 70 == 0 or frame_count % 160 == 0) and not (big_cloud):
                spawn_cloud(clouds_list=clouds1, is_top=True, img_options=clouds, big=False)
                spawn_cloud(clouds_list=clouds2, is_top=False, img_options=clouds, big=False)

            # 위쪽 장애물 생성
            if frame_count % 40 == 0:
                if (frame_count // 40) % 2 == 0:
                    spawn_obstacle(obstacles1, is_top=True, img_options=tree_images)
                else:
                    spawn_Bird(birds1, is_top=True)

            # 아래쪽 장애물 생성 (위보다 30프레임 늦게 시작)
            if (frame_count + 20) % 40 == 0:
                if ((frame_count + 20) // 40) % 2 == 0:
                    spawn_obstacle(obstacles2, is_top=False, img_options=tree_images)
                else:
                    spawn_Bird(birds2, is_top=False)

            for bird in birds1 + birds2:
                bird.animate(leg_swap)

            # 장애물 왼쪽으로 움직이기
            for obstacle_list in [obstacles1, obstacles2, birds1, birds2, items1, items2]:
                for obs in obstacle_list[:]:
                    obs.update(dt)
                    obs.draw(screen)
                    if obs.is_off_screen():
                        obstacle_list.remove(obs)

            # 구름 왼쪽으로 움직이기
            for cloud_list in [clouds1, clouds2]:
                for cloud in cloud_list[:]:
                    cloud.update(dt)
                    cloud.draw(screen)
                    if cloud.is_off_screen():
                        cloud_list.remove(cloud)

            # 공룡 다리 애니메이션
            if frame_count % 3 == 0:  # 3프레임당 하나
                leg_swap = not leg_swap
                leg_swap2 = not leg_swap2

            # 메인 루프 안에서 (dt 계산 후)
            update_item_effects(dt)
            # 기존 공룡 그리기 코드를 이것으로 교체
            draw_dinosaurs()
            ##################################################### 만약 아이템모드라면... #############################################
            # 아이템 UI 표시
            if isOnItemMode:
                if p1Item == 1:
                    screen.blit(item1, (30, 30))
                elif p1Item == 2:
                    screen.blit(item2, (30, 30))
                elif p1Item == 3:
                    screen.blit(item3, (30, 30))

                if p2Item == 1:
                    screen.blit(item1, (30, (MAX_HEIGHT // 2) + 30))
                elif p2Item == 2:
                    screen.blit(item2, (30, (MAX_HEIGHT // 2) + 30))
                elif p2Item == 3:
                    screen.blit(item3, (30, (MAX_HEIGHT // 2) + 30))

                #아이템 소환
                if frame_count % 200 == 0:
                    spawn_item(item_list=items1, is_top=True)
                    spawn_item(item_list=items2, is_top=False)

                # 아이템 충돌판정 (한 번만!)
                for items_list in [items1, items2]:
                    for item in items_list[:]:  # 복사본으로 순회
                        rect = item.get_rect()
                        if dino1_rect.colliderect(rect) and p1Item == "Null":  # 이미 아이템이 있으면 무시
                            p1Item = item.item_type  # 아이템 타입 번호만 저장
                            items_list.remove(item)  # 먹은 아이템 제거
                            break  # 하나만 먹고 끝
                        elif dino2_rect.colliderect(rect) and p2Item == "Null":  # 이미 아이템이 있으면 무시
                            p2Item = item.item_type  # 아이템 타입 번호만 저장
                            items_list.remove(item)  # 먹은 아이템 제거
                            break  # 하나만 먹고 끝



            #숫자 너무 안 커지게
            if frame_count >= 801:
                frame_count = 0

            score_timer += dt

            # 1초마다 실제 점수 10점 증가
            if score_timer >= 1.0:
                real_score += 10
                score_timer -= 1.0

            # 점수 색상 결정
            score_color = (0, 0, 0) if isDay else (255, 255, 255)

            # 보이는 점수는 실제 점수까지 0.2씩 증가
            if display_score < real_score:
                display_score += 0.2

            score_str = str(int(display_score)).zfill(5)
            score_text = font.render(score_str, True, score_color)
            screen.blit(score_text, (screen.get_width() - 100, 20))

            # 충돌 체크
            for obs_list in [obstacles1, obstacles2, birds1, birds2]:
                for obs in obs_list:
                    rect = obs.get_rect()
                    if dino1_rect.colliderect(rect):
                        looser_name = p1Name
                        winner_name = p2Name
                        gameOver = True
                        break
                    if dino2_rect.colliderect(rect):
                        looser_name = p2Name
                        winner_name = p1Name
                        gameOver = True
                        break
                if gameOver:
                    gameOverSound.play()
                    break

            pygame.display.update()
            fps.tick(50)  # 50FPS 고정
        elif gameOver:
            pygame.mixer.music.stop()
            # 배경 그리기
            if isDay:
                screen.blit(screenImageDay, (0, 0))
                screen.blit(screenImageDay, (0, MAX_HEIGHT // 2))
            else:
                screen.blit(screenImageNight, (0, 0))
                screen.blit(screenImageNight, (0, MAX_HEIGHT // 2))
            screen.blit(groundImage, (0, 0))
            screen.blit(groundImage, (0, MAX_HEIGHT // 2))

            # 공룡들 그리기 (마지막 위치에)
            if is_shift1:
                screen.blit(shiftDino1_1 if leg_swap else shiftDino1_2, (dino_x, dino_y + 39))
            else:
                screen.blit(imgDino1_1 if leg_swap else imgDino1_2, (dino_x, dino_y))

            if is_shift2:
                screen.blit(shiftDino2_1 if leg_swap2 else shiftDino2_2, (dino2_x, dino2_y + 39))
            else:
                screen.blit(imgDino2_1 if leg_swap2 else imgDino2_2, (dino2_x, dino2_y))

            # 장애물들도 그리기
            for obstacle_list in [obstacles1, obstacles2, birds1, birds2]:
                for obs in obstacle_list:
                    obs.draw(screen)

            # 승리 메시지 (화면 중앙)
            win_text = font.render(f"{winner_name}님이 {looser_name}님을 완전히 짓밟았어요!", True, score_color)
            win_rect = win_text.get_rect(center=(MAX_WIDTH // 2, MAX_HEIGHT // 2))
            screen.blit(win_text, win_rect)

            # 돌아가기 버튼 (왼쪽 아래)
            back_button_rect = pygame.Rect(MAX_WIDTH // 2 - 200, MAX_HEIGHT // 2 + 50, 120, 50)

            # 버튼 배경 그리기 (회색)
            pygame.draw.rect(screen, (100, 185, 100), back_button_rect)  # ← 버튼 배경색 (변경 가능: 예: (180, 220, 255))
            pygame.draw.rect(screen, (15, 100, 15), back_button_rect, 2)  # ← 버튼 테두리색 (굵기 2)

            # 버튼 텍스트 그리기
            back_text = button_font.render("돌아가기", True, (0, 0, 0))  # ← 텍스트 색상도 변경 가능
            back_text_rect = back_text.get_rect(center=back_button_rect.center)
            screen.blit(back_text, back_text_rect)

            # 재시작 버튼 (오른쪽 아래)
            restart_button_rect = pygame.Rect(MAX_WIDTH // 2 + 50, MAX_HEIGHT // 2 + 50, 120, 50)
            pygame.draw.rect(screen, (100, 185, 100), restart_button_rect)
            pygame.draw.rect(screen, (15, 100, 15), restart_button_rect, 2)

            restart_text = button_font.render("재시작", True, (0, 0, 0))
            restart_text_rect = restart_text.get_rect(center=restart_button_rect.center)
            screen.blit(restart_text, restart_text_rect)

            pygame.display.update()

            # 이벤트 처리
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if back_button_rect.collidepoint(mouse_pos):
                        go_to_menu()
                    elif restart_button_rect.collidepoint(mouse_pos):
                        restart_game()

if __name__ == "__main__":
    starting_game()