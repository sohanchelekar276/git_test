import pygame
import math
import random

pygame.init()

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600
FPS = 60

DARK_BG = (15, 15, 35)
DARKER_BG = (10, 20, 45)
CYAN = (0, 200, 255)
BRIGHT_CYAN = (100, 255, 255)
GRID_COLOR = (40, 100, 150, 40)
PARTICLE_COLOR = (0, 200, 255)
BALL_COLOR = (255, 80, 80)
OBSTACLE_COLOR = (200, 80, 255)
BATTERY_GREEN = (50, 255, 100)
BATTERY_YELLOW = (255, 220, 0)
BATTERY_RED = (255, 60, 60)
WALL_COLOR = (120, 60, 180)


class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-3, 3)
        self.life = 1.0
        self.color = color
        self.size = random.uniform(2, 5)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 0.02
        self.vx *= 0.96
        self.vy *= 0.96

    def draw(self, screen):
        if self.life > 0:
            alpha = int(255 * self.life)
            color_with_alpha = (self.color[0], self.color[1], self.color[2], alpha)
            s = pygame.Surface((int(self.size * 3), int(self.size * 3)), pygame.SRCALPHA)
            pygame.draw.circle(s, color_with_alpha,
                               (int(self.size * 1.5), int(self.size * 1.5)), int(self.size))
            screen.blit(s, (int(self.x - self.size * 1.5), int(self.y - self.size * 1.5)))


class Trail:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.life = 1.0

    def update(self):
        self.life -= 0.1

    def draw(self, screen):
        if self.life > 0:
            alpha = int(120 * self.life)
            size = int(10 * self.life)
            s = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            trail_color = (CYAN[0], CYAN[1], CYAN[2], alpha)
            pygame.draw.circle(s, trail_color, (size, size), size)
            screen.blit(s, (int(self.x - size), int(self.y - size)))


class Obstacle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.glow_phase = random.uniform(0, math.pi * 2)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen):
        self.glow_phase += 0.05
        glow_intensity = int(60 + 40 * math.sin(self.glow_phase))

        glow_size = 8
        glow_surface = pygame.Surface((self.width + glow_size * 2, self.height + glow_size * 2), pygame.SRCALPHA)
        glow_color = (WALL_COLOR[0], WALL_COLOR[1], WALL_COLOR[2], glow_intensity)
        pygame.draw.rect(glow_surface, glow_color, glow_surface.get_rect(), border_radius=8)
        screen.blit(glow_surface, (self.x - glow_size, self.y - glow_size))

        rect = self.get_rect()
        pygame.draw.rect(screen, WALL_COLOR, rect, border_radius=6)

        inner_rect = pygame.Rect(rect.x + 3, rect.y + 3, rect.width - 6, rect.height - 6)
        if inner_rect.width > 0 and inner_rect.height > 0:
            inner_surface = pygame.Surface((inner_rect.width, inner_rect.height), pygame.SRCALPHA)
            inner_color = (200, 140, 255, 40)
            pygame.draw.rect(inner_surface, inner_color, inner_surface.get_rect(), border_radius=4)
            screen.blit(inner_surface, (inner_rect.x, inner_rect.y))

        pygame.draw.rect(screen, (180, 140, 220), rect, 2, border_radius=6)


class MazeMap:
    @staticmethod
    def get_map_1():
        return {
            'name': 'Simple Corridor',
            'dog_start': (60, 300),
            'ball_pos': (940, 300),
            'walls': [
                Obstacle(0, 0, WINDOW_WIDTH, 40),
                Obstacle(0, WINDOW_HEIGHT - 40, WINDOW_WIDTH, 40),
                Obstacle(200, 40, 30, 200),
                Obstacle(200, 360, 30, 200),
                Obstacle(400, 160, 30, 200),
                Obstacle(400, 40, 30, 120),
                Obstacle(600, 240, 30, 200),
                Obstacle(600, 40, 30, 160),
                Obstacle(800, 160, 30, 200),
                Obstacle(800, 40, 30, 80),
            ]
        }

    @staticmethod
    def get_map_2():
        return {
            'name': 'Zigzag Challenge',
            'dog_start': (60, 80),
            'ball_pos': (940, 520),
            'walls': [
                Obstacle(0, 0, WINDOW_WIDTH, 40),
                Obstacle(0, WINDOW_HEIGHT - 40, WINDOW_WIDTH, 40),
                Obstacle(150, 40, 30, 200),
                Obstacle(150, 360, 30, 200),
                Obstacle(300, 160, 30, 200),
                Obstacle(300, 40, 30, 120),
                Obstacle(450, 240, 30, 200),
                Obstacle(450, 40, 30, 200),
                Obstacle(600, 160, 30, 200),
                Obstacle(600, 360, 30, 200),
                Obstacle(750, 240, 30, 200),
                Obstacle(750, 40, 30, 200),
            ]
        }

    @staticmethod
    def get_map_3():
        return {
            'name': 'Room Navigator',
            'dog_start': (60, 520),
            'ball_pos': (940, 80),
            'walls': [
                Obstacle(0, 0, WINDOW_WIDTH, 40),
                Obstacle(0, WINDOW_HEIGHT - 40, WINDOW_WIDTH, 40),
                Obstacle(150, 40, 30, 250),
                Obstacle(150, 350, 30, 210),
                Obstacle(180, 260, 170, 30),
                Obstacle(380, 40, 30, 200),
                Obstacle(380, 300, 30, 260),
                Obstacle(410, 270, 140, 30),
                Obstacle(580, 40, 30, 280),
                Obstacle(580, 380, 30, 180),
                Obstacle(610, 350, 150, 30),
                Obstacle(790, 40, 30, 250),
                Obstacle(790, 350, 30, 210),
                Obstacle(820, 320, 150, 30),
            ]
        }


class RoboticDogSimulation:
    def __init__(self, dog_instance, map_num=1):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Robotic Dog Maze Navigator - IITB Assignment")
        self.clock = pygame.time.Clock()
        self.running = True
        self.paused = False
        self.battery_dead = False

        self.current_map_num = map_num
        self.load_map(map_num)

        self.dog = dog_instance
        self.dog.x = self.dog_start[0]
        self.dog.y = self.dog_start[1]
        self.dog.target_x = self.dog_start[0]
        self.dog.target_y = self.dog_start[1]

        self.ball = {
            'x': self.ball_pos[0],
            'y': self.ball_pos[1],
            'radius': 15,
            'collected': False,
            'pulse': 0
        }

        self.particles = []
        self.trails = []
        self.leg_phase = 0
        self.score = 0
        self.start_time = pygame.time.get_ticks()

        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)

    def load_map(self, map_num):
        if map_num == 1:
            map_data = MazeMap.get_map_1()
        elif map_num == 2:
            map_data = MazeMap.get_map_2()
        elif map_num == 3:
            map_data = MazeMap.get_map_3()
        else:
            map_data = MazeMap.get_map_1()

        self.map_name = map_data['name']
        self.dog_start = map_data['dog_start']
        self.ball_pos = map_data['ball_pos']
        self.obstacles = map_data['walls']

    def create_particles(self, x, y, count, color):
        for _ in range(count):
            self.particles.append(Particle(x, y, color))

    def draw_background(self):
        for y in range(WINDOW_HEIGHT):
            ratio = y / WINDOW_HEIGHT
            color = (
                int(DARK_BG[0] + (DARKER_BG[0] - DARK_BG[0]) * ratio),
                int(DARK_BG[1] + (DARKER_BG[1] - DARK_BG[1]) * ratio),
                int(DARK_BG[2] + (DARKER_BG[2] - DARK_BG[2]) * ratio)
            )
            pygame.draw.line(self.screen, color, (0, y), (WINDOW_WIDTH, y))

        grid_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        for i in range(0, WINDOW_WIDTH, 40):
            pygame.draw.line(grid_surface, GRID_COLOR, (i, 0), (i, WINDOW_HEIGHT), 1)
        for i in range(0, WINDOW_HEIGHT, 40):
            pygame.draw.line(grid_surface, GRID_COLOR, (0, i), (WINDOW_WIDTH, i), 1)
        self.screen.blit(grid_surface, (0, 0))

    def draw_dog(self):
        if not self.battery_dead:
            self.dog.velocity_x += (self.dog.target_x - self.dog.x) * 0.02
            self.dog.velocity_y += (self.dog.target_y - self.dog.y) * 0.02
            self.dog.velocity_x *= 0.88
            self.dog.velocity_y *= 0.88

            self.dog.x += self.dog.velocity_x
            self.dog.y += self.dog.velocity_y

            if not self.paused and abs(self.dog.velocity_x) + abs(self.dog.velocity_y) > 0.5:
                self.trails.append(Trail(self.dog.x, self.dog.y))
                if len(self.trails) > 15:
                    self.trails.pop(0)

            self.leg_phase += 0.2

        for trail in self.trails:
            trail.update()
            trail.draw(self.screen)

        glow_alpha = 70 if not self.battery_dead else 25
        for layer in range(2):
            size = 50 - layer * 15
            alpha = glow_alpha - layer * 25
            glow_surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            glow_color = (CYAN[0], CYAN[1], CYAN[2], alpha)
            pygame.draw.circle(glow_surface, glow_color, (size, size), size)
            self.screen.blit(glow_surface, (int(self.dog.x - size), int(self.dog.y - size)))

        body_color = CYAN if not self.battery_dead else (40, 80, 120)

        pygame.draw.ellipse(self.screen, body_color,
                            (int(self.dog.x - 30), int(self.dog.y - 15), 60, 30))

        pygame.draw.circle(self.screen, body_color, (int(self.dog.x + 25), int(self.dog.y)), 18)

        if not self.battery_dead:
            eye_glow = pygame.Surface((20, 20), pygame.SRCALPHA)
            pygame.draw.circle(eye_glow, (BRIGHT_CYAN[0], BRIGHT_CYAN[1], BRIGHT_CYAN[2], 150), (10, 10), 10)
            self.screen.blit(eye_glow, (int(self.dog.x + 15), int(self.dog.y - 10)))
            pygame.draw.circle(self.screen, (255, 255, 255), (int(self.dog.x + 28), int(self.dog.y - 5)), 4)
            pygame.draw.circle(self.screen, (255, 255, 255), (int(self.dog.x + 28), int(self.dog.y + 5)), 4)
        else:
            pygame.draw.circle(self.screen, (80, 80, 80), (int(self.dog.x + 28), int(self.dog.y - 5)), 4)
            pygame.draw.circle(self.screen, (80, 80, 80), (int(self.dog.x + 28), int(self.dog.y + 5)), 4)

        leg_positions = [
            (self.dog.x - 18, self.dog.y + 10),
            (self.dog.x - 6, self.dog.y + 10),
            (self.dog.x + 6, self.dog.y + 10),
            (self.dog.x + 18, self.dog.y + 10)
        ]

        for i, (lx, ly) in enumerate(leg_positions):
            offset = math.sin(self.leg_phase + i * math.pi / 2) * 6 if not self.battery_dead else 0
            pygame.draw.line(self.screen, body_color, (lx, ly), (lx, ly + 15 + offset), 5)
            leg_joint_color = BRIGHT_CYAN if not self.battery_dead else (60, 60, 60)
            pygame.draw.circle(self.screen, leg_joint_color, (int(lx), int(ly + 15 + offset)), 3)

    def draw_ball(self):
        if not self.ball['collected']:
            self.ball['pulse'] += 0.12
            pulse_scale = 1 + 0.2 * math.sin(self.ball['pulse'])

            glow_size = int(40 * pulse_scale)
            glow_surface = pygame.Surface((glow_size * 2, glow_size * 2), pygame.SRCALPHA)
            ball_glow_color = (BALL_COLOR[0], BALL_COLOR[1], BALL_COLOR[2], 100)
            pygame.draw.circle(glow_surface, ball_glow_color, (glow_size, glow_size), glow_size)
            self.screen.blit(glow_surface, (int(self.ball['x'] - glow_size), int(self.ball['y'] - glow_size)))

            ball_radius = int(self.ball['radius'] * pulse_scale)
            pygame.draw.circle(self.screen, BALL_COLOR,
                               (int(self.ball['x']), int(self.ball['y'])), ball_radius)

            pygame.draw.circle(self.screen, (255, 255, 255),
                               (int(self.ball['x'] - 5), int(self.ball['y'] - 5)), 5)

    def draw_obstacles(self):
        for obstacle in self.obstacles:
            obstacle.draw(self.screen)

    def draw_ui(self):
        title = self.font_medium.render(f"Maze {self.current_map_num}: {self.map_name}", True, BRIGHT_CYAN)
        self.screen.blit(title, (20, 20))

        if not self.ball['collected']:
            elapsed = (pygame.time.get_ticks() - self.start_time) // 1000
            time_text = self.font_small.render(f"Time: {elapsed}s", True, CYAN)
            self.screen.blit(time_text, (20, 60))

        battery_color = BATTERY_GREEN
        if self.dog.battery_level < 50:
            battery_color = BATTERY_YELLOW
        if self.dog.battery_level < 20:
            battery_color = BATTERY_RED

        battery_text = self.font_small.render(f"Battery: {int(self.dog.battery_level)}%", True, battery_color)
        self.screen.blit(battery_text, (20, 90))

        pygame.draw.rect(self.screen, (30, 30, 30), (20, 120, 180, 22), border_radius=4)
        battery_width = int(176 * self.dog.battery_level / 100)
        if battery_width > 0:
            pygame.draw.rect(self.screen, battery_color, (22, 122, battery_width, 18), border_radius=3)
        pygame.draw.rect(self.screen, CYAN, (20, 120, 180, 22), 2, border_radius=4)

        if not self.ball['collected']:
            dx = self.ball['x'] - self.dog.x
            dy = self.ball['y'] - self.dog.y
            distance = math.sqrt(dx * dx + dy * dy)
            dist_text = self.font_small.render(f"Distance: {int(distance)}px", True, CYAN)
            self.screen.blit(dist_text, (20, 155))

        instructions = [
            "Controls:",
            "SPACE - Pause",
            "1/2/3 - Switch Map",
            "R - Reset",
            "C - Recharge",
            "ESC - Quit"
        ]

        box_x = WINDOW_WIDTH - 240
        box_y = 20
        box_surface = pygame.Surface((220, 200), pygame.SRCALPHA)
        pygame.draw.rect(box_surface, (20, 20, 40, 180), box_surface.get_rect(), border_radius=8)
        pygame.draw.rect(box_surface, CYAN, box_surface.get_rect(), 2, border_radius=8)
        self.screen.blit(box_surface, (box_x, box_y))

        for i, instruction in enumerate(instructions):
            color = BRIGHT_CYAN if i == 0 else (180, 180, 180)
            text = self.font_small.render(instruction, True, color)
            self.screen.blit(text, (box_x + 15, box_y + 15 + i * 30))

        if self.battery_dead:
            warning_text = self.font_large.render("BATTERY DEPLETED!", True, BATTERY_RED)
            text_rect = warning_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 30))

            s = pygame.Surface((text_rect.width + 60, text_rect.height + 80), pygame.SRCALPHA)
            pygame.draw.rect(s, (0, 0, 0, 230), s.get_rect(), border_radius=15)
            pygame.draw.rect(s, BATTERY_RED, s.get_rect(), 3, border_radius=15)
            self.screen.blit(s, (text_rect.x - 30, text_rect.y - 25))

            self.screen.blit(warning_text, text_rect)

            prompt = self.font_small.render("Press C to recharge", True, BRIGHT_CYAN)
            prompt_rect = prompt.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 25))
            self.screen.blit(prompt, prompt_rect)

        if self.ball['collected']:
            elapsed = (pygame.time.get_ticks() - self.start_time) // 1000
            success_text = self.font_large.render("BALL COLLECTED!", True, BATTERY_GREEN)
            text_rect = success_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 40))

            s = pygame.Surface((text_rect.width + 60, text_rect.height + 100), pygame.SRCALPHA)
            pygame.draw.rect(s, (0, 0, 0, 230), s.get_rect(), border_radius=15)
            pygame.draw.rect(s, BATTERY_GREEN, s.get_rect(), 3, border_radius=15)
            self.screen.blit(s, (text_rect.x - 30, text_rect.y - 30))

            self.screen.blit(success_text, text_rect)

            time_text = self.font_medium.render(f"Time: {elapsed}s", True, BRIGHT_CYAN)
            time_rect = time_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 10))
            self.screen.blit(time_text, time_rect)

            prompt = self.font_small.render("Press R to reset or 1/2/3 to change map", True, (200, 200, 200))
            prompt_rect = prompt.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 45))
            self.screen.blit(prompt, prompt_rect)

        if self.paused and not self.battery_dead and not self.ball['collected']:
            pause_text = self.font_large.render("PAUSED", True, BRIGHT_CYAN)
            text_rect = pause_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))

            s = pygame.Surface((text_rect.width + 50, text_rect.height + 30), pygame.SRCALPHA)
            pygame.draw.rect(s, (0, 0, 0, 220), s.get_rect(), border_radius=12)
            pygame.draw.rect(s, BRIGHT_CYAN, s.get_rect(), 3, border_radius=12)
            self.screen.blit(s, (text_rect.x - 25, text_rect.y - 15))

            self.screen.blit(pause_text, text_rect)

    def check_ball_collection(self):
        if not self.ball['collected'] and not self.battery_dead:
            dx = self.ball['x'] - self.dog.x
            dy = self.ball['y'] - self.dog.y
            distance = math.sqrt(dx * dx + dy * dy)

            if distance < 30:
                self.ball['collected'] = True
                self.create_particles(self.ball['x'], self.ball['y'], 40, BALL_COLOR)
                elapsed = (pygame.time.get_ticks() - self.start_time) // 1000
                print(f"Ball collected in {elapsed} seconds!")

    def reset_simulation(self):
        self.dog.x = self.dog_start[0]
        self.dog.y = self.dog_start[1]
        self.dog.target_x = self.dog_start[0]
        self.dog.target_y = self.dog_start[1]
        self.dog.velocity_x = 0
        self.dog.velocity_y = 0
        self.ball['x'] = self.ball_pos[0]
        self.ball['y'] = self.ball_pos[1]
        self.ball['collected'] = False
        self.trails = []
        self.start_time = pygame.time.get_ticks()
        print(f"Maze {self.current_map_num} reset!")

    def switch_map(self, map_num):
        self.current_map_num = map_num
        self.load_map(map_num)
        self.dog.x = self.dog_start[0]
        self.dog.y = self.dog_start[1]
        self.dog.target_x = self.dog_start[0]
        self.dog.target_y = self.dog_start[1]
        self.dog.velocity_x = 0
        self.dog.velocity_y = 0
        self.dog.battery_level = 100
        self.battery_dead = False
        self.ball['x'] = self.ball_pos[0]
        self.ball['y'] = self.ball_pos[1]
        self.ball['collected'] = False
        self.trails = []
        self.start_time = pygame.time.get_ticks()
        print(f"Switched to Maze {map_num}: {self.map_name}")

    def update(self):
        if not self.paused and not self.battery_dead and not self.ball['collected']:
            self.dog.find_ball((self.ball['x'], self.ball['y']), self.obstacles)

            self.dog.battery_level -= 0.04
            if self.dog.battery_level <= 0:
                self.dog.battery_level = 0
                self.battery_dead = True
                self.create_particles(self.dog.x, self.dog.y, 25, BATTERY_RED)
                print("Battery depleted! Dog has stopped.")

            self.dog.target_x = max(30, min(WINDOW_WIDTH - 30, self.dog.target_x))
            self.dog.target_y = max(50, min(WINDOW_HEIGHT - 50, self.dog.target_y))

            self.check_ball_collection()

        self.particles = [p for p in self.particles if p.life > 0]
        for particle in self.particles:
            particle.update()

    def draw(self):
        self.draw_background()
        self.draw_obstacles()
        self.draw_ball()
        self.draw_dog()

        for particle in self.particles:
            particle.draw(self.screen)

        self.draw_ui()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    if not self.battery_dead and not self.ball['collected']:
                        self.paused = not self.paused
                elif event.key == pygame.K_r:
                    self.reset_simulation()
                elif event.key == pygame.K_c:
                    self.dog.recharge()
                    self.battery_dead = False
                    self.create_particles(self.dog.x, self.dog.y, 30, BATTERY_GREEN)
                    print("Battery recharged!")
                elif event.key == pygame.K_1:
                    self.switch_map(1)
                elif event.key == pygame.K_2:
                    self.switch_map(2)
                elif event.key == pygame.K_3:
                    self.switch_map(3)

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()


def main():
    try:
        from robotic_dog import RoboticDog, Leg, Sensor

        my_dog = RoboticDog("Spot")

        my_dog.add_leg(Leg(1, "front-left"))
        my_dog.add_leg(Leg(2, "front-right"))
        my_dog.add_leg(Leg(3, "back-left"))
        my_dog.add_leg(Leg(4, "back-right"))

        my_dog.add_sensor(Sensor("ultrasonic"))
        my_dog.add_sensor(Sensor("IMU"))

        my_dog.check_status()

        sim = RoboticDogSimulation(my_dog, map_num=1)
        print("\n=== Robotic Dog Maze Navigator ===")
        print("Your task: Implement pathfinding logic in the find_ball() method")
        print("Press 1, 2, or 3 to switch between mazes")
        print("Press SPACE to pause, R to reset, C to recharge")
        print("==========================================\n")
        sim.run()

    except ImportError as e:
        print("=" * 60)
        print("ERROR: Could not import robotic_dog.py")
        print("=" * 60)
        print(f"Details: {e}")x
        print("\nMake sure you have created 'robotic_dog.py' in the same directory")
        print("with your RoboticDog, Leg, and Sensor class implementations.")
        print("=" * 60)
    except Exception as e:
        print("=" * 60)
        print("ERROR: An error occurred while running the simulation")
        print("=" * 60)
        print(f"Details: {e}")
        print("=" * 60)


if __name__ == "__main__":
    main()
