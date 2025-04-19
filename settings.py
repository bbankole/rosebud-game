class Settings:
    """A class to store all settings for Rosebud"""

    def __init__(self):
        """Initialize the game's static settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (255, 215, 0)

        # Bullet settings
        self.bullet_speed = 2
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (135, 205, 250)
        self.bullets_allowed = 10

        # Treat settings
        self.treat_speed = 1.0
        self.fleet_drop_speed = 10

        self.speedup_scale = 1.1
        # Fleet direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

        self.treat_points = None

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.cat_speed = 1.5
        self.bullet_speed = 3.0
        self.treat_speed = 1.0

        # Fleet direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

        # Scoring
        self.treat_points = 50

        # Cat setting
        self.cat_speed = 1.7
        self.treat_limit = 3
        self.cat_limit = 3

    def increase_speed(self):
       """Increase speed settings and treats point values."""
       self.cat_speed *= self.speedup_scale
       self.bullet_speed *= self.speedup_scale
       self.treat_speed *= self.speedup_scale

       self.treat_points = int(self.treat_points * self.speedup_scale)
       print(self.treat_points)
