import pygame
import sys

#pygame
pygame.init()

#화면세팅
WIDTH, HEIGHT = 1300, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("dduirano")

#배경 이미지 (서로 다른 이미지로 설정)
screen1 = pygame.image.load("./images/뛰라노_배경(기본하늘).png")  # 위쪽 배경
screen2 = pygame.image.load("./images/뛰라노_배경(바닥).png")       # 아래쪽 배경

#배경 이미지 크기 조절
screen1 = pygame.transform.scale(screen1, (WIDTH, HEIGHT // 2))
screen2 = pygame.transform.scale(screen2, (WIDTH, HEIGHT // 2))

#게임 루프 속도
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get(): #이벤트 감지,처리

        #종료
        if event.type == pygame.QUIT: #게임종료확인
            pygame.quit() #python 종료
            sys.exit()  #프로그램 종료

    screen.blit(screen1, (0, 0))               # 위쪽 배경 그리기
    screen.blit(screen2, (0, HEIGHT // 2))     # 아래쪽 배경 그리기

    pygame.display.flip()
    clock.tick(60)
