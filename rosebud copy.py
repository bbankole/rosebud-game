import sys

import pygame

from settings import Settings
from cat import Cat

class Rosebud:
    """Overall class to manage assets and game behavoir."""
    
    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.settings = Settings()

        self.bg_color = (230, 230, 250)
        self.screen = pygame.display.set_mode((1200, 800))

        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get().height
        pygame.display.set_caption("Rosebud")

        self.cat = Cat(self)
        
    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            self.cat.update()
            self._update_screen()

    def _check_events(self):
            """Respond to keypresses and mouse events."""
            # Watch for keyboard and mouse events.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                elif event.type == pygame.KEYDOWN:
                    self._check_keydown_events(event)

                elif event.type == pygame.KEYUP:
                    self._check_keyup_events(event)

                def _check_keydown_events(self, event):
                    """Respond to keypresses"""
                    if event.key == pygame.K_RIGHT:
                          self.cat.moving_right = True
                    elif event.key == pygame.K_LEFT:
                         self.cat.moving_left = True


                    def _check_keyup_events(self, event):
                            """Respond to keypresses."""
                            if event.key == pygame.K_RIGHT:
                                 self.cat.moving_right = False
                            elif event.key == pygame.K_LEFT:
                                 self.cat.moving_left = False
                                 
                                 

                          # Move the cat to the right

    def _update_screen(self):
         """Update images on screen, and flip to the new screen."""
         self.screen.fill(self.bg_color)
         self.cat.blitme()
         
         pygame.display.flip()
    
if __name__ == '__main__':
        #Make a game instance, and run the game.
        ai = Rosebud()
        ai.run_game()

