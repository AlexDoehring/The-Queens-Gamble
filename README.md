# ♟️ The Queen's Gamble

**A chess-based strategy game with a blackjack twist.**  
Capture pieces by playing blackjack, earn currency, and upgrade your odds.  
Built during HackKU 2025 in 36 hours.

---

## 🎮 Gameplay Overview

- Standard chessboard with turn-based play.
- Player-initiated captures trigger a blackjack duel.
- Bot captures are resolved based on probability.
- Earn in-game currency for successful captures.
- Spend currency on upgrades to sabotage the bot or boost your chances.
- Risk-reward dynamics with special rules for **check**, **promotion**, and **busts**.

---

## 🃏 Key Mechanics

| Feature              | Description |
|----------------------|-------------|
| **Blackjack Battles** | Player vs Bot when attacking |
| **Bot Probability**   | Simulates blackjack odds using preset first cards |
| **Currency System**   | Earn money for successful captures, bonus if King is in check |
| **Shop Upgrades**     | Purchase tools to influence game flow (firewalls, retries, shields) |
| **Promotion Gambles** | Beat the promoted piece in blackjack to evolve your pawn |

---

## 🛠️ Tech Stack

- **Frontend**: [React.js / HTML5 Canvas / Your choice]
- **Backend**: [Flask / Node / Firebase / Your choice]
- **Libraries**: 
  - `chess.js`
  - Custom Blackjack Engine
  - [Any UI / Animation Libraries]

---

## 🖼️ Visual Theme

Retro arcade style with pixel art chess pieces and neon-lit card animations.  
Think: *chess club meets Vegas in the 80s*.

---

## 📦 Features to Add

- [ ] Multiplayer mode
- [ ] Advanced bot AI
- [ ] Music / SFX integration
- [ ] Game saving & leaderboard

---

## 🚀 How to Run

```bash
git clone https://github.com/your-username/queens-gamble.git
cd queens-gamble
npm install
npm start
```

## 👥 Team
Alex Doehring – Backend / Integration

Nicholas Holmes – Frontend / UI / Art / Logic

Brett Suhr – Game Design / Logic


Colin Treanor – Backend / Integration

## 💖 Special Thanks
Huge thank you to the HackKU 2025 organizers, mentors, and volunteers for putting together an incredible event and creating the space for innovation and (not-so) friendly competition. Your work made this all possible — we appreciate you!

