import pygame
import random
import time
from control import run
from config import *  # Import configuration settings

class Robot:
    def __init__(robot):
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()

        # Load sound files
        robot.collect_sound = pygame.mixer.Sound("sounds/collect_sound.wav")
        robot.win_sound = pygame.mixer.Sound("sounds/win_sound.wav")

        robot.direction = 'up'
        robot.position = [5, 5]
        robot.robot_x = robot.position[0]
        robot.robot_y = robot.position[1]
        
        # Use config settings
        robot.cell_size = CELL_SIZE
        robot.grid_size = GRID_SIZE
        robot.size = robot.width, robot.height = WINDOW_SIZE, WINDOW_SIZE
        robot.speed = MOVE_SPEED
        
        robot.screen = pygame.display.set_mode(robot.size)
        
        # Load images
        robot.icon_image = pygame.image.load("images/logo.png")
        pygame.display.set_icon(robot.icon_image)

        robot.resource_image = pygame.image.load("images/battery.png")
        robot.resource_image = pygame.transform.scale(robot.resource_image,
                                                    (robot.cell_size, robot.cell_size))
        
        robot.robot_image = pygame.image.load("images/robot.jpg")
        robot.robot_image = pygame.transform.scale(robot.robot_image, 
                                                 (robot.cell_size, robot.cell_size))
        
        # Generate resources using map number from config
        robot.resources = robot.generate_resources()
        
        pygame.display.set_caption("Robot Game - Greenwich Vietnam")

    def draw_grid(robot):
        """Draw a nicer grid with alternating colors"""
        for x in range(robot.grid_size):
            for y in range(robot.grid_size):
                color = GRID_COLOR_1 if (x + y) % 2 == 0 else GRID_COLOR_2
                rect = pygame.Rect(x * robot.cell_size, y * robot.cell_size, 
                                 robot.cell_size, robot.cell_size)
                pygame.draw.rect(robot.screen, color, rect)
                pygame.draw.rect(robot.screen, GRID_LINE_COLOR, rect, 1)

    def generate_resources(robot):
        resources = []
        with open(f"maps/map{MAP_NUMBER}.txt", 'r') as f:
            lines = f.readlines()
            for line in lines:
                x, y = map(int, line.strip().split(','))
                resources.append((x, y))
        return resources

    def check_quit(robot):
        """Check if user wants to quit"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

    def draw_robot(robot, x, y):
        position = (x * robot.cell_size, y * robot.cell_size)
        robot.screen.blit(robot.robot_image, position)

    def draw_resources(robot):
        for resource in robot.resources:
            position = (resource[0] * robot.cell_size,
                       resource[1] * robot.cell_size)
            robot.screen.blit(robot.resource_image, position)

    def go(robot, steps):
        for _ in range(steps):
            robot.check_quit()
            
            if robot.direction == 'up':
                robot.robot_x, robot.robot_y = robot.move_up(robot.robot_x, robot.robot_y)
            elif robot.direction == 'down':
                robot.robot_x, robot.robot_y = robot.move_down(robot.robot_x, robot.robot_y)
            elif robot.direction == 'left':
                robot.robot_x, robot.robot_y = robot.move_left(robot.robot_x, robot.robot_y)
            elif robot.direction == 'right':
                robot.robot_x, robot.robot_y = robot.move_right(robot.robot_x, robot.robot_y)
            
            robot.position[0] = robot.robot_x
            robot.position[1] = robot.robot_y
            
            if (robot.robot_x, robot.robot_y) in robot.resources:
                robot.resources.remove((robot.robot_x, robot.robot_y))
                robot.play_sound(robot.collect_sound)
            
            robot.screen.fill(BACKGROUND_COLOR)
            robot.draw_grid()
            robot.draw_resources()
            robot.draw_robot(robot.robot_x, robot.robot_y)
            pygame.display.flip()
            pygame.event.pump()
            
            time.sleep(robot.speed)

    def turn(robot, direction):
        directions = ['up', 'right', 'down', 'left']
        current_index = directions.index(robot.direction)

        if direction == "left":
            robot.direction = directions[(current_index - 1) % len(directions)]
        elif direction == "right":
            robot.direction = directions[(current_index + 1) % len(directions)]
        elif direction in directions:
            robot.direction = direction

    def move_left(robot, x, y):
        return max(x - 1, 0), y

    def move_right(robot, x, y):
        return min(x + 1, robot.grid_size - 1), y

    def move_up(robot, x, y):
        return x, max(y - 1, 0)

    def move_down(robot, x, y):
        return x, min(y + 1, robot.grid_size - 1)

    def play_sound(robot, sound_file):
        pygame.mixer.Sound.play(sound_file)

    def show_start_button(robot):
        """Display start button and wait for click"""
        font = pygame.font.Font(None, 48)
        button_rect = pygame.Rect((robot.width - BUTTON_WIDTH * 1.5) // 2,
                                 (robot.height - BUTTON_HEIGHT * 1.5) // 2,
                                 BUTTON_WIDTH * 1.5,
                                 BUTTON_HEIGHT * 1.5)
        
        # Draw initial empty map
        robot.screen.fill(BACKGROUND_COLOR)
        robot.draw_grid()
        pygame.display.flip()
        
        while True:
            # Draw button over the map
            # Get mouse position and check hover
            mouse_pos = pygame.mouse.get_pos()
            button_color = BUTTON_HOVER_COLOR if button_rect.collidepoint(mouse_pos) else BUTTON_COLOR
            
            # Draw button
            pygame.draw.rect(robot.screen, button_color, button_rect, border_radius=10)
            text = font.render("Start Game", True, BUTTON_TEXT_COLOR)
            text_rect = text.get_rect(center=button_rect.center)
            robot.screen.blit(text, text_rect)
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_rect.collidepoint(event.pos):
                        return True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return True
            
            # Redraw map (to prevent button trails)
            robot.screen.fill(BACKGROUND_COLOR)
            robot.draw_grid()

    def play(robot):
        # Show empty map with start button
        robot.screen.fill(BACKGROUND_COLOR)
        robot.draw_grid()
        pygame.display.flip()
        
        # Wait for start button click or enter press
        if robot.show_start_button():
            # After start, show full game state
            robot.screen.fill(BACKGROUND_COLOR)
            robot.draw_grid()
            robot.draw_resources()
            robot.draw_robot(robot.robot_x, robot.robot_y)
            pygame.display.flip()
            
            # Start the solution immediately
            try:
                run(robot)
            except Exception as e:
                print(f"Error during run: {e}")
        
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break

            if running:
                robot.screen.fill(BACKGROUND_COLOR)
                robot.draw_grid()
                robot.draw_resources()
                robot.draw_robot(robot.robot_x, robot.robot_y)
                pygame.display.flip()

                if not robot.resources:
                    robot.show_win_screen()
                    running = False

        pygame.quit()

    def show_win_screen(robot):
        """Show winning screen with 'You Win!' image"""
        try:
            win_image = pygame.image.load("images/win.jpg")
            # Scale image to fit 50% of the window (smaller)
            win_size = int(robot.width * 0.5)
            win_image = pygame.transform.scale(win_image, (win_size, win_size))
            win_rect = win_image.get_rect(center=(robot.width // 2, robot.height // 2))
            
            # Create fade effect
            fade_surface = pygame.Surface((robot.width, robot.height))
            fade_surface.fill((0, 0, 0))
            
            # Fade in
            for alpha in range(0, 128, 8):
                robot.screen.fill(BACKGROUND_COLOR)
                robot.draw_grid()
                robot.draw_resources()  # Only draw resources, no robot
                
                fade_surface.set_alpha(alpha)
                robot.screen.blit(fade_surface, (0, 0))
                robot.screen.blit(win_image, win_rect)
                pygame.display.flip()
                pygame.time.delay(50)
            
            robot.play_sound(robot.win_sound)
            pygame.time.wait(int(WIN_DISPLAY_TIME * 1000))
            
        except pygame.error:
            print("Error: 'win.jpg' not found in 'images' directory")

if __name__ == '__main__':
    r = Robot()
    r.play()