import pygame
import helpers
from definitions import *
from gameParameters import gameDisplay
from towerPics import basicTower1, iceTower1, fireTower1, poisonTower1, darkTower1


class TowerButton:
    """Base class for tower buttons (circular buttons)

    Attributes:
        location:       (Required) tuple(x, y), positions center of tower circle
        button_ radius: radius of tower, defaults to 24 pixels
        main_msg:       message to display on tower (optional)
        main_color1:    color without mouse hover (default light_brown)
        main_color2:    color on mouse hover (default orange)
        font:           font for optional button message,
                        default 'Comic Sans MS'
        font_size:      font size of optional message, defaults to 20
        message_color:  txt color of main button optional msg, defaults = black
        option_count:   number of option buttons to create (default = 1)
                        Note: can specify 0-5 options
                        (numbers greater than 5 won't have button)

        The following entries will use # to designate an option number:
        opt#_col1:      option's color while mouse not hovering button
                        default different for each option
        opt#_col2:      option's color while mouse is hovering button
        opt#_msg:       that option's message (default is None)
        opt#_msg_col:   that option's message color (default is black)

    Usage:
        Define a button with x, y coordinates specified, and optional kwargs
        call draw in main loop to draw button and associated option buttons
    """

    def __init__(
            self, location, button_radius=24, destroy=False,
            main_msg=None, set_options_timer=30, main_color1=light_brown,
            main_color2=orange, font="Comic Sans MS", font_size=20,
            message_color=black, option_count=1, opt1_col1=yellow,
            opt1_col2=bright_yellow, opt2_col1=teal,
            opt2_col2=bright_teal, opt3_col1=red,
            opt3_col2=bright_red, opt4_col1=green,
            opt4_col2=bright_green, opt5_col1=purple,
            opt5_col2=bright_purple, opt1_msg=None, opt2_msg=None,
            opt3_msg=None, opt4_msg=None, opt5_msg=None, opt1_msg_col=black,
            opt2_msg_col=black, opt3_msg_col=black, opt4_msg_col=black,
            opt5_msg_col=black, opt1_action=None, opt2_action=None,
            opt3_action=None, opt4_action=None, opt5_action=None):
        super().__init__()
        self.image = None
        self._button_radius = button_radius
        self._mouse = None
        self._click = None
        self.x, self.y = location
        self._font = font
        self._font_size = font_size
        self.destroy = destroy
        self.option_selected = None
        self._options_countdown = 0
        self.set_options_timer = set_options_timer
        self.option_count = option_count
        self.lockout = 20
        self.lockout_timer = self.lockout
        # List == x_offset, y_offset, no_hover_color, hover_color, msg, msg_col
        # Circle list index 0 refers to main circle (tower location)
        self.circle_list = [
            [0, 0, main_color1, main_color2, main_msg, message_color, None]]
        # Option list specifies circles (options) to tower location
        self.options_list = [
            [-0.6, 2.3, opt1_col1, opt1_col2,
             opt1_msg, opt1_msg_col, opt1_action],
            [1.3, 1.9, opt2_col1, opt2_col2,
             opt2_msg, opt2_msg_col, opt2_action],
            [2.2, 0.25, opt3_col1, opt3_col2,
             opt3_msg, opt3_msg_col, opt3_action],
            [1.7, -1.6, opt4_col1, opt4_col2,
             opt4_msg, opt4_msg_col, opt4_action],
            [-0.1, -2.2, opt5_col1, opt5_col2,
             opt5_msg, opt5_msg_col, opt5_action]]
        # Append to circle_list as many options as specified by option_count
        for option in self.options_list:
            if self.options_list.index(option) == self.option_count:
                break
            else:
                self.circle_list.append(option)

    def draw(self):
        """Draw main and option circles, highlight color if hovered
        perform action if clicked,
        show options for a period of set_option_timer"""

        if self.lockout_timer > 0:
            self.lockout_timer -= 1
        # Parameter for killing tower (destroyed if replaced or sold)
        if self.destroy or self.lockout_timer > 0:
            return None

        self._mouse = pygame.mouse.get_pos()
        self._click = pygame.mouse.get_pressed()

        # define relevant variables
        for circle in self.circle_list:
            circle_number = self.circle_list.index(circle)
            x_offset, y_offset, no_hov_color, hov_color, \
                msg, msg_col, action = circle
            if circle_number == 0:
                radius = self._button_radius
            else:
                radius = int(self._button_radius * 0.7)
            x = int(self.x + x_offset * radius)
            y = int(self.y + y_offset * radius)

            # If hovering over a circle
            if (x - radius < self._mouse[0] < x + radius
                    and y - radius < self._mouse[1] < y + radius):
                if circle_number == 0 or self._options_countdown > 0:
                    pygame.draw.circle(gameDisplay, hov_color, (x, y), radius)
                    if circle_number == 0:
                        self.show_tower_image()
                    if circle_number > 0:
                        self._options_countdown = self.set_options_timer
                    if self._click[0] == 1:
                        if circle_number == 0:
                            self._options_countdown = int(
                                self.set_options_timer * 1.5)
                        else:
                            if action is not None:
                                self.option_selected = action
                                self.lockout_timer = 10

            # If not hovering circle, draw inactive circle if possible
            else:
                if circle_number == 0:
                    if not self.image:
                        pygame.draw.circle(
                            gameDisplay, no_hov_color, (x, y), radius)
                    if circle_number == 0:
                        self.show_tower_image()
                if self._options_countdown > 0:
                    pygame.draw.circle(
                        gameDisplay, no_hov_color, (x, y), radius)
                    if circle_number == 0:
                        self.show_tower_image()

            if msg and (circle_number == 0 or self._options_countdown > 0):
                if circle_number == 0:
                    self.set_text(x, y, msg, msg_col, True)
                else:
                    self.set_text(x, y, msg, msg_col, False)
        if self._options_countdown > 0:
            self._options_countdown -= 1

    def show_tower_image(self):
        pass

    def set_text(self, x, y, msg, msg_color, is_main):
        """Draw text over main or option circles if specified"""
        if is_main:
            font = pygame.font.SysFont(self._font, self._font_size, bold=True)
        else:
            font = pygame.font.SysFont(
                self._font, int(self._font_size * .6), bold=True)
        text_surface = font.render(msg, True, msg_color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        gameDisplay.blit(text_surface, text_rect)


class BasicTower(TowerButton):
    def __init__(
            self, location, tower_range=125, destroy=True,
            option_count=5, opt1_msg="Sell", opt1_action="sell",
            opt2_msg="Ice", opt2_action="ice", opt3_msg="Fire",
            opt3_action="fire", opt4_msg="Poison", opt4_action="poison",
            opt5_msg="Dark", opt5_action="dark",
            main_color1=grass_green, main_color2=bright_green):
        super().__init__(
            location, destroy=destroy,
            option_count=option_count, opt1_msg=opt1_msg,
            opt1_action=opt1_action, opt2_msg=opt2_msg, opt2_action=opt2_action,
            opt3_msg=opt3_msg, opt3_action=opt3_action, opt4_msg=opt4_msg,
            opt4_action=opt4_action, opt5_msg=opt5_msg, opt5_action=opt5_action,
            main_color1=main_color1, main_color2=main_color2)
        self.image, self.image_width, self.image_height = basicTower1
        self.radius = tower_range  # range
        self.buy = 100
        self.sell = 75
        self.specialty = None

    def show_tower_image(self):
        gameDisplay.blit(
            self.image, (int(self.x - 0.5 * self.image_width),
                         int(self.y - .8 * self.image_height)))


class IceTower(BasicTower):
    def __init__(
            self, location, tower_range=125,
            option_count=1, opt1_msg="Sell", opt1_action="sell",
            main_color1=blue, main_color2=bright_blue):
        super().__init__(
            location, tower_range=tower_range,
            option_count=option_count, opt1_msg=opt1_msg,
            opt1_action=opt1_action, main_color1=main_color1,
            main_color2=main_color2)
        self.image, self.image_width, self.image_height = iceTower1
        self.buy = 100
        self.sell = 150
        self.specialty = "ice"


class FireTower(BasicTower):
    def __init__(
            self, location, tower_range=125,
            option_count=1, opt1_msg="Sell", opt1_action="sell",
            main_color1=red, main_color2=bright_red):
        super().__init__(
            location, tower_range=tower_range,
            option_count=option_count, opt1_msg=opt1_msg,
            opt1_action=opt1_action, main_color1=main_color1,
            main_color2=main_color2)
        self.image, self.image_width, self.image_height = fireTower1
        self.buy = 100
        self.sell = 150
        self.specialty = "fire"


class PoisonTower(BasicTower):
    def __init__(
            self, location, tower_range=125,
            option_count=1, opt1_msg="Sell", opt1_action="sell",
            main_color1=green, main_color2=bright_green):
        super().__init__(
            location, tower_range=tower_range,
            option_count=option_count, opt1_msg=opt1_msg,
            opt1_action=opt1_action, main_color1=main_color1,
            main_color2=main_color2)
        self.image, self.image_width, self.image_height = poisonTower1
        self.buy = 100
        self.sell = 150
        self.specialty = "poison"


class DarkTower(BasicTower):
    def __init__(
            self, location, tower_range=125,
            option_count=1, opt1_msg="Sell", opt1_action="sell",
            main_color1=purple, main_color2=bright_purple):
        super().__init__(
            location, tower_range=tower_range,
            option_count=option_count, opt1_msg=opt1_msg,
            opt1_action=opt1_action, main_color1=main_color1,
            main_color2=main_color2)
        self.image, self.image_width, self.image_height = darkTower1
        self.buy = 100
        self.sell = 150
        self.specialty = "dark"


# Deals up-front damage, reduced by armor
class BasicMissile:
    def __init__(self, location):
        self.x, self.y = location
        x, y = location
        self.x = x
        self.y = y - 50
        self._tower_location = self.x, self.y
        self.speed = 4
        self.lock_on = None
        self.destroy = True
        self.radius = 5
        self.shoot_rate = 5 * seconds
        self.shoot_counter = 0
        self.missile_color = gray
        self.damage = 5
        self.specialty = None

    def lock_enemy(self, tower, enemy):
        # Checks, need: shoot_counter at 0, enemy alive, no missile alive,
        # Then, if enemy in range of tower, un-destroy missile
        if self.shoot_counter < 1:
            if not enemy.destroy:
                if self.destroy is True:
                    if helpers.collision(tower, enemy):
                        if self.lock_on is None:
                            self.lock_on = enemy
                            self.destroy = False
                            self.shoot_counter = self.shoot_rate
        if self.shoot_counter > 0:
            self.shoot_counter -= 1
        hit = self.shoot(enemy)
        return hit

    def shoot(self, enemy):
        # Move missile towards locked on enemy by self.speed and redraw.
        if not self.destroy:
            if self.lock_on == enemy:
                if self.x < enemy.x:
                    self.x += self.speed
                if self.x > enemy.x:
                    self.x -= self.speed
                if self.y < enemy.y:
                    self.y += self.speed
                if self.y > enemy.y:
                    self.y -= self.speed
                pygame.draw.circle(
                    gameDisplay, self.missile_color,
                    (self.x, self.y), self.radius)
                hit = self.hit(enemy)
                if hit:
                    return hit

    def hit(self, enemy):
        # Check for collision between missile and enemy
        # If collision to locked on target,
        # destroy missile and set its location back to tower
        if helpers.collision(self, enemy):
            self.destroy = True
            self.lock_on = None
            self.x, self.y = self._tower_location
            if not enemy.destroy:
                return self.damage, self.specialty


# Slows enemy and deals up-front damage reduced by armor
class IceMissile(BasicMissile):
    def __init__(self, location):
        super().__init__(location)
        self.damage = 3
        self.missile_color = blue
        self.specialty = "ice"
        self.shoot_rate = 2.5 * seconds


# Burns catches enemy on fire, dealing damage per second for 3 seconds
# No up-front damage, DoT burn reduced by armor
# Enemies on fire will catch other nearby enemies on fire
class FireMissile(BasicMissile):
    def __init__(self, location):
        super().__init__(location)
        self.damage = 0
        self.missile_color = red
        self.specialty = "fire"

    def lock_enemy(self, tower, enemy):
        # Checks, need: shoot_counter at 0, enemy alive, no missile alive,
        # Then, if enemy in range of tower, un-destroy missile
        if self.shoot_counter < 1:
            # Only lock-on if not freshly burned
            if enemy.burned_counter < 2:
                if not enemy.destroy:
                    if self.destroy is True:
                        if helpers.collision(tower, enemy):
                            if self.lock_on is None:
                                self.lock_on = enemy
                                self.destroy = False
                                self.shoot_counter = self.shoot_rate
        if self.shoot_counter > 0:
            self.shoot_counter -= 1
        hit = self.shoot(enemy)
        return hit


# Deals armor piercing DoT every 5 seconds (no up-front damage)
# Poison lasts indefinitely
class PoisonMissile(BasicMissile):
    def __init__(self, location):
        super().__init__(location)
        self.damage = 0
        self.missile_color = green
        self.specialty = "poison"
        self.shoot_rate = 8 * seconds

    def lock_enemy(self, tower, enemy):
        # Checks, need: shoot_counter at 0, enemy alive, no missile alive,
        # Then, if enemy in range of tower, un-destroy missile
        if self.shoot_counter < 1:
            # Only lock-on if not poisoned
            if enemy.poison_charges < 2:
                if not enemy.destroy:
                    if self.destroy is True:
                        if helpers.collision(tower, enemy):
                            if self.lock_on is None:
                                self.lock_on = enemy
                                self.destroy = False
                                self.shoot_counter = self.shoot_rate
        if self.shoot_counter > 0:
            self.shoot_counter -= 1
        hit = self.shoot(enemy)
        return hit


# Deals quadruple damage (3/4 as armor piercing)
class DarkMissile(BasicMissile):
    def __init__(self, location):
        super().__init__(location)
        self.damage = 2
        self.missile_color = purple
        self.specialty = "dark"
