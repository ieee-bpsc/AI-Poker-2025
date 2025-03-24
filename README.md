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

Note: If you find any bugs, please e-mail them to ieee.sb@pilani.bits-pilani.ac.in
