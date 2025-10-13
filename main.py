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
    # The main loop now runs until the engine signals it to stop
    while not engine.should_exit:
        SCREEN.fill(BLACK)
        
        # --- Event handling is now passed to the engine ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                engine.should_exit = True
            # The engine will handle key presses based on game state
            engine.handle_input(event)
        
        # Handle continuous movement separately
        engine.handle_continuous_input()

        engine.update()
        engine.render(SCREEN)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()

