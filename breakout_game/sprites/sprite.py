"""
Module describing all sprite objects in the game.
"""

from __future__ import annotations

import math
import time

from typing import TYPE_CHECKING

import pygame

from config import settings
from utils import path_utils

from sprites.powerup_manager import PowerUpManager

if TYPE_CHECKING:
    from sprite_manager import SpriteManager


class _GameSprite(pygame.sprite.Sprite):
    """
    Base class for any game sprite. All game sprites must inherit from this class.

    Sprite is registered in groups provided.

    Attributes:
        sprite_manager (SpriteManager): Instance of sprites.SpriteManager class
        sprite_groups (list[pygame.sprite.AbstractGroup]): Any collection of any group types in pygame.sprite.Group
        image (pygame.Surface): An image of the sprite. Must be an instance of pygame.Surface
        rect (pygame.Rect): An instance of the pygame.Rect class
        position (pygame.math.Vector2): Position of sprite on the screen.
            Defaults to pygame.math.Vector2(rect.topleft)
        direction (pygame.math.Vector2): Direction in which sprites moves along x and y-axis.
            Defaults to pygame.math.Vector2((0, 0)
        speed (int, float): Speed of movement. Defaults to 0
        original_image (pygame.Surface): A copy of the original image provided during construction.
            Defaults to image.copy(). Used primarily for powerup handling.
        original_rect (pygame.Rect): A copy of the original rectangle provided during construction.
            Defaults to rect.copy(). Used primarily for powerup handling.
        original_width (int): The width of the original rectangle.
            Defaults to rect.width. Used primarily for powerup handling.
        original_height (int): The height of the original rectangle.
            Defaults to rect.width. Used primarily for powerup handling.

    Args:
        sprite_manager (SpriteManager): Instance of the sprites.SpriteManager class.
        sprite_groups (list[pygame.sprite.AbstractGroup]): Any collection of any group types in pygame.sprite.Group.
        image (pygame.Surface): An image of the sprite. Must be an instance of pygame.Surface.
        rect (pygame.Rect): An instance of the pygame.Rect class.

    version: 1
    """
    def __init__(
            self,
            sprite_manager: SpriteManager,
            sprite_groups: list[pygame.sprite.AbstractGroup],
            image: pygame.Surface,
            rect: pygame.Rect
    ):
        pygame.sprite.Sprite.__init__(self)
        for group in sprite_groups:
            self.add(group)

        self.sprite_manager = sprite_manager
        self.sprite_groups = sprite_groups
        self.image = image
        self.rect = rect

        self.position = pygame.math.Vector2(self.rect.topleft)  # pylint: disable=I1101
        self.direction = pygame.math.Vector2((0, 0))  # pylint: disable=I1101
        self.speed = 0

        self.original_image = self.image.copy()
        self.original_rect = self.rect.copy()
        self.original_width = self.rect.width
        self.original_height = self.rect.height

    def update(self, *args, **kwargs):
        """
        Updates the sprite based on the game logic.
        """
        raise NotImplementedError('Sprite class must implement "update" method')

    def movement(self, delta_time: (int, float)):
        """
        Updates the position of sprite based on current position, speed, delta time and direction.

        Args:
        delta_time (int, float): Time passed since last frame.
        """
        self.position.x += self.direction.x * self.speed * delta_time
        self.position.y += self.direction.y * self.speed * delta_time
        self.rect.x = round(self.position.x)
        self.rect.y = round(self.position.y)

    def update_position_from_rect(self):
        """
        Update position attribute for rectangle attribute.
        """
        self.position.x = self.rect.x
        self.position.y = self.rect.y

    def change_size(
            self,
            new_width: int,
            new_height: int
    ):
        """
        Change size of the sprite based on the new width and height provided.

        The new image is created from the original one. Does not handle active powerups.

        Args:
            new_width (int): New width.
            new_height (int): New height.
        :return:
        """
        rect_center = self.rect.center
        self.image = pygame.transform.scale(self.original_image, (new_width, new_height))
        self.rect = self.image.get_rect(center=rect_center)
        self.rect.height = new_height
        self.update_position_from_rect()

    def change_image(
            self,
            new_image: pygame.Surface,
            new_width: int,
            new_height: int
    ):
        """
        Change image of the sprite based on the image, new width and height provided.

        The new image is created from the provided one. Does not handle active powerups.

        Args:
            new_image (pygame.Surface): New image of type pygame.Surface.
            new_width (int): New width.
            new_height (int): New height.
        """
        rect_center = self.rect.center
        self.image = pygame.transform.scale(new_image, (new_width, new_height))
        self.rect = self.image.get_rect(center=rect_center)
        self.update_position_from_rect()

    def restore_size(self):
        """
        Restore size of the sprite based on the original width and original height. Scales the current image.
        """
        rect_center = self.rect.center
        self.image = pygame.transform.scale(self.image, (self.original_width, self.original_height))
        self.rect = self.image.get_rect(center=rect_center)
        self.update_position_from_rect()

    def restore_image(self):
        """
        Restore image of the sprite based on the original one.
        """
        rect_center = self.rect.center
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(center=rect_center)
        self.update_position_from_rect()


class Heart(_GameSprite):
    """
    Sprite representing the hearts - player's health points.
    """
    def __init__(
            self,
            sprite_manager: SpriteManager,
            sprite_groups: list[pygame.sprite.AbstractGroup],
            image: pygame.Surface,
            rect: pygame.Rect
    ):
        super().__init__(sprite_manager=sprite_manager, sprite_groups=sprite_groups, image=image, rect=rect)

    # pylint: disable=W0221
    def update(self, *args, **kwargs):
        pass


class Player(_GameSprite):
    """
    Player sprite representing the paddle and the player.

    Attributes:
        health (int): The health of the player.
        lost_hp_sound (pygame.mixer.Sound): The sound of the player loosing a health point.
    """
    def __init__(
            self,
            sprite_manager: SpriteManager,
            sprite_groups: list[pygame.sprite.AbstractGroup],
            image: pygame.Surface,
            rect: pygame.Rect,
    ):
        super().__init__(sprite_manager=sprite_manager, sprite_groups=sprite_groups, image=image, rect=rect)
        self.health: int = settings.MAX_PLAYER_HEALTH
        self.speed = settings.DEFAULT_PADDLE_SPEED

        lost_hp_sound_path = path_utils.get_asset_path('sounds/lost_hp.mp3')
        self.lost_hp_sound: pygame.mixer.Sound = pygame.mixer.Sound(lost_hp_sound_path)

    def check_screen_constraint(self):
        """
        Check if the paddle hits the screen boundaries and adjust position accordingly.
        """
        if self.rect.right > settings.GAME_WINDOW_WIDTH:
            self.rect.right = settings.GAME_WINDOW_WIDTH
            self.position.x = self.rect.x

        if self.rect.left < 0:
            self.rect.left = 0
            self.position.x = self.rect.x

    def loose_health(self):
        """
        Make player loose health.
        """
        if self.health >= 1:
            self.health -= 1
            heart_sprites = self.sprite_manager.heart_sprites_group.sprites()
            heart_sprites[-1].kill()
            self.sprite_manager.score_sprites_group.sprites()[0].subtract_score(200)
            self.lost_hp_sound.stop()
            self.lost_hp_sound.play()

    def add_health(self):
        """
        Add health to the player.
        """
        if self.health < settings.MAX_PLAYER_HEALTH:
            self.health += 1
            heart_horizontal_gap = settings.SCOREBOARD_WIDTH // (settings.MAX_PLAYER_HEALTH + 1)

            heart_midtop = (
                settings.GAME_WINDOW_WIDTH + self.health * heart_horizontal_gap,
                settings.GAME_WINDOW_HEIGHT // 7
            )
            self.sprite_manager.create_heart(midtop=heart_midtop)

    # pylint: disable=W0221
    def update(self, delta_time: (int, float), keys_pressed: pygame.key.ScancodeWrapper):
        """
        Checks which keys are pressed and updates the paddle position.

        Args:
            delta_time (int, float): The time passed since last frame.
            keys_pressed (pygame.key.ScancodeWrapper): Keys pressed.
        """
        if keys_pressed[pygame.K_RIGHT]:  # pylint: disable=E1101
            self.direction.x = 1
        elif keys_pressed[pygame.K_LEFT]:  # pylint: disable=E1101
            self.direction.x = -1
        else:
            self.direction.x = 0

        self.movement(delta_time)
        self.check_screen_constraint()
        self.rect.x = round(self.position.x)


class Score(_GameSprite):
    """
    Sprite representing a score on the scoreboard.

    Attributes:
        score (int): The score to draw on the scoreboard.
        font (pygame.font.Font): The font to use for the score.
        color (pygame.Color): The color to use for the score.

    Args:
        font (pygame.font.Font): The font to use for the score.
        color (pygame.Color): The color to use for the score.

    version: 1
    """
    def __init__(
            self,
            sprite_manager: SpriteManager,
            sprite_groups: list[pygame.sprite.AbstractGroup],
            image: pygame.Surface,
            rect: pygame.Rect,
            font: pygame.font.Font,
            color: pygame.Color
    ):
        super().__init__(sprite_manager=sprite_manager, sprite_groups=sprite_groups, image=image, rect=rect)
        self.score: int = 0
        self.font: pygame.font.Font = font
        self.color: pygame.Color = color

    def add_score(self, points: int):
        """
        Add score to the object.

        Args:
            points (int): Points to add.
        """
        self.score += points

    def subtract_score(self, points: int):
        """
        Subtract score from the object.

        Args:
            points (int): Points to subtract.

        Returns:

        """
        self.score -= points

    def update(self, *args, **kwargs):
        """
        Update the score based on the new score and realign the text.
        Returns:

        """
        old_rect_center = self.rect.center
        self.image = self.font.render(f'Score: {self.score}', True, self.color)
        self.rect = self.image.get_rect(center=old_rect_center)


class PowerUp(_GameSprite):
    """
    Sprite representing a powerup icon in the game.

    Attributes:
        power (str): The name of the powerup.
        powerup_manager (PowerUpManager): The PowerUpManager instance which handles the behaviour of powerups.
        powerup_sound (pygame.mixer.Sound): The sound to play when player catches the powerup.

    Args:
        power (str): The name of the powerup.
        powerup_manager (PowerUpManager): The PowerUpManager instance which handles the behaviour of powerups.

    version: 1
    """
    def __init__(
            self,
            sprite_manager: SpriteManager,
            sprite_groups: list[pygame.sprite.AbstractGroup],
            image: pygame.Surface,
            rect: pygame.Rect,
            powerup_manager: PowerUpManager,
            power: str = ''
    ):
        super().__init__(sprite_manager=sprite_manager, sprite_groups=sprite_groups, image=image, rect=rect)

        self.direction = pygame.math.Vector2((0, 1))  # pylint: disable=I1101
        self.speed = settings.DEFAULT_POWERUP_SPEED
        self.power: str = power
        self.powerup_manager: PowerUpManager = powerup_manager

        powerup_sound_path = path_utils.get_asset_path('sounds/get powerup.mp3')
        self.powerup_sound: pygame.mixer.Sound = pygame.mixer.Sound(powerup_sound_path)
        self.powerup_sound.set_volume(0.3)

    def activate(self):
        """
        Activate the powerup. Checks for timers on the scoreboard and conflicting powers. Plays the sound.
        """
        self.powerup_manager.activate_powerup(self.power)
        if settings.POWERS[self.power]['time'] != -1:
            powerup_timers_in_game = self.sprite_manager.power_up_timer_info_group.sprites()
            for powerup_timer in powerup_timers_in_game:

                powerup_timer_power_name = powerup_timer.power_name
                conflicting_power = settings.POWERS[powerup_timer_power_name]['conflicting-power']

                if powerup_timer_power_name == self.power:
                    powerup_timer.kill()
                elif conflicting_power is not None:
                    if conflicting_power == self.power:
                        powerup_timer.kill()
            self.sprite_manager.create_powerup_timer_info(self.power, settings.POWERS[self.power]['time'])
        self.powerup_sound.stop()
        self.powerup_sound.play()

    def update(self, delta_time: (int, float)):  # pylint: disable=W0221
        """
        Update the position of the sprite and check if it hit the paddle.

        Args:
            delta_time (int, float): Time passed since the last frame.
        """
        if self.rect.top > settings.GAME_WINDOW_HEIGHT:
            self.kill()
        if pygame.sprite.collide_rect(self, self.sprite_manager.player_sprites_group.sprites()[0]):
            self.activate()
            self.sprite_manager.score_sprites_group.sprites()[0].add_score(
                100 * (self.sprite_manager.level_difficulty + 1)
            )
            self.kill()
        self.movement(delta_time)


class Block(_GameSprite):
    """
    Block sprite.

    Attributes:
        health (int): Health of the block.
        hit_sound (pygame.mixer.Sound): Sound played when block is hit.
        break_sound (pygame.mixer.Sound): Sound played when block is broken.

    Args:
        health (int): Health of the block.
    """
    def __init__(
            self,
            sprite_manager: SpriteManager,
            sprite_groups: list[pygame.sprite.AbstractGroup],
            image: pygame.Surface,
            rect: pygame.Rect,
            health: int,
    ):
        super().__init__(sprite_manager=sprite_manager, sprite_groups=sprite_groups, image=image, rect=rect)
        self.health = health
        self.update_image()

        hit_sound_path = path_utils.get_asset_path('sounds/hit blocks.mp3')
        self.hit_sound = pygame.mixer.Sound(hit_sound_path)
        self.hit_sound.set_volume(0.25)

        break_sound_path = path_utils.get_asset_path('sounds/break blocks.mp3')
        self.break_sound = pygame.mixer.Sound(break_sound_path)
        self.break_sound.set_volume(0.75)

    def get_damage(self, amount: int):
        """
        Get damage based on the amount of damage specified

        Args:
            amount (int): The amount of damage.
        """
        self.health -= amount
        if self.health <= 0:
            self.sprite_manager.score_sprites_group.sprites()[0].add_score(
                30 * (self.sprite_manager.level_difficulty + 1)
            )
            self.break_sound.stop()
            self.break_sound.play()
            self.kill()
            self.sprite_manager.drop_powerup(self)
        else:
            self.sprite_manager.score_sprites_group.sprites()[0].add_score(
                10 * (self.sprite_manager.level_difficulty + 1)
            )
            self.hit_sound.stop()
            self.hit_sound.play()

    def update_image(self):
        """
        Update the image of the block based on health.
        """
        if self.health in settings.COLOR_LEGEND:
            new_image = pygame.image.load(settings.COLOR_LEGEND[self.health])
            self.change_image(new_image, settings.BLOCK_WIDTH, settings.BLOCK_HEIGHT)

    def update(self, *args, **kwargs):
        """
        Update the sprite.
        """
        self.update_image()


class Ball(_GameSprite):
    """
    Ball sprite. Handles collision detection and bouncing.

    Attributes:
        speed (int): Speed of the ball.
        original_speed (int): Original speed of the ball. Used for powerups.
        strength (int): Strength of the ball. Used to detect how much damage is dealt to blocks.
            Defaults to 1
        original_strength (int): Original strength of the ball. Used for powerups.
        time_delay_counter (int, float): Time to delay when ball is lost before activating it again.
        hit_paddle_sound (pygame.mixer.Sound): Sound to play when ball hits the paddle.
        active (bool): Whether the ball is active or not.
            Defaults to False

    Args:
        speed (int): Speed of the ball.
    """
    def __init__(
            self,
            sprite_manager: SpriteManager,
            sprite_groups: list[pygame.sprite.AbstractGroup],
            image: pygame.Surface,
            rect: pygame.Rect,
            speed: int
    ):
        super().__init__(sprite_manager=sprite_manager, sprite_groups=sprite_groups, image=image, rect=rect)

        self.direction = pygame.math.Vector2((0, -1))  # pylint: disable=I1101

        self.speed = speed
        self.original_speed = speed

        self.strength = 1
        self.original_strength = 1

        self.time_delay_counter = 0

        hit_paddle_sound_path = path_utils.get_asset_path('sounds/hit paddle.mp3')
        self.hit_paddle_sound = pygame.mixer.Sound(hit_paddle_sound_path)
        self.active = False

    def get_angle_of_direction(self):
        """
        Get the angle of direction in radians
        """
        return math.atan2(self.direction[1], self.direction[0])

    def set_direction_from_angle(self, angle: (int, float)):
        """
        Set direction from the angle presented in radians.

        Args:
            angle (int, float): Angle in radians
        """
        self.direction = pygame.math.Vector2((math.cos(angle), math.sin(angle)))  # pylint: disable=I1101

    def change_speed(self, new_speed: int):
        """
        Change the speed of the ball. Used in powerups.

        Args:
            new_speed (int): New speed of the ball.
        """
        self.speed = new_speed

    def restore_speed(self):
        """
        Restore the original speed of the ball. Used in powerups.
        """
        self.speed = self.original_speed

    def change_strength(self, new_strength: int):
        """
        Change the strength of the ball. Used in powerups.

        Args:
            new_strength (int): New strength of the ball.
        """
        self.strength = new_strength

    def restore_strength(self):
        """
        Restore the original strength of the ball. Used in powerups.
        """
        self.strength = self.original_strength

    def loose_ball(self):
        """
        Loose the ball, make it inactive and make player loose health.
        """
        self.time_delay_counter = time.time()
        if len(self.sprite_manager.ball_sprites_group.sprites()) == 1:
            self.sprite_manager.player_sprites_group.sprites()[0].loose_health()
            self.active = False
        else:
            self.kill()

    def frame_collision(self):
        """
        Check if the ball collides with the game window, change its direction and position.
        """
        # Hit the left side of the game window
        if self.rect.left < 0:
            self.rect.left = 0
            self.position.x = 0
            self.direction.x *= -1

        # Hit the right side of the game window
        elif self.rect.right > settings.GAME_WINDOW_WIDTH:
            self.rect.right = settings.GAME_WINDOW_WIDTH
            self.position.x = self.rect.topleft[0]
            self.direction.x *= -1

        # Hit the top of the game window
        if self.rect.top < 0:
            self.rect.top = 0
            self.position.y = 0
            self.direction.y *= -1

        # Hit the bottom of the game window
        elif self.rect.top > settings.GAME_WINDOW_HEIGHT:
            self.loose_ball()

    def get_overlapping_rect(self, colliding_sprites: list) -> pygame.rect.Rect:
        """
        Get overlapping rectangle from the colliding sprites.
        The rectangle is calculated as the biggest rectangle which encapsulates all the overlap rectangles.

        Args:
            colliding_sprites (list): List of colliding sprites.

        Returns:
            pygame.rect.Rect: The overlapping rectangle.
        """
        total_overlap_left = settings.GAME_WINDOW_WIDTH
        total_overlap_right = 0
        total_overlap_top = settings.GAME_WINDOW_HEIGHT
        total_overlap_bottom = 0

        # Calculate the overall area of overlapping
        for sprite in colliding_sprites:
            overlap = self.rect.clip(sprite.rect)
            total_overlap_left = min(total_overlap_left, overlap.left)
            total_overlap_right = max(total_overlap_right, overlap.right)
            total_overlap_top = min(total_overlap_top, overlap.top)
            total_overlap_bottom = max(total_overlap_bottom, overlap.bottom)

        # Keyword arguments do not work here
        overlap_rect = pygame.rect.Rect(  # pylint: disable=I1101
            total_overlap_left,  # left
            total_overlap_top,  # top
            abs(total_overlap_right - total_overlap_left),  # width
            abs(total_overlap_bottom - total_overlap_top)  # height
        )
        return overlap_rect

    def handle_vertical_collision(self, overlapping_rect: pygame.Rect):
        """
        Handle the collision in vertical direction. Adjust the position and direction.

        Args:
            overlapping_rect (pygame.Rect): Overlapping rectangle obtained from get_overlapping_rect
        """
        if self.direction.y < 0:
            self.rect.top = overlapping_rect.bottom
        else:
            self.rect.bottom = overlapping_rect.top
        self.direction.y *= -1

    def handle_horizontal_collision(self, overlapping_rect: pygame.Rect):
        """
        Handle the collision in horizontal direction. Adjust the position and direction.

        Args:
            overlapping_rect (pygame.Rect): Overlapping rectangle obtained from get_overlapping_rect
        """
        if self.direction.x < 0:
            self.rect.left = overlapping_rect.right
        else:
            self.rect.right = overlapping_rect.left
        self.direction.x *= -1

    def handle_diagonal_collision(self, overlapping_rect: pygame.Rect):
        """
        Handle the collision in diagonal direction. Adjust the position and direction.

        Args:
            overlapping_rect (pygame.Rect): Overlapping rectangle obtained from get_overlapping_rect
        """
        if self.direction.x < 0:
            self.rect.left = overlapping_rect.right
        else:
            self.rect.right = overlapping_rect.left
        self.direction.x *= -1
        if self.direction.y < 0:
            self.rect.top = overlapping_rect.bottom
        else:
            self.rect.bottom = overlapping_rect.top
        self.direction.y *= -1

    def handle_hor_hit_by_player(self, colliding_players: list[Player]):
        """
        Handle hit by player colliding with the ball in horizontal direction

        Note:
            It is a special case to prevent the ball from clipping inside the paddle.

        Args:
            colliding_players (list[Player]): List of player sprites
        """
        player_direction_x = colliding_players[0].direction.x
        paddle_path_per_frame = abs(round(player_direction_x * colliding_players[0].speed / settings.FPS))
        if player_direction_x > 0:
            self.rect.x += paddle_path_per_frame * 3
        else:
            self.rect.x -= paddle_path_per_frame * 3

        self.direction.x = player_direction_x

    def paddle_adjust_angle(self, overlapping_rect: pygame.Rect):
        """
        Adjust the angle of the ball according to the position of the hit point.

        Args:
            overlapping_rect (pygame.Rect): Overlapping rectangle obtained from get_overlapping_rect.
        """
        hit_point_x = overlapping_rect.centerx
        paddle_middle = self.sprite_manager.player_sprites_group.sprites()[0].rect.centerx
        paddle_width = self.sprite_manager.player_sprites_group.sprites()[0].rect.width

        dist_from_paddle_center = hit_point_x - paddle_middle
        angle_ratio = abs(dist_from_paddle_center) / (paddle_width / 2)
        if angle_ratio != 0:
            resulting_angle = math.pi / 2 - angle_ratio * (math.pi / 2 - math.pi / 6)
            resulting_cotangent = 1 / math.tan(resulting_angle)

            if dist_from_paddle_center > 0:
                self.direction.x = resulting_cotangent * abs(self.direction.y)
            else:
                self.direction.x = -1 * resulting_cotangent * abs(self.direction.y)
        else:
            self.direction.x = 0

    def handle_bounce(self, overlapping_rect: pygame.rect.Rect, colliding_players: list[Player]):
        """
        General method to handle bounce movement.

        Args:
            overlapping_rect (pygame.rect.Rect): Overlapping rectangle obtained from get_overlapping_rect.
            colliding_players (list[Player]): List of paddles that collide with the ball.
        """
        if len(colliding_players) > 0:
            if overlapping_rect.height > overlapping_rect.width:
                self.handle_hor_hit_by_player(colliding_players)
            elif overlapping_rect.width > overlapping_rect.height:
                self.handle_vertical_collision(overlapping_rect)
                self.paddle_adjust_angle(overlapping_rect)
            else:
                self.handle_diagonal_collision(overlapping_rect)
        else:
            # Vertical
            if overlapping_rect.width > overlapping_rect.height:
                self.handle_vertical_collision(overlapping_rect)
            # Horizontal
            if overlapping_rect.height > overlapping_rect.width:
                self.handle_horizontal_collision(overlapping_rect)
            # Diagonal
            if overlapping_rect.height == overlapping_rect.width:
                self.handle_diagonal_collision(overlapping_rect)

    def handle_collisions(self):
        """
        General method to handle collisions between blocks and paddles.
        """
        colliding_blocks = pygame.sprite.spritecollide(self, self.sprite_manager.block_sprites_group, False)
        colliding_players = pygame.sprite.spritecollide(self, self.sprite_manager.player_sprites_group, False)
        colliding_sprites = colliding_blocks + colliding_players
        if len(colliding_sprites) > 0:
            overlap_rect = self.get_overlapping_rect(colliding_sprites=colliding_sprites)
            self.handle_bounce(overlapping_rect=overlap_rect, colliding_players=colliding_players)

            if len(colliding_players) == 0:

                for sprite in colliding_sprites:
                    if getattr(sprite, 'health', None):
                        for _ in range(self.strength):
                            sprite.get_damage(1)
            else:
                self.hit_paddle_sound.stop()
                self.hit_paddle_sound.play()
            self.position.x = self.rect.x
            self.position.y = self.rect.y

    # pylint: disable=W0221
    def update(self, delta_time: (int, float), keys_pressed: pygame.key.ScancodeWrapper):
        """
        Update the status of the ball. Handle movement, collisions and activation.

        Args:
            delta_time (int, float):
            keys_pressed (pygame.key.ScancodeWrapper):
        """
        if self.active:

            if self.direction.magnitude() != 0:
                self.direction = self.direction.normalize()

            self.movement(delta_time)
            self.frame_collision()
            self.handle_collisions()

        else:
            if time.time() - self.time_delay_counter > 0.5:
                self.rect.midbottom = self.sprite_manager.player_sprites_group.sprites()[0].rect.midtop
                self.position = pygame.math.Vector2(self.rect.topleft)  # pylint: disable=I1101

                if keys_pressed[pygame.K_SPACE]:  # pylint: disable=E1101
                    self.active = True
                    self.direction = pygame.math.Vector2((0, -1))  # pylint: disable=I1101
            else:
                pass


class Scoreboard(_GameSprite):
    """
    Scoreboard sprite. Does nothing.
    """
    def __init__(
            self,
            sprite_manager: SpriteManager,
            sprite_groups: list[pygame.sprite.AbstractGroup],
            image: pygame.Surface,
            rect: pygame.Rect
    ):
        super().__init__(sprite_manager=sprite_manager, sprite_groups=sprite_groups, image=image, rect=rect)

    def update(self, *args, **kwargs):
        pass


class PowerUpTimerInfo(_GameSprite):
    """
    Powerup timer info sprite.
    Creates a text on the scoreboard saying how much time is left for the powerup to be active.

    Attributes:
        font (pygame.font.Font): The font to use for the text.
        color (pygame.Color): The color to use for the text.
        power_name (str): The name of the powerup.
        powerup_time (int, float): The time in seconds for the powerup to be active.
    Args:
        font (pygame.font.Font): The font to use for the text.
        color (pygame.Color): The color to use for the text.
        power_name (str): The name of the powerup.
        powerup_time (int, float): The time in seconds for the powerup to be active.
    """
    def __init__(
            self,
            sprite_manager: SpriteManager,
            sprite_groups: list[pygame.sprite.AbstractGroup],
            image: pygame.Surface,
            rect: pygame.Rect,
            font: pygame.font.Font,
            color: pygame.Color,
            power_name: str,
            powerup_time: (int, float)
    ):
        super().__init__(sprite_manager=sprite_manager, sprite_groups=sprite_groups, image=image, rect=rect)

        self.font = font
        self.color = color
        self.powerup_time = powerup_time
        self.start_time = time.time()
        self.power_name = power_name

    # pylint: disable=W0221
    def update(self, time_in_pause: (int, float) = 0):
        """
        Update the text.

        Args:
            time_in_pause (int, float): Time spent in pause. Defaults to 0.
        """
        self.start_time += time_in_pause
        time_left = self.powerup_time - (time.time() - self.start_time)
        old_rect_center = self.rect.center
        if time_left > 0:
            self.image = self.font.render(
                f'{self.power_name.upper()} Time Left: {time_left:.2f}', True, self.color)
            self.rect = self.image.get_rect(center=old_rect_center)
        else:
            self.kill()
