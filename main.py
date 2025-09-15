import pygame
import math
pygame.init()

WIDTH, HEIGHT = 900, 900
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Planet Sim")

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARK_GREY = (80, 78, 81)
ORANGE = (255, 165, 0)
LIGHT_BLUE = (173, 216, 230)
LIGHT_BLUE2 = (0, 191, 255)
LIGHT_YELLOW = (255, 255, 224)

FONT = pygame.font.SysFont("comicsans", 16)
def log_scale(x, y, center_x, center_y, min_radius=40, max_radius=(WIDTH //2) - 40):
    """
    maps (x, y) to screen coordinates using a logarithmic scale.
    min_radius: minimum distance from center (for mercury)
    max_radius: maximum distance from center (for neptune)
    """
    r = math.sqrt(x**2 + y**2)
    if r ==0 :
        return center_x, center_y
    log_r = math.log10(r +1)
    max_r = 30.07 * Planet.AU
    max_log_r = math.log10(max_r +1)
    scaled_r = min_radius + (log_r / max_log_r) * (max_radius - min_radius)
    theta = math.atan2(y, x)
    screen_x = center_x + scaled_r * math.cos(theta)
    screen_y = center_y + scaled_r * math.sin(theta)
    return screen_x, screen_y

    
class Planet:
    AU = (149.6e6 * 1000) #AU is astronomical unit, aka. distance from earth to sun
    G = 6.67428e-11 #gravitational constant, aka the force of attraction
    SCALE = 250 / AU #1AU = 100 pixels
    TIMESTEP = 3600*24 #seconds per hour multiplied by 24 hours in a day 

    def __init__(self, x, y, radius, color, mass, name=""):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        self.name = name

        self.sun = False #dont want to draw the orbit of the sun cause yeah..
        self.distance_to_sun = 0
        self.orbit = []

        self.x_vel = 0
        self.y_vel = 0


    def draw(self, win): 
        angle = math.atan2(self.y, self.x)
        x = WIDTH / 2 + self.display_radius * math.cos(angle)
        y = HEIGHT / 2 + self.display_radius * math.sin(angle)

        if not self.sun:
            pygame.draw.circle(win, (80, 80, 80), (WIDTH // 2, HEIGHT // 2), self.display_radius, 1)

        pygame.draw.circle(win, self.color, (int(x), int(y)), self.radius)
        if not self.sun:
            name_text = FONT.render(self.name, 1, WHITE)
            name_x = x - name_text.get_width() / 2
            name_y = y + self.radius + 4
            win.blit(name_text, (name_x, name_y))

            distance_text = FONT.render(f"{round(self.distance_to_sun/1000, 1)} km", 1, WHITE)
            padding = 6
            card_width = distance_text.get_width() + 2 * padding
            card_height = distance_text.get_height() + 2 * padding
            card_x = x - card_width / 2
            card_y = y - self.radius - card_height - 8  

            pygame.draw.rect(win, (40, 40, 40), (card_x, card_y, card_width, card_height), border_radius=6)
            pygame.draw.rect(win, (120, 120, 120), (card_x, card_y, card_width, card_height), 2, border_radius=6)
            win.blit(distance_text, (card_x + padding, card_y + padding))
    
    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x**2 + distance_y**2)

        if other.sun: 
            self.distance_to_sun = distance
        
        force = self.G * self.mass * other.mass / distance**2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta)* force
        force_y = math.sin(theta)* force
        return force_x, force_y
    
    def update_position(self, planets):
        if self.sun:
            return
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue

            fx, fy = self.attraction(planet)
            total_fx = total_fx + fx
            total_fy = total_fy + fy

        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP

        self.orbit.append((self.x, self.y))


def main():
    run = True
    clock = pygame.time.Clock()#this just sets the max framerate per second

    display_radii = [60,100, 140, 180, 220, 270, 320, 370, 420] 

    sun = Planet(0, 0, 30, YELLOW, 1.98992 * 10**30, "Sun")
    sun.sun = True
    sun.display_radius = 0

    earth = Planet(-1 * Planet.AU, 0, 16, BLUE, 5.9741 * 10**24, "Earth")
    earth.y_vel = 29.783 * 1000 
    earth.display_radius = display_radii[2]

    mars = Planet(-1.524 * Planet.AU, 0, 12, RED, 6.39 * 10**23, "Mars")
    mars.y_vel = 24.077 * 1000
    mars.display_radius = display_radii[2]

    mercury = Planet(0.387 * Planet.AU, 0, 8, DARK_GREY, 3.30 * 10**23, "Mercury")
    mercury.y_vel = 47.4 * 1000
    mercury.display_radius = display_radii[0]

    venus = Planet(0.723 * Planet.AU, 0, 14, WHITE , 4.8685 * 10**24, "Venus")
    venus.y_vel = -35.02 * 1000
    venus.display_radius = display_radii[1]

    jupiter = Planet(5.208 * Planet.AU, 0, 20, ORANGE, 1.898 * 10**27, "Jupiter")
    jupiter.y_vel = 13.07 * 1000
    jupiter.display_radius = display_radii[4]

    saturn = Planet(9.537 * Planet.AU, 0, 18, LIGHT_YELLOW, 5.683 * 10**26, "Saturn")
    saturn.y_vel = 9.69 * 1000
    saturn.display_radius = display_radii[5]

    uranus = Planet(19.191 * Planet.AU, 0, 17, LIGHT_BLUE, 8.681 * 10**25, "Uranus")
    uranus.y_vel = 6.81 * 1000
    uranus.display_radius = display_radii[6]

    neptune = Planet(30.07 * Planet.AU, 0, 17, LIGHT_BLUE2, 1.024 * 10**26, "Neptune")
    neptune.y_vel = 5.43 * 1000
    neptune.display_radius = display_radii[7]

    planets = [sun, earth, mars, mercury, venus, jupiter, saturn, uranus, neptune]

    while run: 
        clock.tick(60)
        WIN.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for planet in planets: 
            planet.update_position(planets)
            planet.draw(WIN)
        
        pygame.display.update()

    pygame.quit()
 
main()
