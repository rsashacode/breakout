import unittest
from unittest.mock import Mock, patch
import pygame
from sprites import Ball, Score
import settings

# Set up mocks for pygame that are used by all tests
pygame.font = Mock()
pygame.Surface = Mock()
pygame.Color = Mock()
pygame.font.Font.render = Mock(return_value=pygame.Surface())

class TestPygameSprites(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set up pygame mocks and initialization here, if needed
        pygame.init()
        cls.font = pygame.font.Font(None, 36)
        cls.color = pygame.Color(255, 255, 255)  # white color

    @classmethod
    def tearDownClass(cls):
        # Clean up pygame here, if needed
        pygame.quit()

    def setUp(self):
        # Set up objects that are common but might be modified by individual tests
        self.sprite_manager = Mock()
        self.sprite_groups = Mock()
        self.image = pygame.Surface((100, 50))
        self.rect = self.image.get_rect()

# Test cases for Ball
class TestBall(TestPygameSprites):
    def setUp(self):
        super().setUp()
        self.speed = settings.DEFAULT_BALL_SPEED  # Substitute with actual default speed
        self.ball = Ball(
            sprite_manager=self.sprite_manager,
            sprite_groups=self.sprite_groups,
            image=self.image,
            rect=self.rect,
            speed=self.speed
        )

    def test_initialization(self):
        """Test if the ball is initialized with the correct speed and direction."""
        self.assertEqual(self.ball.speed, self.speed)
        self.assertEqual(self.ball.direction, pygame.math.Vector2((0, -1)))

    def test_movement(self):
        """Test if the ball's position is updated correctly when moving."""
        initial_position = self.ball.position.copy()
        self.ball.direction = pygame.math.Vector2((1, 0))  # Move right
        self.ball.movement(1)  # Move for 1 second
        self.assertNotEqual(self.ball.position, initial_position)
        self.assertEqual(self.ball.position.x, initial_position.x + self.speed)
        self.assertEqual(self.ball.position.y, initial_position.y)

    def test_collision_with_walls(self):
        """Test if the ball bounces correctly when colliding with walls."""
        self.ball.rect.x = -5  # Simulate collision with the left wall
        self.ball.frame_collision()
        self.assertGreaterEqual(self.ball.rect.x, 0)
        self.assertEqual(self.ball.direction.x, 1)  # Direction should now be to the right

        self.ball.rect.y = -5  # Simulate collision with the top wall
        self.ball.frame_collision()
        self.assertGreaterEqual(self.ball.rect.y, 0)
        self.assertEqual(self.ball.direction.y, 1)  # Direction should now be downwards

    def test_update(self):
        """Test if the update method correctly manages the ball's behavior."""
        with patch.object(self.ball, 'movement'), \
             patch.object(self.ball, 'frame_collision'), \
             patch.object(self.ball, 'handle_collisions'):
            self.ball.update(1, Mock())  # Simulate 1 second of update with a mock for keys_pressed
            self.ball.movement.assert_called_once()
            self.ball.frame_collision.assert_called_once()
            self.ball.handle_collisions.assert_called_once()

# Test cases for Score
class TestScore(TestPygameSprites):
    def setUp(self):
        super().setUp()
        self.score = Score(
            sprite_manager=self.sprite_manager,
            sprite_groups=[Mock()],
            image=self.image,
            rect=self.rect,
            font=self.font,
            color=self.color
        )

    def test_initial_score(self):
        """Score should start at 0."""
        self.assertEqual(self.score.score, 0)

    def test_add_score(self):
        """Adding points to the score should increase it correctly."""
        self.score.add_score(10)
        self.assertEqual(self.score.score, 10)
        self.score.add_score(5)
        self.assertEqual(self.score.score, 15)

    def test_subtract_score(self):
        """Subtracting points should decrease the score correctly."""
        self.score.add_score(10)
        self.score.subtract_score(3)
        self.assertEqual(self.score.score, 7)

    def test_update(self):
        """Update should redraw the score with the current value."""
        self.score.score = 10
        self.score.update()
        self.font.render.assert_called_with('Score: 10', True, self.color)

class TestPlayer(unittest.TestCase):

    def setUp(self):
        self.sprite_manager = Mock()
        self.sprite_groups = Mock()
        self.image = pygame.Surface((50, 50))  # Assuming player image size is 50x50
        self.rect = pygame.Rect(0, 0, 50, 50)
        self.player = Player(
            sprite_manager=self.sprite_manager,
            sprite_groups=self.sprite_groups,
            image=self.image,
            rect=self.rect,
        )

    def test_initial_health(self):
        """Test if the player is initialized with maximum health."""
        self.assertEqual(self.player.health, settings.MAX_PLAYER_HEALTH)

    def test_loose_health(self):
        """Test if the player loses health correctly."""
        initial_health = self.player.health
        self.player.loose_health()
        self.assertEqual(self.player.health, initial_health - 1)

    def test_add_health(self):
        """Test if the player gains health correctly."""
        # Reduce health first to add later
        self.player.health = settings.MAX_PLAYER_HEALTH - 1
        self.player.add_health()
        self.assertEqual(self.player.health, settings.MAX_PLAYER_HEALTH)

    def test_check_screen_constraint(self):
        """Test if the player stays within screen bounds."""
        self.player.rect.right = settings.GAME_WINDOW_WIDTH + 10
        self.player.check_screen_constraint()
        self.assertEqual(self.player.rect.right, settings.GAME_WINDOW_WIDTH)

        self.player.rect.left = -10
        self.player.check_screen_constraint()
        self.assertEqual(self.player.rect.left, 0)

    def test_update(self):
        """Test if the player's state is updated correctly based on input."""
        # Assuming you have a method to simulate key presses
        keys_pressed = {pygame.K_RIGHT: True}
        delta_time = 0.016  # Approximate delta for 60 FPS
        self.player.update(delta_time, keys_pressed)
        # Check if player moved to the right
        self.assertGreater(self.player.rect.x, 0)

    def tearDown(self):
        # Any cleanup code if needed
        pass

if __name__ == '__main__':
    unittest.main()
