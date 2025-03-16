from enum import Enum
from typing import List
from card import Card, Deck
from player import Player, PlayerAction, PlayerStatus
from hand_evaluator import HandEvaluator


class GamePhase(Enum):
    SETUP = "setup"
    PRE_FLOP = "pre-flop"
    FLOP = "flop"
    TURN = "turn"
    RIVER = "river"
    SHOWDOWN = "showdown"


class PokerGame:
    def __init__(self, players: List[Player], big_blind: int):
        self.players = players
        self.big_blind = big_blind
        self.deck = None
        self.community_cards = []
        self.pot = 0
        self.current_bet = 0
        self.phase = GamePhase.SETUP
        self.button_position = 0
        self.active_player_index = 0
        self.min_raise = big_blind
        self.has_played = [False] * len(self.players)

    def start_new_hand(self):
        print("\n====== NEW HAND ======")
        # Reset game state
        self.deck = Deck()
        self.community_cards = []
        self.pot = 0
        self.current_bet = 0
        self.phase = GamePhase.SETUP
        self.min_raise = self.big_blind

        # Reset player statuses
        for i, player in enumerate(self.players):
            player.reset_for_new_hand()
            self.has_played[i] = False if player.status == PlayerStatus.ACTIVE else True

        # Move button to next player
        self.button_position = (self.button_position + 1) % len(self.players)

        # Deal cards
        self._deal_hole_cards()

        # Post blinds
        self._post_blinds()

        # Begin pre-flop betting
        self.phase = GamePhase.PRE_FLOP
        self.active_player_index = (self.button_position + 2) % len(self.players)
        self._adjust_active_player_index()

        # Show game state
        self._display_game_state()

    def _deal_hole_cards(self):
        for player in self.players:
            if player.status != PlayerStatus.OUT:
                player.hole_cards = self.deck.deal(2)

    def _post_blinds(self):
        # Big blind only, no small blind
        bb_position = (self.button_position + 1) % len(self.players)
        bb_player = self.players[bb_position]

        if bb_player.stack > 0:
            action, amount = bb_player.take_action(PlayerAction.BET, self.big_blind)
            self.pot += amount
            self.current_bet = amount
            print(f"{bb_player.name} posts big blind: {amount}")

    def _adjust_active_player_index(self):
        # Find next active player
        original_index = self.active_player_index
        while not self.players[self.active_player_index].can_make_action():
            self.active_player_index = (self.active_player_index + 1) % len(self.players)
            if self.active_player_index == original_index:
                # We've gone all the way around, no active players
                return False
        return True

    def player_action(self, action: PlayerAction, amount: int = 0) -> bool:
        player = self.players[self.active_player_index]

        # Validate action
        if action == PlayerAction.CHECK and self.current_bet > player.bet_amount:
            print(f"Cannot check when there's a bet. Current bet: {self.current_bet}")
            return False

        if action == PlayerAction.CALL:
            amount = self.current_bet - player.bet_amount

        if action in [PlayerAction.BET, PlayerAction.RAISE]:
            if self.current_bet == 0:
                min_amount = 1  
                action = PlayerAction.BET
            else:
                min_amount = self.current_bet
                action = PlayerAction.RAISE

            if amount < min_amount:
                print(f"Minimum {action.value} is {min_amount}")
                return False

            # Update minimum raise
            self.min_raise = amount - self.current_bet

            # Update current bet
            self.current_bet = amount

        # Execute action
        print(f"{player.name} {action.value}s", end="")
        if action in [PlayerAction.BET, PlayerAction.RAISE, PlayerAction.CALL]:
            print(f" {amount}")
        else:
            print()

        actual_action, actual_amount = player.take_action(action, amount)
        self.pot += actual_amount

        # Move to next player
        self.has_played[self.active_player_index] = True
        self.active_player_index = (self.active_player_index + 1) % len(self.players)

        # Check if betting round is complete
        if self._is_betting_round_complete():
            self._advance_game_phase()
        else:
            self._adjust_active_player_index()

        # Show updated game state
        self._display_game_state()
        return True

    def _is_betting_round_complete(self) -> bool:
        active_players = [p for p in self.players if p.status in [PlayerStatus.ACTIVE, PlayerStatus.ALL_IN]]

        # If only one active player (others folded), round is complete
        if len([p for p in active_players if p.status == PlayerStatus.ACTIVE]) <= 1:
            return True

        # If every active player has had a chance to act at least once
        if all(p.bet_amount == self.current_bet or p.status != PlayerStatus.ACTIVE for p in active_players):
            if self.active_player_index == (self.button_position + 1) % len(self.players):
                return True
        
        return False

    def _advance_game_phase(self):
        # Reset bet amounts for the next betting round
        for player in self.players:
            player.bet_amount = 0
        self.current_bet = 0
        self.min_raise = self.big_blind

        # Move to the next phase
        if self.phase == GamePhase.PRE_FLOP:
            self.phase = GamePhase.FLOP
            self.community_cards.extend(self.deck.deal(3))
        elif self.phase == GamePhase.FLOP:
            self.phase = GamePhase.TURN
            self.community_cards.extend(self.deck.deal(1))
        elif self.phase == GamePhase.TURN:
            self.phase = GamePhase.RIVER
            self.community_cards.extend(self.deck.deal(1))
        elif self.phase == GamePhase.RIVER:
            self.phase = GamePhase.SHOWDOWN
            self._showdown()
            return

        # Start betting with player after button
        self.active_player_index = (self.button_position + 1) % len(self.players)
        self._adjust_active_player_index()
        self._reset_has_played()

    def _showdown(self):
        # Evaluate hands for all players who haven't folded
        active_players = [p for p in self.players if p.status != PlayerStatus.FOLDED]

        if len(active_players) == 1:
            # Only one player left, they win automatically
            winner = active_players[0]
            winner.stack += self.pot
            print(f"{winner.name} wins {self.pot} chips")
            return

        # Evaluate hands
        results = []
        print("\n=== SHOWDOWN ===")
        for player in active_players:
            result = HandEvaluator.evaluate_hand(player.hole_cards, self.community_cards)
            results.append((player, result))

            print(f"{player.name}: {[str(c) for c in player.hole_cards]} - {result.hand_rank.name}")

        # Find the winner(s)
        results.sort(key=lambda x: (x[1].hand_rank.value, x[1].hand_value), reverse=True)
        best_result = results[0][1]

        winners = []
        for player, result in results:
            if (result.hand_rank == best_result.hand_rank and
                    result.hand_value == best_result.hand_value):
                winners.append(player)

        # Distribute the pot
        split_amount = self.pot // len(winners)
        remainder = self.pot % len(winners)

        for player in winners:
            winnings = split_amount
            if remainder > 0:
                winnings += 1
                remainder -= 1

            player.stack += winnings
            print(f"{player.name} wins {winnings} chips with {best_result.hand_rank.name}")

    def _display_game_state(self):
        print(f"\nPhase: {self.phase.value}")
        print(f"Pot: {self.pot}")

        if self.community_cards:
            print(f"Community cards: {[str(c) for c in self.community_cards]}")

        print("\nPlayers:")
        for i, player in enumerate(self.players):
            position = ""
            if i == self.button_position:
                position = "(BTN)"

            cards = "[hidden]"
            if player.status == PlayerStatus.FOLDED:
                cards = "folded"
            elif player.status == PlayerStatus.OUT:
                cards = "out"

            active = "→ " if i == self.active_player_index and player.can_make_action() else "  "

            print(f"{active}{player.name} {position}: ${player.stack} {cards} {player.status.value}")

    def _reset_has_played(self):
        self.has_played = [False if player.status == PlayerStatus.ACTIVE else True for player in self.players]
