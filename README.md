# ♛ The Queen's Gamble: Chess × Blackjack

**The Queen’s Gamble** is a strategy-packed mashup of **classic chess** and **thrilling blackjack**. Every time you attempt to capture a piece, you must win a hand of blackjack to seal the deal. Whether you're a tactician or a risk-taker, this game challenges both brains and luck.

---

## 🎮 Game Features

- ♟️ **Classic Chess Engine**  
  Standard chess rules including legal moves, special cases like castling, en passant, and promotion.

- 🃏 **Blackjack Duels on Capture**  
  Try to take an opponent's piece? You'll have to win a mini blackjack round to confirm the capture.

- 🛒 **Upgrade & Power-Up Shop**  
  - **Upgrades**:  
    - `Luck`: Reduce AI’s chance of capturing your pieces.  
    - `Bounty`: Increases reward (money) when you capture pieces.  
  - **Power-Ups**:  
    - `T8kBack`: Undo your last move.  
    - `Redo`: Retry a lost blackjack round.  
    - `Skip`: Skip the opponent’s turn.

- 🤖 **AI Opponent**  
  A basic minimax-based AI plays as Black with probabilistic capturing logic that can be influenced by player upgrades.

- 🎲 **Custom Card-Deck Logic**  
  Fully functional deck shuffling, hand evaluation, and animated UI for blackjack.

- 🎨 **Themed UI & Sounds**  
  Multiple board themes, sound effects for moves and captures, and immersive blackjack visuals.

---

## 🧩 Project Structure

```
The-Queens-Gamble/
│
├── main.py                 # Main game loop
├── game.py                 # Overall game manager and integration
├── board.py                # Chess board and move logic
├── piece.py                # Piece definitions and stats (value, bounty, probability)
├── move.py                 # Move objects and validation
├── square.py               # Square definitions and logic
│
├── ai.py                   # Simple minimax AI
├── config.py               # Theme and sound configuration
├── theme.py / color.py     # Theme color configuration
├── const.py                # Constants for dimensions, UI
├── sound.py                # Sound playback wrapper
├── dragger.py              # Drag-and-drop logic for chess pieces
│
├── shop.py                 # Shop system and UI
├── upgrade.py              # Upgrade definitions
├── powerup.py              # Power-up definitions
│
├── blackjack.py            # Blackjack rules and flow
├── blackjack_ui.py         # UI for Blackjack mini-game
├── deck.py / card.py       # Card and deck management
│
├── assets/                 # Images and sounds
│   ├── images/
│   │   ├── blackjack/      # Blackjack-specific UI graphics
│   │   ├── shop/           # Shop UI elements
│   │   └── imgs-80px/      # Chess piece images
│   └── sounds/
│       ├── move.wav
│       └── capture.wav
│
└── README.md               # This file
```

---

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/AlexDoehring/The-Queens-Gamble
cd The-Queens-Gamble
```

### 2. Install Dependencies

Ensure Python 3.8+ is installed. Then install Pygame:

```bash
pip install pygame
```

### 3. Run the Game

```bash
python src/main.py
```

Make sure the `assets/` folder is intact and contains all images and sounds for proper visuals and gameplay.

---

## 🕹️ Controls & Gameplay

- **Drag and drop** chess pieces to play.
- Capturing a piece **triggers blackjack** — win the hand to confirm the capture.
- **Hit** or **Stand** using on-screen buttons.
- Use the **right panel shop** to buy upgrades or power-ups using in-game money.
- Press `R` to reset the game or `T` to change the board theme.

---

## 💰 Money System

- Start with **$15**.
- Earn more by winning blackjack duels and capturing pieces.
- Spend in the shop to improve your odds or manipulate gameplay.

| Upgrade | Effect |
|---------|--------|
| **Luck**   | Lowers AI capture probability |
| **Bounty** | Increases cash reward per capture |

| Power-Up | Effect |
|----------|--------|
| **T8kBack** | Undo your last move |
| **Redo**    | Retry a lost blackjack duel |
| **Skip**    | Skip the opponent’s turn |

---

## 🧠 AI Logic

- Plays as Black.
- Uses a depth-1 **minimax** algorithm to evaluate board state.
- Probabilistic capturing depends on the piece's built-in chance and your **Luck** upgrade.

---

## 📸 Screenshots

*Coming soon: UI previews and gameplay GIFs.*

---

## 🔮 Future Ideas

- Multiplayer support
- Smarter AI with adjustable difficulty
- Online matchmaking
- Additional card game modes
- Leaderboards and statistics

---

## 👑 Credits

Created by:

- Brett Suhr  
- Alex Doehring  
- Nicholas Holmes  
- Colin Treanor

---

## 📜 License

This project is © 2025 Brett Suhr, Alex Doehring, Nicholas Holmes, and Colin Treanor.  
All rights reserved. This code may not be copied, distributed, or modified without explicit permission.