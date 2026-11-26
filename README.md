# Sudoku Arena: Human vs AI (Professional 3D Tactile Edition) 🎮⚡

**Sudoku Arena: Human vs AI** has been upgraded with a **luxury 3D tactile user interface**, **mechanical click feedback**, **procedural vector icons** (guaranteeing zero missing glyph boxes), **multi-screen navigation** (Welcome / Home, Levels, Game Arena), **dynamic Fullscreen**, and an **educational slow-motion AI visualizer** that shows candidate testing, failure detection (wrong numbers flashing in 3D red), and backtracking.

---

## 🌟 Visual & 3D Upgrades

### 1. Zero Broken Glyphs / Procedural Vector Icons
- **100% Procedural Rendering**: Eliminated all fragile Unicode symbols (such as `▶`, `⛶`, `◐`, `⌫`, `★`, `☆`, `💀`, `🤖`) that frequently caused missing character boxes (tofu rectangles) in system fonts.
- **Custom Vector Graphics Engine**:
  - Crisp Play, Pause, Step, Fullscreen, Theme, Home, Back, Hint bulb, Reset, and Backspace icons drawn natively via anti-aliased Pygame geometry.
  - Procedurally shaded 3D gold stars for level difficulty ratings.
  - Realistic hardware instrument LED jewel indicators that pulse with AI states.

### 2. Tactile 3D Mechanical Interface
- **Mechanical 3D Button Depth**:
  - Buttons possess real physical elevation with bottom drop shadows and top-edge light bevel highlights.
  - **Hover**: Button elevates toward the user (shadow expands).
  - **Click**: Button mechanically depresses into the panel surface by 4px, giving tactile feedback.
- **3D Recessed Grid Tray & Tiles**:
  - The 9x9 Sudoku board rests inside a beveled 3D tray with drop shadows.
  - Each cell is rendered like a physical 3D tile with bevel highlights.
  - 3x3 box divider lines feature recessed 3D grooves.
- **3D Recessed Gauge Displays**:
  - Timers and AI Telemetry boxes look like sunken physical instrument gauges with dark inner bevels.

### 3. Multi-Screen Experience
1. **🏠 Welcome / Home Page**:
   - 3D container panel with title: **SUDOKU ARENA: HUMAN VS AI**.
   - Tactile buttons: `PLAY GAME`, `SELECT DIFFICULTY`, `WATCH AI SOLVE (DEMO)`.
   - Utility controls: `THEME`, `FULLSCREEN`, and status footer.
2. **🎯 Levels Selection Page**:
   - 8 level cards arranged in a clean 4x2 grid with star difficulty ratings, clue counts, and descriptions:
     1. **Beginner** (60 Clues, ★☆☆☆☆)
     2. **Easy** (52 Clues, ★☆☆☆☆)
     3. **Medium** (44 Clues, ★★☆☆☆)
     4. **Hard** (38 Clues, ★★★☆☆)
     5. **Expert** (32 Clues, ★★★★☆)
     6. **Master** (27 Clues, ★★★★☆)
     7. **Grandmaster** (22 Clues, ★★★★★)
     8. **Impossible** (17 Clues, ★★★★★ 💀)
3. **⚔️ Game Arena**:
   - Top bar with `HOME`, `LEVELS`, Level Badge, `THEME`, and `SCREEN`.
   - Large 3D Sudoku board + tactile mechanical numpad keys (1-9 and DEL).
   - Right-side dashboard: Dual Timers, AI Telemetry with 3D LED indicator, Action controls (`AI SOLVE`, `STEP AI >`, `HINT (MRV)`, `RESET BOARD`, `NEW PUZZLE`), and Keyboard shortcuts.

### 4. Slow-Motion AI Visualizer (Mistakes & Backtracking)
- 🟡 **Candidate Testing (`TRY`)**: The AI places a candidate digit in **glowing 3D amber** with a live explanation.
- 🔴 **Mistake Revealing (`WRONG`)**: When downstream cells encounter a conflict, the cell flashes in **bright 3D CRIMSON RED**, highlighting the failed candidate so you can see the AI discover its mistake!
- 🔄 **Backtracking (`BACKTRACK`)**: The cell erases the digit and steps back up the search tree.
- 🟢 **Success (`SOLVED`)**: Flash confirmation across the board.
- **`[ STEP AI > ]` Button**: Manually advance the AI **one decision at a time** for step-by-step study.

---

## 🕹️ Controls & Shortcuts

| Input | Action |
| :--- | :--- |
| **`F11`** or `FULLSCREEN` | Toggle Fullscreen / Windowed Mode |
| **`T`** or `THEME` | Toggle Dark Mode / Light Mode |
| **`Mouse Click`** | Navigate screens, select cells, click tactile buttons, input digits via 3D numpad |
| **`Arrow Keys`** | Move active grid cell |
| **`1` – `9`** (or Numpad) | Place digit in active cell |
| **`Backspace` / `Del` / `0`** | Clear cell |
| **`H`** | Request instant MRV Hint |
| **`Space` / `S`** | Start or Pause AI Solver |
| **`N`** | Generate New Puzzle at current difficulty |
| **`R`** | Reset board to initial clues |

---

## 🚀 How to Run

Launch the game:
```bash
python main.py
```

Run the automated headless test suite:
```bash
python test_game.py
```
