from player import Player
from game import PokerGame, GamePhase
from ui import get_player_input


def run_demo_game():
    # Create players
    players = [
        Player("Alice", 1000),
        Player("Bob", 1000),
        Player("Charlie", 1000),
        Player("Dave", 1000),
    ]
    
    # Create game
    game = PokerGame(players, big_blind=20)
    
    # Run a few hands
    for _ in range(3):
        game.start_new_hand()
        
        # Main game loop
        while game.phase != GamePhase.SHOWDOWN:
            if not get_player_input(game):
                continue
        
        print("\nHand complete. Press Enter for next hand...")
        input()


if __name__ == "__main__":
    run_demo_game()