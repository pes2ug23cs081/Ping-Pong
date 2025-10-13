import pygame
from game.game_engine import GameEngine

# Initialize pygame/Start application
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong - Pygame Version")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Game loop
engine = GameEngine(WIDTH, HEIGHT)

def main():
    running = True
    while running:
        SCREEN.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        engine.handle_input()
        engine.update()
        engine.render(SCREEN)

        # If the game is over, show the final screen for a moment
        if engine.game_over:
            pygame.display.flip()  
            pygame.time.wait(3000) # Wait for 3 seconds 
            running = False        # Exit the main loop
        else:
            pygame.display.flip()  # Otherwise, just update the display normally
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
