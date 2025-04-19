class GameStats:
    """Track statistics for Rosebud"""

    def __init__(self, ai_game):
        """Initialize statistics."""
        self.settings = ai_game.settings
        self.reset_stats()

        # Start Rosebud in an inactive status
        self.game_active = False

        # High score should never be reset
        self.high_score = 0

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.treats_left = self.settings.treat_limit
        self.cats_left = self.settings.cat_limit
        self.score = 0
        self.level = 1
