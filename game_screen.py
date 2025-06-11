#일반 게임 화면 (소영)
import pygame
import sys

#1. 스크린 세팅, fps(루프속도)
#2. 공룡 보여주기, 점프

pygame.init()
pygame.display.set_caption("dduirano")
MAX_WIDTH, MAX_HEIGHT = 1300, 700

def main():
    #스크린 세팅, fps
    screen = pygame.display.set_mode((MAX_WIDTH, MAX_HEIGHT))
    fps = pygame.time.Clock()

    # 배경 이미지
    screen1 = pygame.image.load("./images/뛰라노_배경(기본하늘).png")  # 위쪽 배경
    screen2 = pygame.image.load("./images/뛰라노_배경(기본하늘).png")  # 아래쪽 배경
    # 배경 이미지 크기 조절
    screen1 = pygame.transform.scale(screen1, (MAX_WIDTH, MAX_HEIGHT // 2))
    screen2 = pygame.transform.scale(screen2, (MAX_WIDTH, MAX_HEIGHT // 2))

    #공룡1 이미지
    imgDino1_1 = pygame.image.load("./images/뛰라노_공룡(기본).png")
    imgDino1_2 = pygame.image.load("./images/뛰라노_공룡(움직임).png")
    #공룡2 이미지
    imgDino2_1 = pygame.image.load("./images/뛰라노_공룡(기본).png")
    imgDino2_2 = pygame.image.load("./images/뛰라노_공룡(움직임).png")


    #공룡 크기 키우기
    scale_factor = 2
    imgDino1_1 = pygame.transform.scale(
        imgDino1_1,
        (int(imgDino1_1.get_width() * scale_factor), int(imgDino1_1.get_height() * scale_factor))
    )
    imgDino1_2 = pygame.transform.scale(
        imgDino1_2,
        (int(imgDino1_2.get_width() * scale_factor), int(imgDino1_2.get_height() * scale_factor))
    )
    imgDino2_1 = pygame.transform.scale(  # 공룡 2 크기 조절
        imgDino2_1,
        (int(imgDino2_1.get_width() * scale_factor), int(imgDino2_1.get_height() * scale_factor))
    )
    imgDino2_2 = pygame.transform.scale(  # 공룡 2 크기 조절
        imgDino2_2,
        (int(imgDino2_2.get_width() * scale_factor), int(imgDino2_2.get_height() * scale_factor))
    )

    # 이 부분에서 dino_height와 dino2_height를 다시 계산
    dino_height = imgDino1_1.get_size()[1]  # 스케일링된 첫 번째 공룡의 높이
    dino2_height = imgDino2_1.get_size()[1]  # 스케일링된 두 번째 공룡의 높이

    #공룡1 세팅
    dino_bottom = MAX_HEIGHT - dino_height - 10  # 공룡이 바닥에 딱 붙어있게
    dino_x = 50
    dino_y = dino_bottom
    jump_top = 400
    leg_swap = True  # 다리 번걸아 바꾸기 -> true면 1_1, false면 1_2 이미지 사용
    is_bottom = True  # 공룡이 바닥에 서있는 상태 -> True 점프 가능, False 점프 중
    is_go_up = False  # 올라가는 중인지 -> true면 점프 시작, false는 최고점 도달, 아래로 떨어짐

    # 공룡2 세팅
    dino2_bottom = (MAX_HEIGHT // 2) - dino2_height - 10  # 공룡이 바닥에 딱 붙어있게
    dino2_x = 50
    dino2_y = dino2_bottom
    jump_top2 = 50
    leg_swap2 = True  # 다리 번걸아 바꾸기 -> true면 1_1, false면 1_2 이미지 사용
    is_bottom2 = True  # 공룡이 바닥에 서있는 상태 -> True 점프 가능, False 점프 중
    is_go_up2 = False  # 올라가는 중인지 -> true면 점프 시작, false는 최고점 도달, 아래로

    #공룡1의 장애물
    #선인장(소)
    imgTree1_1 = pygame.image.load('images/뛰라노_장애물(작은선인장).png')
    tree1_1_height = imgTree1_1.get_size()[1]
    tree1_1_x = MAX_WIDTH
    tree1_1_y = MAX_HEIGHT - tree1_1_height
    # 선인장(중)
    imgTree1_2 = pygame.image.load('images/뛰라노_장애물(중간선인장).png')
    tree1_2_height = imgTree1_2.get_size()[1]
    tree1_2_x = MAX_WIDTH
    tree1_2_y = MAX_HEIGHT - tree1_2_height
    # 선인장(대)
    imgTree1_3 = pygame.image.load('images/뛰라노_장애물(큰선인장) (2).png')
    tree1_3_height = imgTree1_3.get_size()[1]
    tree1_3_x = MAX_WIDTH
    tree1_3_y = MAX_HEIGHT - tree1_3_height

    # 공룡2의 장애물
    # 선인장(소)
    imgTree2_1 = pygame.image.load('images/뛰라노_장애물(작은선인장).png')
    tree2_1_height = imgTree2_1.get_size()[1]
    tree2_1_x = MAX_WIDTH
    tree2_1_y = (MAX_HEIGHT // 2) - tree2_1_height
    # 선인장(중)
    imgTree2_2 = pygame.image.load('images/뛰라노_장애물(중간선인장).png')
    tree2_2_height = imgTree2_2.get_size()[1]
    tree2_2_x = MAX_WIDTH
    tree2_2_y = (MAX_HEIGHT // 2) - tree2_2_height
    # 선인장(대)
    imgTree2_3 = pygame.image.load('images/뛰라노_장애물(큰선인장) (2).png')
    tree2_3_height = imgTree2_3.get_size()[1]
    tree2_3_x = MAX_WIDTH
    tree2_3_y = (MAX_HEIGHT // 2) - tree2_3_height

    #게임 만들기
    while True:
        for event in pygame.event.get():# 이벤트 감지,처리
            # 종료
            if event.type == pygame.QUIT:  # 게임종료확인
                pygame.quit()  # python 종료
                sys.exit()  # 프로그램 종료

            #점프시작 조건
            #공룡1
            elif event.type == pygame.KEYDOWN: #키보드를 눌렀을때(이벤트 처리)
                if event.key == pygame.K_UP:
                    if is_bottom: #만약 공룡이 바닥에 있다면,(바닥에 있을 때만 점프 가능)
                        is_go_up = True # 위로 올라가기 시작
                        is_bottom = False #그래서 바닥에 없음
                # 공룡2
                elif event.key == pygame.K_w:
                    if is_bottom2:  # 만약 공룡이 바닥에 있다면,(바닥에 있을 때만 점프 가능)
                        is_go_up2 = True  # 위로 올라가기 시작
                        is_bottom2 = False  # 그래서 바닥에 없음

        # 배경 그리기
        screen.blit(screen1, (0, 0))
        screen.blit(screen2, (0, MAX_HEIGHT // 2))

        #움직임
        #공룡1
        if is_go_up: #공룡이 점프중이면,
            dino_y -= 30.0 #걷는 거 멈춤
        elif not is_go_up and not is_bottom: #점프 최고점에 도달해서 다시 떨어지는 중이면,
            dino_y += 15.0 #이동하면서 아래로 내려오게 하기
        # 공룡2
        if is_go_up2:  # 공룡이 점프중이면,
            dino2_y -= 30.0  # 걷는 거 멈춤
        elif not is_go_up2 and not is_bottom2:  # 점프 최고점에 도달해서 다시 떨어지는 중이면,
            dino2_y += 15.0  # 이동하면서 아래로 내려오게 하기

        #위치 확인
        #공룡1
        if is_go_up and dino_y <= jump_top:  # end up
            is_go_up = False
        if not is_bottom and dino_y >= dino_bottom:
            is_bottom = True
            dino_y = dino_bottom
        # 공룡2
        if is_go_up2 and dino2_y <= jump_top2:  # end up
            is_go_up2 = False
        if not is_bottom2 and dino2_y >= dino2_bottom:
            is_bottom2 = True
            dino2_y = dino2_bottom

        #나타나기
        #공룡1
        if leg_swap:
            screen.blit(imgDino1_1, (dino_x, dino_y))
            leg_swap = False
        else:
            screen.blit(imgDino1_2, (dino_x, dino_y))
            leg_swap = True
        # 공룡2
        if leg_swap2:
            screen.blit(imgDino2_1, (dino2_x, dino2_y))
            leg_swap2 = False
        else:
            screen.blit(imgDino2_2, (dino2_x, dino2_y))
            leg_swap2 = True


        #screen1 선인장 동작

        #screen2 선인장 동작



        #screen1 선인장 나타나기
        screen.blit(imgTree1_1, (tree1_1_x, tree1_1_y))
        screen.blit(imgTree1_2, (tree1_2_x, tree1_2_y))
        screen.blit(imgTree1_3, (tree1_3_x, tree1_3_y))

        # screen2 선인장 나타나기
        screen.blit(imgTree2_1, (tree2_1_x, tree2_1_y))
        screen.blit(imgTree2_1, (tree2_1_x, tree2_1_y))
        screen.blit(imgTree2_3, (tree2_3_x, tree2_3_y))

        pygame.display.update() #스크린 띄우기
        fps.tick(30) #1초에 30번 돌리기

# 실행하기
if __name__ == "__main__":
    main()