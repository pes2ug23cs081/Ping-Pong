import pygame
from .paddle import Paddle
from .ball import Ball

# Game Engine

WHITE = (255, 255, 255)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)

        self.player_score = 0
        self.ai_score = 0
        
        # Font setup 
        self.score_font = pygame.font.SysFont("Arial", 30)
        self.game_over_font = pygame.font.SysFont("Arial", 60)
        self.menu_font = pygame.font.SysFont("Arial", 24)

        #Load sound effects
        try:
            self.paddle_sound = pygame.mixer.Sound("Assets/BallHit.wav")
            self.wall_sound = pygame.mixer.Sound("Assets/WallHit.wav")
            self.score_sound = pygame.mixer.Sound("Assets/Victory.wav")
        except pygame.error as e:
            print(f"Error loading sound file: {e}")
            # Create dummy sound objects if files are not found, so the game doesn't crash
            self.paddle_sound = pygame.mixer.Sound(buffer=b'')
            self.wall_sound = pygame.mixer.Sound(buffer=b'')
            self.score_sound = pygame.mixer.Sound(buffer=b'')


        # New state management 
        self.state = 'PLAYING' # Can be 'PLAYING' or 'GAME_OVER'
        self.winning_score = 5
        self.winner_text = ""
        self.should_exit = False # Flag to signal the main loop to exit

    def handle_input(self, event):
        """Handles single key press events, ideal for menus."""
        if self.state == 'GAME_OVER':
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_3:
                    self.reset_game(3)
                elif event.key == pygame.K_5:
                    self.reset_game(5)
                elif event.key == pygame.K_7:
                    self.reset_game(7)
                elif event.key == pygame.K_ESCAPE:
                    self.should_exit = True

    def handle_continuous_input(self):
        """Handles continuous key presses, ideal for movement."""
        if self.state == 'PLAYING':
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.player.move(-10, self.height)
            if keys[pygame.K_s]:
                self.player.move(10, self.height)

    def update(self):
        # Only update game objects if we are in the 'PLAYING' state
        if self.state == 'PLAYING':
            if self.ball.move():
                self.wall_sound.play()
            
            if self.ball.check_collision(self.player, self.ai):
                self.paddle_sound.play()

            if self.ball.x <= 0:
                self.ai_score += 1
                self.score_sound.play()
                self.ball.reset()
            elif self.ball.x >= self.width:
                self.player_score += 1
                self.score_sound.play()
                self.ball.reset()
            
            self.check_for_winner()
            self.ai.auto_track(self.ball, self.height)
    
    def check_for_winner(self):
        """Checks if a player has reached the winning score and changes state."""
        if self.player_score >= self.winning_score:
            self.winner_text = "Player Wins!"
            self.state = 'GAME_OVER'
        elif self.ai_score >= self.winning_score:
            self.winner_text = "AI Wins!"
            self.state = 'GAME_OVER'

    def render(self, screen):
        # Always draw the basic game elements
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width//2, 0), (self.width//2, self.height))

        # Draw score
        player_text = self.score_font.render(str(self.player_score), True, WHITE)
        ai_text = self.score_font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width//4, 20))
        screen.blit(ai_text, (self.width * 3//4, 20))

        # If the game is over, display the winner and replay menu
        if self.state == 'GAME_OVER':
            # Display winner text
            text_surface = self.game_over_font.render(self.winner_text, True, WHITE)
            text_rect = text_surface.get_rect(center=(self.width/2, self.height/3))
            screen.blit(text_surface, text_rect)
            
            # Display replay options
            self.draw_text(screen, "Press (3) for Best of 3", (self.width/2, self.height/2), self.menu_font)
            self.draw_text(screen, "Press (5) for Best of 5", (self.width/2, self.height/2 + 40), self.menu_font)
            self.draw_text(screen, "Press (7) for Best of 7", (self.width/2, self.height/2 + 80), self.menu_font)
            self.draw_text(screen, "Press (ESC) to Exit", (self.width/2, self.height/2 + 120), self.menu_font)

    def draw_text(self, screen, text, pos, font):
        """Helper function to draw centered text."""
        text_surface = font.render(text, True, WHITE)
        text_rect = text_surface.get_rect(center=pos)
        screen.blit(text_surface, text_rect)

    def reset_game(self, winning_score):
        """Resets the game state for a new match."""
        self.winning_score = winning_score
        self.player_score = 0
        self.ai_score = 0
        self.ball.reset()
        self.winner_text = ""
        self.state = 'PLAYING'

