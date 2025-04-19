import pygame
from pygame.sprite import Sprite

class Treat(Sprite):
    """A class to represent a single treat in the fleet."""

    def __init__(self, ai_game):
        """Initialize the treat and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        self.image = pygame.image.load('/Users/bridgettebankole/Desktop/Rosebud/Images/treat.png')
        self.rect = self.image.get_rect()

        # Set the initial position of the treat
        self.rect.x = 0  # You can adjust the initial x position as needed
        self.rect.y = 0  # You can adjust the initial y position as needed

    def check_edges(self):
        """Return True if the treats are at the edge of the screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        """Move the treats to the right or left."""
        self.rect.x += (self.settings.treat_speed * self.settings.fleet_direction)

    def center_ship(self):
        """Center the ship on the screen."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)