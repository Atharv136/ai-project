# Sudoku Arena: Human vs AI (Web & Desktop Edition) 🎮⚡

**Sudoku Arena: Human vs AI** is a modern, luxury-grade Sudoku experience equipped with:
- **Direct 1-Click Vercel Deployment** (Zero env vars, zero build steps, instant loading on phones, tablets, and desktops)
- **Local Desktop Pygame Application** (`main.py`)
- **Tactile 3D Physical UI** with mechanical button depression and recessed instrument displays
- **100% Procedural Vector Icons** (Zero broken Unicode boxes or missing glyphs)
- **Multi-Screen Flow**: Welcome / Home Page, Levels Page (8 Tiers), and Game Arena
- **Educational Slow-Motion AI Visualizer**: Exposes candidate testing, mistake detection (cell flashes in 3D crimson red), and backtracking
- **Instant Hint System** powered by Minimum Remaining Values (MRV) heuristic
- **Dynamic 3D Dark & Light Themes**

---

## 🚀 How to Deploy on Vercel (Easiest Method - 30 Seconds)

Because this web version is built with pure, self-contained modern HTML5/CSS/JavaScript with zero backend dependencies:

### Method A: Via Vercel Web Dashboard (Drag-and-Drop or GitHub)
1. Push this folder to a GitHub repository (or use the Vercel CLI).
2. Go to **[vercel.com](https://vercel.com/)** and click **"Add New Project"**.
3. Import your repository.
4. **Environment Variables**: Leave blank (none required!).
5. **Build Command & Output Directory**: Leave default (it automatically serves `index.html`).
6. Click **"Deploy"**! Your game is live in seconds with a shareable URL.

### Method B: Via Vercel CLI
From your terminal in this directory:
```bash
npx vercel
```
Follow the prompts (press Enter for defaults) and it will immediately deploy live!

---

## 💻 How to Run Locally

### 1. Run the Web Version (In Your Browser)
You can open `index.html` directly in any web browser, or serve it with Python:
```bash
python -m http.server 3000
```
Then visit `http://localhost:3000`.

### 2. Run the Native Desktop Pygame Version
```bash
python main.py
```

### 3. Run Automated Verification Tests
- **Web Engine Tests**: `node test_web.js`
- **Pygame Desktop Tests**: `python test_game.py`

---

## 🕹️ Controls & Keyboard Shortcuts

| Input | Action |
| :--- | :--- |
| **`F11`** or `FULLSCREEN` | Toggle Fullscreen / Windowed Mode |
| **`T`** or `THEME` | Toggle Dark Mode / Light Mode |
| **`Mouse / Touch`** | Select cells, click 3D tactile buttons, input numbers via on-screen numpad |
| **`Arrow Keys`** | Move active grid selection |
| **`1` – `9`** (or Numpad) | Place digit in active cell |
| **`Backspace` / `Del` / `0`** | Clear cell |
| **`H`** | Request instant MRV Hint |
| **`Space` / `S`** | Start or Pause AI Visual DFS Solver |
| **`N`** | Generate New Puzzle at current tier |
| **`R`** | Reset board to initial clues |

---

## 🧠 AI & CSP Architecture

1. **Depth-First Search (DFS) with Backtracking Generator**:
   - Implemented as a non-blocking coroutine generator (`*visualDFSGenerator` in JS, `yield` in Python).
   - Allows the browser or desktop event loop to run smoothly at 60 FPS while the AI explores choices.
   - Highlights wrong digits in vivid 3D crimson red before erasing and backtracking.
2. **Minimum Remaining Values (MRV) Heuristic**:
   - "Fail-first" CSP heuristic that finds guaranteed correct hint digits instantaneously.
3. **8 Difficulty Tiers (Isomorphic Symmetries)**:
   - Uses minimal 17-clue basis transformed through the $1.2 \times 10^{12}$ isomorphic symmetry group (digit permutations, band/stack swaps, transpose).
