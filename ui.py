from player import Player, PlayerAction, PlayerStatus
from game import PokerGame


def get_player_input(game: PokerGame) -> bool:
    player = game.players[game.active_player_index]
    
    if player.status != PlayerStatus.ACTIVE:
        return True
    
    print(f"\n{player.name}'s turn")
    print(f"Your cards: {[str(c) for c in player.hole_cards]}")
    
    # Calculate call amount
    call_amount = game.current_bet - player.bet_amount
    
    # Display available actions
    print("Available actions:")
    if call_amount == 0:
        print("1. Check")
        print("2. Bet")
    else:
        print("1. Fold")
        print("2. Call", call_amount)
        print("3. Raise")
    
    action_input = input("Enter choice: ")
    
    try:
        if call_amount == 0:
            if action_input == "1":
                return game.player_action(PlayerAction.CHECK)
            elif action_input == "2":
                amount = int(input("Enter bet amount: "))
                return game.player_action(PlayerAction.BET, amount)
        else:
            if action_input == "1":
                return game.player_action(PlayerAction.FOLD)
            elif action_input == "2":
                return game.player_action(PlayerAction.CALL)
            elif action_input == "3":
                amount = int(input(f"Enter total raise amount: "))
                return game.player_action(PlayerAction.RAISE, amount)
    except ValueError:
        print("Invalid input")
        return False
    
    print("Invalid choice")
    return False
