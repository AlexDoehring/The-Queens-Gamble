
# ♛ The Queen's Gamble: Chess × Blackjack

**The Queen’s Gamble** is a bold fusion of **classic chess strategy** and the **high-stakes thrill of blackjack**. Every attempted capture triggers a head-to-head card duel — brains meet luck in this one-of-a-kind experience. Whether you’re a sharp tactician or a high-roller, this game will test every facet of your gameplay.

---

## 🎮 Game Highlights

- ♟️ **Traditional Chess Engine**  
  Full chess ruleset, including special moves like castling, en passant, and pawn promotion.

- 🃏 **Blackjack Battles for Captures**  
  Think you’ve got that piece? Prove it — win a round of blackjack to confirm the capture.

- 🛍️ **In-Game Shop: Upgrades & Power-Ups**
  - **Upgrades**  
    - `Luck`: Decreases the AI’s chances of successfully capturing your pieces.  
    - `Bounty`: Boosts the money you earn from winning captures.
  - **Power-Ups**  
    - `T8kBack`: Undo your last chess move.  
    - `Redo`: Retry a lost blackjack duel.  
    - `Skip`: Skip the AI’s next move.

- 🤖 **AI Opponent**  
  A minimax-powered AI opponent with probabilistic capture logic that’s influenced by player upgrades.

- 🎨 **Immersive UI & Audio**  
  Dynamic board themes, authentic sound effects, and animated blackjack sequences bring the game to life.

---

## 🗂️ Project Structure

```
The-Queens-Gamble/
├── src/
│   ├── main.py               # Game entry point
│   ├── game.py               # Manages overall game state
│   ├── board.py              # Chess board + move rules
│   ├── piece.py              # Piece logic and attributes
│   ├── move.py               # Move validation
│   ├── square.py             # Tile logic
│   ├── ai.py                 # AI logic (minimax)
│   ├── config.py             # UI/Sound config
│   ├── theme.py / color.py   # Theme styling
│   ├── const.py              # UI constants
│   ├── sound.py              # Audio playback
│   ├── dragger.py            # Drag-and-drop handling
│   ├── shop.py               # Upgrade shop logic
│   ├── upgrade.py            # Upgrade definitions
│   ├── powerup.py            # Power-up logic
│   ├── blackjack.py          # Blackjack rules
│   ├── blackjack_ui.py       # Blackjack UI
│   ├── deck.py / card.py     # Card handling
│
├── assets/
│   ├── images/
│   │   ├── blackjack/        # Blackjack UI art
│   │   ├── shop/             # Shop visuals
│   │   └── imgs-80px/        # Piece sprites
│   └── sounds/
│       ├── move.wav
│       └── capture.wav
│
└── README.md
```

---

## 🛠️ How to Run

### 1. Clone the Repo

```bash
git clone https://github.com/AlexDoehring/The-Queens-Gamble
cd The-Queens-Gamble
```

### 2. Install Dependencies

Make sure you have **Python 3.8+** installed. Then run:

```bash
pip install pygame
```

### 3. Launch the Game

```bash
python src/main.py
```

Ensure the `assets/` directory remains intact — it contains vital images and sounds.

---

## 🎮 How to Play

- **Move pieces** by dragging and dropping.
- **Capturing a piece?** Win a blackjack round first!
- Use the **on-screen blackjack controls** to hit or stand.
- Access the **shop** on the side panel to buy upgrades and power-ups.
- Press `R` to restart the game or `T` to switch themes.

---

## 💸 Money System

- Begin with **$15**
- Earn money by winning blackjack duels and capturing pieces.
- Spend money in the shop to gain advantages.

| Upgrade  | Effect                             |
|----------|------------------------------------|
| Luck     | Lowers AI’s chance of capturing    |
| Bounty   | Increases payout per capture       |

| Power-Up | Effect                              |
|----------|-------------------------------------|
| T8kBack  | Undo your last move                 |
| Redo     | Retry a lost blackjack round        |
| Skip     | Skip the opponent’s next turn       |

---

## 🧠 AI Overview

- Plays as Black
- Uses a simple **depth-1 minimax algorithm**
- Incorporates randomness in capture attempts, influenced by your **Luck** stat

---

## 📸 Previews

*Coming soon: screenshots and gameplay GIFs!*

---

## 🌟 Future Features

- Multiplayer mode
- Smarter AI with difficulty levels
- Online matchmaking
- Alternate card game duels
- Leaderboards & player stats

---

## 👥 Team

Developed by:

- Brett Suhr  
- Alex Doehring  
- Nicholas Holmes  
- Colin Treanor

---

## 📜 License

© 2025 Brett Suhr, Alex Doehring, Nicholas Holmes, and Colin Treanor.  
All rights reserved. Redistribution or modification without permission is prohibited.
