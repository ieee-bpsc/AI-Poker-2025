from enum import Enum
from typing import List, Tuple, Optional
from dataclasses import dataclass
from card import Card


class PlayerAction(Enum):
    FOLD = "fold"
    CHECK = "check"
    CALL = "call"
    BET = "bet"
    RAISE = "raise"
    ALL_IN = "all-in"


class PlayerStatus(Enum):
    ACTIVE = "active"
    FOLDED = "folded"
    ALL_IN = "all-in"
    OUT = "out"


@dataclass
class Player:
    name: str
    stack: int
    status: PlayerStatus = PlayerStatus.ACTIVE
    hole_cards: List[Card] = None
    bet_amount: int = 0
    
    def __post_init__(self):
        if self.hole_cards is None:
            self.hole_cards = []
    
    def reset_for_new_hand(self):
        self.hole_cards = []
        self.status = PlayerStatus.ACTIVE if self.stack > 0 else PlayerStatus.OUT
        self.bet_amount = 0
    
    def can_make_action(self) -> bool:
        return self.status in [PlayerStatus.ACTIVE]
    
    def take_action(self, action: PlayerAction, amount: int = 0) -> Tuple[PlayerAction, int]:
        if action == PlayerAction.FOLD:
            self.status = PlayerStatus.FOLDED
            return action, 0
        
        if action in [PlayerAction.BET, PlayerAction.RAISE, PlayerAction.CALL]:
            # Calculate maximum possible bet
            max_bet = min(amount, self.stack)
            
            # Update stack and bet amount
            self.stack -= max_bet
            self.bet_amount += max_bet
            
            # Check if player is all-in
            if self.stack == 0:
                self.status = PlayerStatus.ALL_IN
                return PlayerAction.ALL_IN, max_bet
            
            return action, max_bet
        
        return action, 0