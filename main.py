import random
import time

from data import *
import pygame
import sys

# We create three arrays, one for the spanish words, another for the english words, and another for visited
# we also create integer arrays for the words
# we need to keep track of the score
# we start off with two random words (add them to visited) and keep note of what index/position those words are
# we access the integer arrays (monthly searches) using the index
# when button higher or lower is pressed, we compute and check
# if correct, add point, wait a bit, get rid of the left word (add to visited) and move the right word to the left
# use randomizer and check condition to see if next word has already been visited
# if all words have been visited, make all unvisited and make the left word visited before getting a new word for the right side

# if incorrect, end game, go to final screen display score, and choose play again button

pygame.init()

# set the size for the surface (screen)
# MUST BE PLAYED ON 1000 x 800
screen = pygame.display.set_mode((1800, 900), 0)
# set the caption for the screen
pygame.display.set_caption("Higher Lower")
# define colours you will be using
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (153, 204, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
loop = True
intro = True
game = True
final = True
high_score = 0


def findrandom(visited):
    while True:
        newint = random.randint(0, 19)
        if visited[newint - 1] is False:
            break
    visited[newint - 1] = True
    return newint - 1


def checkiffilled(visited):
    a = False  # false = all are visited, true = unvisited
    for i in range(19):
        if visited[i] is False:
            a = True
            break
    if a is False:
        visited[:] = [False] * 19
    return findrandom(visited)


#CREATE A RULES STAGE

while loop:
    screen_W = screen.get_width()
    screen_H = screen.get_height()
    while intro:
        pos = pygame.mouse.get_pos()
        screen.fill(WHITE)
        imagelogo = pygame.image.load("../HigherLower/images/higherorlower.png")
        font_title = pygame.font.SysFont("arial bold", 80)
        title_text = font_title.render("Higher Lower", True, BLACK)

        font_title = pygame.font.SysFont("arial bold", 60)
        play_text = font_title.render("Play game", True, BLACK)

        logo_image = imagelogo.get_rect()
        logo_image.center = (screen_W / 2, screen_H / 2.8)
        screen.blit(imagelogo, logo_image)

        textRect2 = title_text.get_rect()
        textRect2.center = (screen_W / 1.83, screen_H - screen_H / 3)
        screen.blit(play_text, textRect2)

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False
                intro = False
                game = False
                final = False
            if event.type == pygame.MOUSEBUTTONUP:
                if textRect2.collidepoint(pos):
                    intro = False

    new_word = True
    new_game = True
    left = 0
    right = 0
    score = 0
    display_buttons = True
    correct = False
    wrong = False
    pause = False

    while game:
        pos = pygame.mouse.get_pos()
        screen.fill(WHITE)
        font_text = pygame.font.SysFont("arial", 40)
        font_buttons = pygame.font.SysFont("arial", 23)
        font_score = pygame.font.SysFont("arial", 18)
        Higher = font_buttons.render("Más", True, BLACK)
        Lower = font_buttons.render("Menos", True, BLACK)
        score_display = font_score.render(str(score), True, BLACK)
        score_current = font_score.render("Score: ", True, BLACK)
        highscore_display = font_score.render(str(high_score), True, BLACK)
        highscore = font_score.render("Highscore: ", True, BLACK)

        if score > high_score:
            high_score = score

        imagecorrect = pygame.image.load("../HigherLower/images/correct.png")
        image_correct = imagecorrect.get_rect()
        image_correct.center = (screen_W / 2, screen_H / 2.8)

        imagewrong = pygame.image.load("../HigherLower/images/wrong.png")
        image_wrong = imagewrong.get_rect()
        image_wrong.center = (screen_W / 2, screen_H / 2.8)

        if pause is True:
            pygame.time.wait(1000)
            pause = False
            if wrong is True:
                loop = False
                game = False
        if correct is True:
            screen.blit(imagecorrect, image_correct)
            pause = True
            correct = False
        elif wrong is True:
            screen.blit(imagewrong, image_wrong)
            pause = True



        #make the higher/lower.get_rect actually the button and not the text

        pygame.draw.line(screen, BLACK, (screen_W / 2, 0), (screen_W / 2, screen_H - 30), 5)
        Button1 = Higher.get_rect()
        Button2 = Lower.get_rect()
        screen_click = screen.get_rect()
        if display_buttons is True:
            pygame.draw.rect(screen, GREEN, (1250, 350, 250, 80))
            pygame.draw.rect(screen, RED, (1250, 480, 250, 80))
            Button1.center = (screen_W / 1.3, screen_H - screen_H / 1.77)
            screen.blit(Higher, Button1)

            Button2.center = (screen_W / 1.3, screen_H - screen_H / 2.35)
            screen.blit(Lower, Button2)

        if new_word is True:
            left = right
            if new_game is True:
                left = checkiffilled(visited)
                new_game = False

            right = checkiffilled(visited)
            new_word = False

        left_text = font_text.render(spanish[left], True, BLACK)
        left_english = font_text.render(english[left], True, BLACK)
        left_score = font_text.render(searches[left] + " búsquedas (mensual)", True, BLACK)

        left_word = left_text.get_rect()
        left_word.center = (screen_W / 4, screen_H - screen_H / 1.3)
        screen.blit(left_text, left_word)

        left_english_text = left_english.get_rect()
        left_english_text.center = (screen_W / 4, screen_H - screen_H / 1.5)
        screen.blit(left_english, left_english_text)

        left_searches = left_score.get_rect()
        left_searches.center = (screen_W / 4, screen_H - screen_H / 1.8)
        screen.blit(left_score, left_searches)

        right_text = font_text.render(spanish[right], True, BLACK)

        right_word = right_text.get_rect()
        right_word.center = (screen_W / 1.3, screen_H - screen_H / 1.3)
        screen.blit(right_text, right_word)

        score_text = score_current.get_rect()
        score_text.center = (screen_W / 1.1, screen_H - screen_H / 15)
        screen.blit(score_current, score_text)

        score_number = score_display.get_rect()
        score_number.center = (screen_W / 1.07, screen_H - screen_H / 15)
        screen.blit(score_display, score_number)

        highscore_text = highscore_display.get_rect()
        highscore_text.center = (screen_W / 1.2, screen_H - screen_H / 15)
        screen.blit(highscore_display, highscore_text)

        highscore_number = highscore.get_rect()
        highscore_number.center = (screen_W / 1.25, screen_H - screen_H / 15)
        screen.blit(highscore, highscore_number)



        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False
                intro = False
                game = False
                final = False
            if event.type == pygame.MOUSEBUTTONUP:

                if Button1.collidepoint(pos):  # higher
                    if searches[right] >= searches[left]:
                        correct = True
                        score += 1
                        display_buttons = False
                        new_word = True
                    else:
                        wrong = True


                elif Button2.collidepoint(pos):  # lower
                    if searches[right] <= searches[left]:
                        correct = True
                        score += 1
                        display_buttons = False
                        new_word = True
                    else:
                        wrong = True



pygame.quit()
sys.exit()
