# Knee Ga Clock by SSL-ACTX
# Not gonna lie, this is brain-wracking. I saved some time by using formulas online.
# Even chatbots can't even help me. Lol.

import pygame
import math
import datetime
import os

pygame.init()
screen_width, screen_height = 600, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Knee Ga Clock")

clock = pygame.time.Clock()
num_hands = 3  # minute, second, and hour hands :)
num_seconds = 60
center_x, center_y = screen_width // 2, screen_height // 2
radius = 200
font = pygame.font.Font(None, 24)
start_angle = -math.pi / 2.1  # start angle - important part! (12 o'clock)

# load the momoi nword frames named "frame_xx_delay-0.1s.gif"
image_folder = "./momoi/"
image_files = [f for f in sorted(os.listdir(image_folder)) if f.startswith(
    "frame_") and f.endswith(".gif")]
images = [pygame.image.load(os.path.join(
    image_folder, img)).convert_alpha() for img in image_files]

running = True
hand_positions = [0] * num_hands
show_lines = False


def calculate_angle(pos, num_parts):
    return (pos / num_parts) * 2 * math.pi + start_angle


frame_index = 0
frame_delay = 40  # the speed our momoi nword images are played
last_frame_time = pygame.time.get_ticks()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    current_time = datetime.datetime.now()
    # subtracts 1 second coz it always advance by 2s
    second = (current_time.second - 1) % 60
    # subtracts 1 min as it's always  advanced by 1min
    minute = (current_time.minute - 1) % 60
    hour = (current_time.hour - 1) % 12  # same case lol

    # hand updater
    hand_positions[0] = minute
    hand_positions[1] = second
    hand_positions[2] = hour

    screen.fill((255, 255, 255))
    pygame.draw.circle(screen, (0, 0, 0), (center_x, center_y), radius, 2)

    # the black circle -- lol
    pygame.draw.circle(screen, (0, 0, 0), (center_x, center_y), 10)

    title_text = font.render("Knee Ga Clock - Seuriin", True, (0, 0, 0))
    title_rect = title_text.get_rect(
        center=(center_x, 40))
    screen.blit(title_text, title_rect)

    # draw the hands - reducing their length to resemble clock's hands
    for i, pos in enumerate(hand_positions):
        angle = calculate_angle(pos, num_seconds)
        if i == 0:  # minute hand
            hand_length = radius * 0.6
        elif i == 1:  # second hand
            hand_length = radius * 0.8
        else:  # hour hand
            hand_length = radius * 0.5

        hand_x = center_x + int(hand_length * math.cos(angle))
        hand_y = center_y + int(hand_length * math.sin(angle))

        if show_lines:
            pygame.draw.line(screen, (0, 0, 0), (center_x,
                             center_y), (hand_x, hand_y), 3)

        # the important formatting of num in the clock's hands
        current_second_str = str(pos + 1)
        text_width, text_height = font.size(current_second_str)
        num_repetitions = int(hand_length / text_width)

        # this positions numbers around the circle from the top position --hard asf
        for j in range(num_repetitions):
            x = center_x + \
                int((hand_length * j / num_repetitions) * math.cos(angle))
            y = center_y + \
                int((hand_length * j / num_repetitions) * math.sin(angle))
            text = font.render(current_second_str, True, (0, 0, 0))
            text_rect = text.get_rect(center=(x, y))
            screen.blit(text, text_rect)

    # current datetime -- below the clock sht
    hour_display = current_time.strftime(
        "%I:%M:%S %p")  # am/pm
    datetime_text = font.render(hour_display, True, (0, 0, 0))
    datetime_rect = datetime_text.get_rect(
        center=(center_x, center_y + radius + 20))
    screen.blit(datetime_text, datetime_rect)

    # animation frame update
    current_time = pygame.time.get_ticks()
    if current_time - last_frame_time > frame_delay:
        frame_index = (frame_index + 1) % len(images)
        last_frame_time = current_time

    # momoi nword
    img = pygame.transform.scale(
        images[frame_index], (150, 150))
    img_rect = img.get_rect(bottomright=(
        screen_width - 10, screen_height - 10))
    screen.blit(img, img_rect)

    # useless/optional key handling for line - pressing L
    keys = pygame.key.get_pressed()
    if keys[pygame.K_l]:
        show_lines = not show_lines

    pygame.display.flip()
    clock.tick(10)

pygame.quit()
