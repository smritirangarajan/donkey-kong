# Donkey Kong Classic (Python + Pygame)

A faithful recreation of the classic **Donkey Kong arcade game** built with Python and Pygame. Play as Mario, climb ladders, dodge barrels and flames, and rescue the princess from Donkey Kong!

## 🧠 Based On + Improvements

This project is based on a YouTube tutorial by **LeMaster Tech**:  
📺 [Watch the full video](https://www.youtube.com/watch?v=u6RV1lkHW8M&t=16372s)

I followed the structure and core mechanics shown in the tutorial, and then **optimized** and **refactored** the code to:

- Separate game logic into organized classes: `Player`, `Barrel`, `Flame`, `Ladder`, `Bridge`, `Hammer`
- Improve performance with surface caching
- Expand level support with a `levels_data.py` system
- Refactor main loop to reduce complexity and improve readability

---

## 🎮 Features

- Classic arcade-style platforming gameplay  
- Rolling barrels with edge detection and physics  
- Climbable ladders and multi-level platform layouts  
- Pick up hammers to destroy barrels  
- Animated characters: Mario, Donkey Kong, Peach, fireballs  
- Multiple level support (expandable!)  
- Score tracking, bonus timer, and extra lives  
- Pixel-perfect collision detection

---

## 🧠 How It Works

- **Player (Mario)** can move, jump, climb, and pick up hammers.
- **Barrels** spawn periodically, roll across platforms, and fall when there's no floor.
- **Flames** spawn from the oil drum and climb ladders randomly.
- **Hammers** give Mario temporary power to destroy barrels.
- **Victory condition** is reaching the top platform.

---

## 🛠️ Setup Instructions

```bash
git clone https://github.com/yourusername/donkey-kong-pygame.git
cd donkey-kong-pygame
Copy
Edit
pip install pygame
python main.py
