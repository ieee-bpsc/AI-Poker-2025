import os
import sys
import os
import time
from player import PlayerStatus, PlayerAction
from game import PokerGame, GamePhase
from baseplayers import InputPlayer


def run_game(num_hands):

    players = [
        InputPlayer("Alice", 1000),
        InputPlayer("Bob", 1000),
        InputPlayer("Charlie", 1000),
        InputPlayer("David", 1000)
    ]
    
    # Create game
    game = PokerGame(players, big_blind=20)

    # Run several hands
    for _ in range(num_hands):
        print(f"\nHand number {game.hand_number + 1}")
        game_status = game.start_new_hand()
        if not game_status:
            print(f"Not enough players left in the game... game over.")
            break
        
        # Main game loop
        num_tries = 0
        while game.phase != GamePhase.SHOWDOWN:
            if num_tries == 3:
                game.player_action(PlayerAction.FOLD, 0)
                num_tries = 0
                continue

            player = game.players[game.active_player_index]

            if game.num_active_players() == 1 and player.bet_amount == game.current_bet:
                game.advance_game_phase()
                game.display_game_state()
                continue

            print(f"\n{player.name}'s turn")
            print(f"Your cards: {[str(c) for c in player.hole_cards]}")

            try:
                is_successful = game.get_player_input()
            except Exception as e:
                print(f"Player {player.name}'s turn failed: {e}")
                is_successful = False

            if not is_successful:
                print("Invalid command received.")
                num_tries += 1
            else:
                num_tries = 0
            time.sleep(.5)

        print("\nHand complete. Starting new hand...")
        # time.sleep(5)

    print("Winners are:")
    for g, winner, winning in game.hand_winners:
        print(f"Game {g}: {winner} ({winning})")
    print("\nFinal stack sizes are:")
    for player in game.players:
        print(f"{player.name}: ${player.stack}")


if __name__ == "__main__":
    start_time = time.time()
    with open("logs_1.txt", "w", encoding="utf-8") as f:
        sys.stdout = f
        run_game(40)

    sys.stdout = sys.__stdout__
    end_time = time.time()
    print("Game over. Total time taken:", end_time - start_time)
