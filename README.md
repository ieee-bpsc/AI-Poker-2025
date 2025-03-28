# Poker Engine, AI Poker 2025

## Overview
This project provides a framework for simulating poker games. It allows you to create custom poker players by extending a base Player class and overriding the action function. 

## Features
Standard Texas Hold 'Em poker with 52 cards (no jokers) except for some minor changes. The changes include:
- There is no side pot. This means that winning after going all in will also reward you with the raises made subsequently.
- There is only one blind.
- Aces are treated as either high or low depending on which gives a better hand.

## Getting Started

To get started with the Poker Engine, first clone the repository using:

```bash
git clone https://github.com/Tanish-0001/AI-Poker-2025.git
```

Then you can create a custom player by implementing a class that inherits from the base Player class, and implement the function ```action```. This function must return an action (of the type PlayerAction) and an amount. Your player instance must be created with the parameters name and stack. Note that if you are using ```__init__```, you must call ```super().__init__()``` with the parameters name and stack.

Optionally, if you would like to play poker yourself, you can use the ```InputPlayer``` player provided in baseplayers.py.
    

### Example

Here’s a simple example of how to create a custom player class:

```python
from player import Player, PlayerAction

class MyPlayer(Player):
    def __init__(self, name, stack, strategy="fold"):
        super().__init__(name, stack)
        self.strategy = strategy

    def action(self, game_state, action_history):
        # Implement your strategy here
        if self.strategy == "fold":
            return PlayerAction.FOLD, 0
        else:
            return PlayerAction.ALL_IN, self.stack
```

### Game State

The game state that ```action``` receives is structured in the following way:
1. Hole Cards' Index (suit order is spades, hearts, diamonds, clubs and rank order is 2, 3, ..., Q, K, Ace)
2. Community Cards' Index. 0 means not yet dealt
3. Pot
4. Current Raise Amount
5. Blind
6. Active Player Index
7. Number of players
8. Each player's stack
9. Hand number - Maintains a count of how many hands have been dealt at the table.

For example, here is a sample game_state:
```python
[16, 7, 0, 0, 0, 0, 0, 20, 20, 20, 3, 4, 1000, 1000, 980, 1000, 1]
```
Which means that the player has the cards with index 16 and 7 (which corresponds to the 4 of hearts and 7 of spades), the community cards are all unrevealed, the pot has $20, the current raise is $20 (which includes the blind), the blind is $20, the active player index is 3 (which means its the 4th player's turn), the number of players is 4 and they have $1000, $1000, $980, $1000 resepctively, and the game number is 1.

### Action History

The action history is a list of tuples consisting of the following data: (phase, name, action, amount). Here is a sample action history:
```python
[('pre-flop', 'David', 'call', 20),
('pre-flop', 'Alice', 'raise', 60),
('pre-flop', 'Bob', 'fold', 0),
('pre-flop', 'Charlie', 'fold', 0),
('pre-flop', 'David', 'call', 40),
('flop', 'David', 'check', 0),
('flop', 'Alice', 'check', 0)]
```
Note that the action history does not include posting of the blind. The above action history follows a game where Charlie posts a blind of 20, followed by David calling 20, Alice raising to 60, Bob folding, Charlie folding, David calling 40, David checking, Alice checking.

Note: If you find any bugs, please e-mail them to ieee.sb@pilani.bits-pilani.ac.in
