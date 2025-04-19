import sys
import pygame
import time
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from cat import Cat
from bullet import Bullet
from treat import Treat

class Rosebud:
    """Overall class to manage assets and game behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.settings = Settings()

        self.bg_color = (230, 230, 250)
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Rosebud")

        # Create an instance to store the game statistics,
        # and create a scoreboard.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.cat = Cat(self)
        self.bullets = pygame.sprite.Group()
        self.treats = pygame.sprite.Group()

        self._create_fleet()

        # Make the play button
        self.play_button = Button(self, "Play")

    def _create_fleet(self):
        """Create the fleet of treats."""
        treat = Treat(self)
        treat_width = treat.rect.width
        treat_height = treat.rect.height

        # Calculate the number of treats per row.
        available_space_x = self.settings.screen_width - (2 * treat_width)
        number_treats_x = available_space_x // (2 * treat_width)

        # Calculate the number of rows.
        available_space_y = (self.settings.screen_height -
                             (3 * treat_height) - treat_height)
        number_rows = available_space_y // (2 * treat_height)

        for row_number in range(number_rows):
            for treat_number in range(number_treats_x):
                self._create_treat(treat_number, row_number)

    def _create_treat(self, treat_number, row_number):
        """Create a treat and place it in a row."""
        treat = Treat(self)
        treat_width, treat_height = treat.rect.size
        treat.x = treat_width + 2 * treat_width * treat_number
        treat.rect.x = treat.x
        treat.rect.y = treat_height + 2 * treat_height * row_number
        self.treats.add(treat)

    def _check_fleet_edges(self):
        """Respond appropriately if any treats have reached the edge"""
        for treat in self.treats.sprites():
            if treat.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for treat in self.treats.sprites():
            treat.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.cat.update()
                self._update_bullets()
                self._update_treats()

            self._update_screen()

    def _update_treats(self):
        """
        Check if the fleet is at the edge,
        then update the positions of all treats in the fleet.
        """
        self._check_fleet_edges()
        self.treats.update()
        if pygame.sprite.spritecollideany(self.cat, self.treats):
            self._cat_hit()
            print("You got treats! 🐱")

            # Look for aliens hitting the bottom of the screen.
            self._check_treat_bottom()

    def _cat_hit(self):
        """Respond to the cat being hit by a treat"""
        if self.stats.treats_left > 0:
            self.stats.treats_left -= 1
            self.treats.empty()
            self.bullets.empty()
            self._create_fleet()
            self.cat.center_cat()
            # Pause.
            time.sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _update_bullets(self):
        """Update the position of bullets and get rid of old bullets."""
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_treat_collisions()

        if not self.treats:
            # Destroy existing bullets and create new fleet.
            self.bullets.empty()
            self._create_fleet()

    def _check_bullet_treat_collisions(self):
        """Respond to bullet-treat collisions"""
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.treats, True, True)
        if collisions:
            for treats in collisions.values():
                self.stats.score += self.settings.treat_points * len(treats)
            self.sb.prep_score()
            self.sb.check_high_score()

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():  # Fix typo here
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player click Play."""
        if self.play_button.rect.collidepoint(mouse_pos) and not self.stats.game_active:
            # Reset the game statistics.
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()

            # Get rid of any remaining treats and bullets.
            self.treats.empty()
            self.bullets.empty()

            # Create a new fleet and center the cat.
            self._create_fleet()
            self.cat.center_cat()

            # Hide the mouse cursor
            pygame.mouse.set_visible(False)


    def _check_keydown_events(self, event):
        """Respond to keypresses"""
        if event.key ==        pygame.K_RIGHT:
            self.cat.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.cat.moving_left = True
        elif event.key == pygame.K_ESCAPE:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """Respond to key releases"""
        if event.key == pygame.K_RIGHT:
            self.cat.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.cat.moving_left = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_screen(self):
        """Update images on screen, and flip to the new screen."""
        self.screen.fill(self.bg_color)
        self.cat.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.treats.draw(self.screen)

        # Draw the score information.
        self.sb.show_score()

        # Draw the play button if the game is inactive.
        if not self.stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip()

    def _check_treat_bottom(self):
        """Check if any treats have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for treat in self.treats.sprites():
            if treat.rect.bottom >= screen_rect.bottom:
                # Treat this the same as if the ship got hit.
                self._cat_hit()
                break

if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = Rosebud()
    ai.run_game()

