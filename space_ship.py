"""
DOCSTRING

The player-controlled spaceship.
Just like Creature, but includes custom motion, hit detection method,
and attributes related to the short immunity following a hit.

The ship moves left if the player presses the left key, 
and right if the palyer presses the right key.

After it is hit, the spaceship cannot be hit again according to the delay
(currently, one second). The delaying method handles this, as do the 
delay attribute, i.e. the amount in seconds that the ship should be immune,
and the last_hit attribute, which stores the last frame when the ship was hit.
"""
import pygame
import os

from bullet import Bullet
from abstract import Creature
from enums import Win, Bulletenum, Paths
from space_invader import SpaceInvader

class SpaceShip(Creature):

    def __init__(
        self,
        vel: int,
        lives: int,
        init_x: int, 
        init_y: int, 
        width: int,
        height: int,
        path: os.path,
        sound: pygame.mixer.Sound
    ):
        super().__init__(vel, lives, init_x, init_y, width, height, path)
        self.ready_to_shoot = True
        self.laser_sound = sound

    def move(self, keys_pressed: dict) -> None:
        """
        Updates the ship's location according to keys pressed.
        """
        condition = self.rect.x < Win.WIDTH.value-self.width

        if keys_pressed[pygame.K_LEFT] and self.rect.x > 0: # LEFT
            self.rect.x -= self.vel
        if keys_pressed[pygame.K_RIGHT] and condition: # RIGHT
            self.rect.x += self.vel

    def is_hit(self, frame: int, invader: SpaceInvader) -> bool:
        """
        Returns true if invader and ship collide.
        """
        if self.rect.colliderect(invader.rect):
            if not self.delaying_hit(frame):
                self.last_hit = frame
                return True
        return False

    def shoot(self, frame: int, keys_pressed) -> list:
        """
        Shoots a bullet, maybe implement a delay later.
        Returns a list with bullet is space is pressed, empty list otherwise.
        """
        if keys_pressed[pygame.K_SPACE] and self.ready_to_shoot:
            self.ready_to_shoot = False # So the player has to press the space bar again
            self.laser_sound.play() # The laser beam sound
            return [
                Bullet(
                    init_x=self.rect.x + (self.width - Bulletenum.WIDTH.value)/2,
                    init_y=self.rect.y,
                )
            ]
        elif not keys_pressed[pygame.K_SPACE]:
            self.ready_to_shoot = True
        return []