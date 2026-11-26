/**
 * Sudoku Arena: Human vs AI (Web Edition)
 * ========================================
 * 100% Client-Side Pure JavaScript Architecture
 * - Zero Backend / Zero Env Vars Required -> Direct 1-Click Vercel Deploy!
 * - True JS Generator (*visualDFSGenerator) for non-blocking educational slow AI
 * - Minimum Remaining Values (MRV) Heuristic Solver
 * - 8 Mathematically verified difficulty tiers (60 to 17 minimal clues)
 * - 3D Tactile UI with Physical Click Depressions
 */

"use strict";

// ---------------------------------------------------------------------------
// 1. SUDOKU SOLVER: MRV HEURISTIC & SLOW STEP-BY-STEP DFS GENERATOR
// ---------------------------------------------------------------------------
class SudokuSolver {
  static getCandidates(board, r, c) {
    if (board[r][c] !== 0) return new Set();
    const used = new Set(board[r]);
    for (let i = 0; i < 9; i++) {
      used.add(board[i][c]);
    }
    const br = Math.floor(r / 3) * 3;
    const bc = Math.floor(c / 3) * 3;
    for (let i = 0; i < 3; i++) {
      for (let j = 0; j < 3; j++) {
        used.add(board[br + i][bc + j]);
      }
    }
    const legal = new Set();
    for (let d = 1; d <= 9; d++) {
      if (!used.has(d)) legal.add(d);
    }
    return legal;
  }

  static isValidPlacement(board, r, c, val) {
    for (let i = 0; i < 9; i++) {
      if (i !== c && board[r][i] === val) return false;
      if (i !== r && board[i][c] === val) return false;
    }
    const br = Math.floor(r / 3) * 3;
    const bc = Math.floor(c / 3) * 3;
    for (let i = 0; i < 3; i++) {
      for (let j = 0; j < 3; j++) {
        const nr = br + i;
        const nc = bc + j;
        if ((nr !== r || nc !== c) && board[nr][nc] === val) return false;
      }
    }
    return true;
  }

  static findAllConflicts(board) {
    const conflicts = new Set();
    // Rows
    for (let r = 0; r < 9; r++) {
      const seen = {};
      for (let c = 0; c < 9; c++) {
        const val = board[r][c];
        if (val !== 0) {
          if (val in seen) {
            conflicts.add(`${r},${c}`);
            conflicts.add(`${r},${seen[val]}`);
          } else {
            seen[val] = c;
          }
        }
      }
    }
    // Columns
    for (let c = 0; c < 9; c++) {
      const seen = {};
      for (let r = 0; r < 9; r++) {
        const val = board[r][c];
        if (val !== 0) {
          if (val in seen) {
            conflicts.add(`${r},${c}`);
            conflicts.add(`${seen[val]},${c}`);
          } else {
            seen[val] = r;
          }
        }
      }
    }
    // 3x3 Blocks
    for (let br = 0; br < 9; br += 3) {
      for (let bc = 0; bc < 9; bc += 3) {
        const seen = {};
        for (let i = 0; i < 3; i++) {
          for (let j = 0; j < 3; j++) {
            const r = br + i;
            const c = bc + j;
            const val = board[r][c];
            if (val !== 0) {
              if (val in seen) {
                conflicts.add(`${r},${c}`);
                conflicts.add(seen[val]);
              } else {
                seen[val] = `${r},${c}`;
              }
            }
          }
        }
      }
    }
    return conflicts;
  }

  static solveMRV(board) {
    const b = board.map(row => [...row]);

    function _solve(current) {
      const emptyCells = [];
      for (let r = 0; r < 9; r++) {
        for (let c = 0; c < 9; c++) {
          if (current[r][c] === 0) {
            const cands = SudokuSolver.getCandidates(current, r, c);
            if (cands.size === 0) return null; // Domain wipeout
            emptyCells.push({ r, c, cands: Array.from(cands).sort((x, y) => x - y) });
          }
        }
      }
      if (emptyCells.length === 0) return current;

      // MRV: Pick variable with fewest remaining legal values
      emptyCells.sort((a, b) => a.cands.length - b.cands.length);
      const { r, c, cands } = emptyCells[0];

      for (const val of cands) {
        current[r][c] = val;
        const res = _solve(current);
        if (res !== null) return res;
        current[r][c] = 0;
      }
      return null;
    }

    return _solve(b);
  }

  /**
   * Educational Step-by-Step AI Visualizer (JavaScript Generator)
   * Deliberately yields TRY, WRONG (cell flashes red), and BACKTRACK.
   */
  static *visualDFSGenerator(board, emptyCells, stats) {
    function* _dfsStep(idx) {
      if (idx >= emptyCells.length) {
        yield { state: "SOLVED", r: null, c: null, val: null, msg: "PUZZLE SOLVED: All constraints satisfied!" };
        return true;
      }

      const { r, c } = emptyCells[idx];

      for (let digit = 1; digit <= 9; digit++) {
        if (SudokuSolver.isValidPlacement(board, r, c, digit)) {
          // 1. TRY candidate
          board[r][c] = digit;
          stats.explored++;
          yield { state: "TRY", r, c, val: digit, msg: `TESTING candidate ${digit} at Row ${r + 1}, Col ${c + 1}` };

          // Recursive search downstream
          const solved = yield* _dfsStep(idx + 1);
          if (solved) return true;

          // 2. WRONG: Downstream failed -> flash cell in RED!
          stats.backtracks++;
          yield { state: "WRONG", r, c, val: digit, msg: `DEAD END! Candidate ${digit} at Row ${r + 1}, Col ${c + 1} failed downstream.` };

          // 3. BACKTRACK: Erase and revert
          board[r][c] = 0;
          yield { state: "BACKTRACK", r, c, val: 0, msg: `BACKTRACK: Erased (${r + 1}, ${c + 1}) to test next candidate.` };
        }
      }
      return false;
    }

    const hasSolution = yield* _dfsStep(0);
    if (!hasSolution) {
      yield { state: "UNSOLVABLE", r: null, c: null, val: null, msg: "No valid solution exists for this board." };
    }
  }
}

// ---------------------------------------------------------------------------
// 2. SUDOKU GENERATOR: 8 TIERS & ISOMORPHIC SYMMETRIES
// ---------------------------------------------------------------------------
class SudokuGenerator {
  static DIFFICULTY_TIERS = [
    { id: 0, name: "Beginner", clues: 60, stars: 1, desc: "Gentle warmup, ample clues" },
    { id: 1, name: "Easy", clues: 52, stars: 1, desc: "Casual logical solving" },
    { id: 2, name: "Medium", clues: 44, stars: 2, desc: "Standard balanced puzzle" },
    { id: 3, name: "Hard", clues: 38, stars: 3, desc: "Advanced candidate filtering" },
    { id: 4, name: "Expert", clues: 32, stars: 4, desc: "Complex elimination chains" },
    { id: 5, name: "Master", clues: 27, stars: 4, desc: "Sparse clues, deep logic" },
    { id: 6, name: "Grandmaster", clues: 22, stars: 5, desc: "Extreme deductive challenge" },
    { id: 7, name: "Impossible", clues: 17, stars: 5, desc: "17-Clue minimal boundary" },
  ];

  static BASE_17_STR = "000000010400000000020000000000050407008000300001090000300400200050100000000806000";
  static _BASE_SOL = null;

  static applyIsomorphism(board) {
    let b = board.map(row => [...row]);

    // 1. Permute digits 1..9
    const mapping = [1, 2, 3, 4, 5, 6, 7, 8, 9];
    for (let i = mapping.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [mapping[i], mapping[j]] = [mapping[j], mapping[i]];
    }
    const digitMap = { 0: 0 };
    for (let i = 0; i < 9; i++) digitMap[i + 1] = mapping[i];
    b = b.map(row => row.map(cell => digitMap[cell]));

    // 2. Permute rows within bands
    for (let band = 0; band < 9; band += 3) {
      const rows = [0, 1, 2].sort(() => Math.random() - 0.5);
      const bandRows = [b[band + rows[0]], b[band + rows[1]], b[band + rows[2]]];
      for (let r = 0; r < 3; r++) b[band + r] = bandRows[r];
    }

    // 3. Permute columns within stacks
    for (let stack = 0; stack < 9; stack += 3) {
      const cols = [0, 1, 2].sort(() => Math.random() - 0.5);
      for (let r = 0; r < 9; r++) {
        const orig = [b[r][stack], b[r][stack + 1], b[r][stack + 2]];
        for (let c = 0; c < 3; c++) b[r][stack + c] = orig[cols[c]];
      }
    }

    // 4. Random reflection (transposition)
    if (Math.random() < 0.5) {
      const transposed = [];
      for (let r = 0; r < 9; r++) {
        transposed.push([]);
        for (let c = 0; c < 9; c++) {
          transposed[r].push(b[c][r]);
        }
      }
      b = transposed;
    }

    return b;
  }

  static createPuzzle(tierId) {
    const tier = this.DIFFICULTY_TIERS[tierId];
    const targetClues = tier.clues;

    // Load base 17 minimal basis
    const raw17 = [];
    for (let r = 0; r < 9; r++) {
      raw17.push([]);
      for (let c = 0; c < 9; c++) {
        raw17[r].push(parseInt(this.BASE_17_STR[r * 9 + c], 10));
      }
    }

    if (!this._BASE_SOL) {
      this._BASE_SOL = SudokuSolver.solveMRV(raw17);
    }

    const extraCluesNeeded = targetClues - 17;
    const emptyCells = [];
    for (let r = 0; r < 9; r++) {
      for (let c = 0; c < 9; c++) {
        if (raw17[r][c] === 0) emptyCells.push({ r, c });
      }
    }

    // Shuffle and pick revealed coords
    emptyCells.sort(() => Math.random() - 0.5);
    const revealed = emptyCells.slice(0, extraCluesNeeded);

    const baseBoard = raw17.map(row => [...row]);
    for (const { r, c } of revealed) {
      baseBoard[r][c] = this._BASE_SOL[r][c];
    }

    const puzzle = this.applyIsomorphism(baseBoard);
    const solution = SudokuSolver.solveMRV(puzzle);
    return { puzzle, solution };
  }
}

// ---------------------------------------------------------------------------
// 3. MAIN WEB APPLICATION CONTROLLER
// ---------------------------------------------------------------------------
class SudokuArenaApp {
  constructor() {
    this.currentScreen = "home";
    this.currentTier = 2; // Medium (44 clues)
    this.puzzle = null;
    this.solution = null;
    this.board = null;
    this.cellTypes = {}; // 'initial', 'user', 'hint', 'ai'
    this.selectedCell = { r: 0, c: 0 };
    this.conflicts = new Set();

    // AI Solver & Generator
    this.aiRunning = false;
    this.aiGenerator = null;
    this.aiStats = { explored: 0, backtracks: 0 };
    this.aiSpeedId = "ultra_slow";
    this.aiSpeeds = {
      ultra_slow: { name: "0.6s", interval: 600 },
      slow: { name: "0.25s", interval: 250 },
      medium: { name: "0.08s", interval: 80 },
      fast: { name: "FAST", interval: 20 },
      instant: { name: "MAX", interval: 0 },
    };
    this.aiTimerHandle = null;

    // Timers
    this.humanTime = 0.0;
    this.aiTime = 0.0;
    this.isHumanActive = true;
    this.clockInterval = null;
    this.gameWon = false;

    this.initDOM();
    this.bindEvents();
    this.loadNewPuzzle(this.currentTier);
  }

  initDOM() {
    // Screens
    this.screenHome = document.getElementById("screen-home");
    this.screenLevels = document.getElementById("screen-levels");
    this.screenGame = document.getElementById("screen-game");

    // Board & Gauges
    this.boardEl = document.getElementById("sudoku-board");
    this.timerHumanEl = document.getElementById("timer-human");
    this.timerAiEl = document.getElementById("timer-ai");
    this.currentTierBadge = document.getElementById("current-tier-badge");
    this.homeFooterTier = document.getElementById("home-footer-tier");

    // AI Telemetry
    this.aiDisplayBox = document.getElementById("ai-display-box");
    this.aiLed = document.getElementById("ai-led");
    this.aiStatusMsg = document.getElementById("ai-status-msg");
    this.statExplored = document.getElementById("stat-explored");
    this.statBacktracks = document.getElementById("stat-backtracks");
    this.statRatio = document.getElementById("stat-ratio");

    // Buttons
    this.btnAiSolve = document.getElementById("btn-ai-solve");
    this.solveIcon = document.getElementById("solve-icon");
    this.solveText = document.getElementById("solve-text");
    this.btnAiStep = document.getElementById("btn-ai-step");
    this.btnHint = document.getElementById("btn-hint");
    this.btnReset = document.getElementById("btn-reset");
    this.btnNewPuzzle = document.getElementById("btn-new-puzzle");

    // Victory Modal
    this.victoryModal = document.getElementById("victory-modal");
    this.vicTitle = document.getElementById("vic-title");
    this.vicTime = document.getElementById("vic-time");

    // Build 81 Cell DOM elements
    this.boardEl.innerHTML = "";
    this.cellElements = [];
    for (let r = 0; r < 9; r++) {
      this.cellElements.push([]);
      for (let c = 0; c < 9; c++) {
        const cell = document.createElement("div");
        cell.className = "cell-tile";
        cell.dataset.r = r;
        cell.dataset.c = c;
        cell.addEventListener("click", () => this.selectCell(r, c));
        this.boardEl.appendChild(cell);
        this.cellElements[r].push(cell);
      }
    }

    // Build Level Cards on Levels Screen
    this.renderLevelsGrid();

    // Start precision clock (runs at 10 Hz)
    this.clockInterval = setInterval(() => this.updateClocks(), 100);
  }

  renderLevelsGrid() {
    const container = document.getElementById("levels-container");
    container.innerHTML = "";

    SudokuGenerator.DIFFICULTY_TIERS.forEach((tier, i) => {
      const card = document.createElement("div");
      card.className = `level-card-3d ${i === this.currentTier ? "active" : ""}`;
      card.addEventListener("click", () => {
        this.loadNewPuzzle(i);
        this.switchScreen("game");
      });

      // Stars SVG
      let starsHTML = "";
      for (let s = 0; s < 5; s++) {
        const fillCol = s < tier.stars ? "var(--star-gold)" : "var(--star-empty)";
        starsHTML += `
          <svg class="star-svg" viewBox="0 0 24 24">
            <polygon points="12,2 15,8 22,9 17,14 18,21 12,17 6,21 7,14 2,9 9,8" fill="${fillCol}"/>
          </svg>
        `;
      }

      card.innerHTML = `
        <div class="level-card-title">LEVEL ${i + 1}: ${tier.name.toUpperCase()}</div>
        <div class="level-clue-pill">${tier.clues} CLUES</div>
        <div class="level-stars-row">${starsHTML}</div>
        <div class="level-desc">${tier.desc}</div>
      `;
      container.appendChild(card);
    });
  }

  switchScreen(screenName) {
    this.currentScreen = screenName;
    document.querySelectorAll(".screen").forEach(s => s.classList.remove("active"));
    if (screenName === "home") {
      this.screenHome.classList.add("active");
    } else if (screenName === "levels") {
      this.screenLevels.classList.add("active");
      this.renderLevelsGrid();
    } else if (screenName === "game") {
      this.screenGame.classList.add("active");
    }
  }

  toggleTheme() {
    const current = document.documentElement.getAttribute("data-theme") || "dark";
    const next = current === "dark" ? "light" : "dark";
    document.documentElement.setAttribute("data-theme", next);
    this.showToast(`THEME: ${next.toUpperCase()}`, "info");
  }

  toggleFullscreen() {
    if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen().catch(() => {});
      this.showToast("FULLSCREEN ENABLED", "info");
    } else {
      if (document.exitFullscreen) document.exitFullscreen().catch(() => {});
      this.showToast("WINDOWED MODE", "info");
    }
  }

  showToast(msg, type = "info") {
    const t = document.getElementById("toast");
    t.textContent = msg;
    t.className = `toast ${type}`;
    clearTimeout(this._toastTimeout);
    this._toastTimeout = setTimeout(() => {
      t.className = "toast hidden";
    }, 2200);
  }

  loadNewPuzzle(tierId) {
    this.currentTier = tierId;
    const { puzzle, solution } = SudokuGenerator.createPuzzle(this.currentTier);
    this.puzzle = puzzle;
    this.solution = solution;
    this.board = puzzle.map(row => [...row]);

    this.cellTypes = {};
    for (let r = 0; r < 9; r++) {
      for (let c = 0; c < 9; c++) {
        if (puzzle[r][c] !== 0) {
          this.cellTypes[`${r},${c}`] = "initial";
        } else {
          this.cellTypes[`${r},${c}`] = "empty";
        }
      }
    }

    this.humanTime = 0.0;
    this.aiTime = 0.0;
    this.isHumanActive = true;
    this.aiRunning = false;
    this.aiGenerator = null;
    this.aiStats = { explored: 0, backtracks: 0 };
    this.gameWon = false;
    this.selectedCell = { r: 0, c: 0 };

    this.stopAILoop();
    this.updateSolveButton();

    const tier = SudokuGenerator.DIFFICULTY_TIERS[this.currentTier];
    const text = `LEVEL ${this.currentTier + 1}: ${tier.name.toUpperCase()} (${tier.clues} CLUES)`;
    this.currentTierBadge.textContent = text;
    this.homeFooterTier.textContent = `CURRENT TIER: ${tier.name.toUpperCase()} (${tier.clues} CLUES) • PRESS F11 FOR FULLSCREEN`;

    this.setAIStatus("IDLE", "Ready. Watch AI solve step-by-step or solve it yourself!");
    this.updateConflicts();
    this.renderBoard();
  }

  resetBoard() {
    this.stopAILoop();
    for (let r = 0; r < 9; r++) {
      for (let c = 0; c < 9; c++) {
        if (this.cellTypes[`${r},${c}`] !== "initial") {
          this.board[r][c] = 0;
          this.cellTypes[`${r},${c}`] = "empty";
        }
      }
    }
    this.aiRunning = false;
    this.aiGenerator = null;
    this.aiStats = { explored: 0, backtracks: 0 };
    this.gameWon = false;
    this.updateSolveButton();
    this.setAIStatus("IDLE", "Board reset to initial clues.");
    this.updateConflicts();
    this.renderBoard();
    this.showToast("Board reset to initial clues.", "warn");
  }

  selectCell(r, c) {
    this.selectedCell = { r, c };
    this.renderBoard();
  }

  setCellValue(r, c, val, tag = "user") {
    if (this.cellTypes[`${r},${c}`] === "initial") return false;

    if (val === 0) {
      this.board[r][c] = 0;
      this.cellTypes[`${r},${c}`] = "empty";
    } else {
      this.board[r][c] = val;
      this.cellTypes[`${r},${c}`] = tag;
    }

    this.updateConflicts();
    this.renderBoard();

    if (this.isBoardSolved()) {
      this.handleVictory("HUMAN");
    }
    return true;
  }

  updateConflicts() {
    this.conflicts = SudokuSolver.findAllConflicts(this.board);
  }

  isBoardSolved() {
    if (this.conflicts.size > 0) return false;
    for (let r = 0; r < 9; r++) {
      for (let c = 0; c < 9; c++) {
        if (this.board[r][c] === 0) return false;
      }
    }
    return true;
  }

  triggerHint() {
    if (this.gameWon) return;

    let target = null;
    if (this.selectedCell) {
      const { r, c } = this.selectedCell;
      if (this.board[r][c] === 0) target = { r, c };
    }

    if (!target) {
      const empty = [];
      for (let r = 0; r < 9; r++) {
        for (let c = 0; c < 9; c++) {
          if (this.board[r][c] === 0) {
            const cands = SudokuSolver.getCandidates(this.board, r, c);
            empty.push({ r, c, len: cands.size });
          }
        }
      }
      if (empty.length === 0) {
        this.showToast("Board is already full!", "warn");
        return;
      }
      empty.sort((a, b) => a.len - b.len);
      target = { r: empty[0].r, c: empty[0].c };
    }

    const correctVal = this.solution[target.r][target.c];
    this.setCellValue(target.r, target.c, correctVal, "hint");
    this.selectCell(target.r, target.c);
    this.showToast(`Hint: Placed ${correctVal} at Row ${target.r + 1}, Col ${target.c + 1}`, "success");
  }

  // -------------------------------------------------------------------------
  // AI STEP-BY-STEP SOLVER ENGINE (NON-BLOCKING WEB RUNTIME)
  // -------------------------------------------------------------------------
  toggleAISolver() {
    if (this.gameWon) return;

    if (this.aiRunning) {
      this.stopAILoop();
      this.setAIStatus("IDLE", "AI Solver Paused.");
      this.showToast("AI Solver paused.", "warn");
      return;
    }

    this.isHumanActive = false;

    if (!this.aiGenerator) {
      // Revert user digits
      for (let r = 0; r < 9; r++) {
        for (let c = 0; c < 9; c++) {
          if (!["initial", "hint"].includes(this.cellTypes[`${r},${c}`])) {
            this.board[r][c] = 0;
            this.cellTypes[`${r},${c}`] = "empty";
          }
        }
      }
      this.updateConflicts();

      const emptyCells = [];
      for (let r = 0; r < 9; r++) {
        for (let c = 0; c < 9; c++) {
          if (this.board[r][c] === 0) emptyCells.push({ r, c });
        }
      }
      this.aiStats = { explored: 0, backtracks: 0 };
      this.aiGenerator = SudokuSolver.visualDFSGenerator(this.board, emptyCells, this.aiStats);
      this.showToast("AI Solver started!", "info");
    }

    this.startAILoop();
  }

  executeSingleAIStep() {
    if (!this.aiGenerator) {
      this.isHumanActive = false;
      for (let r = 0; r < 9; r++) {
        for (let c = 0; c < 9; c++) {
          if (!["initial", "hint"].includes(this.cellTypes[`${r},${c}`])) {
            this.board[r][c] = 0;
            this.cellTypes[`${r},${c}`] = "empty";
          }
        }
      }
      this.updateConflicts();
      const emptyCells = [];
      for (let r = 0; r < 9; r++) {
        for (let c = 0; c < 9; c++) {
          if (this.board[r][c] === 0) emptyCells.push({ r, c });
        }
      }
      this.aiStats = { explored: 0, backtracks: 0 };
      this.aiGenerator = SudokuSolver.visualDFSGenerator(this.board, emptyCells, this.aiStats);
    }

    const { value, done } = this.aiGenerator.next();
    if (done || !value) {
      this.stopAILoop();
      return;
    }

    const { state, r, c, val, msg } = value;
    this.setAIStatus(state, msg);

    if (state === "TRY") {
      this.board[r][c] = val;
      this.cellTypes[`${r},${c}`] = "ai";
      this.activeAICell = { r, c, state: "ai-try" };
    } else if (state === "WRONG") {
      // DRAMATIC RED HIGHLIGHT: The mistake is shown clearly!
      this.board[r][c] = val;
      this.activeAICell = { r, c, state: "ai-wrong" };
    } else if (state === "BACKTRACK") {
      this.board[r][c] = 0;
      this.cellTypes[`${r},${c}`] = "empty";
      this.activeAICell = { r, c, state: "ai-backtrack" };
    } else if (state === "SOLVED") {
      this.stopAILoop();
      this.activeAICell = null;
      this.handleVictory("AI");
    } else if (state === "UNSOLVABLE") {
      this.stopAILoop();
      this.showToast("Puzzle has no solution!", "error");
    }

    this.renderBoard();
  }

  startAILoop() {
    if (this.aiTimerHandle) {
      clearInterval(this.aiTimerHandle);
      cancelAnimationFrame(this.aiTimerHandle);
      this.aiTimerHandle = null;
    }
    this.aiRunning = true;
    this.updateSolveButton();

    const interval = this.aiSpeeds[this.aiSpeedId].interval;

    if (interval === 0) {
      // Instant Mode: execute batches within animation frames
      const runBatch = () => {
        if (!this.aiRunning) return;
        const t0 = performance.now();
        while (this.aiRunning && performance.now() - t0 < 25) {
          this.executeSingleAIStep();
        }
        if (this.aiRunning) {
          this.aiTimerHandle = requestAnimationFrame(runBatch);
        }
      };
      this.aiTimerHandle = requestAnimationFrame(runBatch);
    } else {
      // Educational Step Mode: execute the first step immediately for responsiveness
      this.executeSingleAIStep();
      if (!this.aiRunning) return;

      this.aiTimerHandle = setInterval(() => {
        if (!this.aiRunning) {
          this.stopAILoop();
          return;
        }
        this.executeSingleAIStep();
      }, interval);
    }
  }

  stopAILoop() {
    this.aiRunning = false;
    if (this.aiTimerHandle) {
      clearInterval(this.aiTimerHandle);
      cancelAnimationFrame(this.aiTimerHandle);
      this.aiTimerHandle = null;
    }
    this.updateSolveButton();
  }

  updateSolveButton() {
    if (this.aiRunning) {
      this.btnAiSolve.classList.replace("btn-accent", "btn-warning");
      this.solveText.textContent = "PAUSE AI";
      this.solveIcon.innerHTML = `<rect x="6" y="5" width="4" height="14" fill="currentColor"/><rect x="14" y="5" width="4" height="14" fill="currentColor"/>`;
    } else {
      this.btnAiSolve.classList.replace("btn-warning", "btn-accent");
      this.solveText.textContent = "AI SOLVE";
      this.solveIcon.innerHTML = `<polygon points="6,4 20,12 6,20" fill="currentColor"/>`;
    }
  }

  setAIStatus(state, msg) {
    this.aiLed.className = `led-jewel state-${state.toLowerCase()}`;
    this.aiStatusMsg.textContent = msg;

    this.statExplored.textContent = this.aiStats.explored.toLocaleString();
    this.statBacktracks.textContent = this.aiStats.backtracks.toLocaleString();

    let ratio = 0.0;
    if (this.aiStats.explored > 0) {
      ratio = (this.aiStats.backtracks / this.aiStats.explored) * 100;
    }
    this.statRatio.textContent = `${ratio.toFixed(1)}%`;
  }

  handleVictory(winner) {
    this.gameWon = true;
    this.stopAILoop();
    if (winner === "HUMAN") {
      this.vicTitle.textContent = "HUMAN VICTORY!";
      this.vicTime.textContent = `Play Time: ${this.formatTime(this.humanTime)}`;
      this.showToast(`VICTORY! Solved in ${this.humanTime.toFixed(1)}s!`, "success");
    } else {
      this.vicTitle.textContent = "AI SOLVED THE BOARD!";
      this.vicTime.textContent = `AI Time: ${this.aiTime.toFixed(2)}s | Explored: ${this.aiStats.explored} | Backtracks: ${this.aiStats.backtracks}`;
      this.showToast(`AI Defeated Board in ${this.aiTime.toFixed(2)}s!`, "success");
    }
    this.victoryModal.classList.remove("hidden");
  }

  formatTime(totalSec) {
    const m = Math.floor(totalSec / 60);
    const s = totalSec % 60;
    return `${String(m).padStart(2, "0")}:${s.toFixed(1).padStart(4, "0")}`;
  }

  updateClocks() {
    if (this.currentScreen !== "game" || this.gameWon) return;

    if (this.isHumanActive) {
      this.humanTime += 0.1;
      this.timerHumanEl.textContent = this.formatTime(this.humanTime);
      this.timerHumanEl.classList.add("active");
    } else {
      this.timerHumanEl.classList.remove("active");
    }

    if (this.aiRunning) {
      this.aiTime += 0.1;
      this.timerAiEl.textContent = `${this.aiTime.toFixed(2)} s`;
      this.timerAiEl.classList.add("active");
    } else {
      this.timerAiEl.classList.remove("active");
    }
  }

  renderBoard() {
    const selR = this.selectedCell ? this.selectedCell.r : -1;
    const selC = this.selectedCell ? this.selectedCell.c : -1;
    const activeVal = selR >= 0 ? this.board[selR][selC] : 0;

    for (let r = 0; r < 9; r++) {
      for (let c = 0; c < 9; c++) {
        const cell = this.cellElements[r][c];
        const val = this.board[r][c];
        const tag = this.cellTypes[`${r},${c}`] || "empty";

        // Reset classes
        cell.className = "cell-tile";
        cell.textContent = val !== 0 ? val : "";

        // Tag class
        if (tag === "initial") cell.classList.add("initial");
        else if (tag === "user") cell.classList.add("user");
        else if (tag === "hint") cell.classList.add("hint");
        else if (tag === "ai") cell.classList.add("ai");

        // Crosshair highlighting
        if (selR >= 0) {
          const inSameRow = (r === selR);
          const inSameCol = (c === selC);
          const inSameBox = (Math.floor(r / 3) === Math.floor(selR / 3) && Math.floor(c / 3) === Math.floor(selC / 3));
          if (inSameRow || inSameCol || inSameBox) {
            cell.classList.add("crosshair");
          }
        }

        // Same digit highlight
        if (activeVal !== 0 && val === activeVal) {
          cell.classList.add("same-digit");
        }

        // Selected cell
        if (r === selR && c === selC) {
          cell.classList.add("selected");
        }

        // AI highlights
        if (this.activeAICell && this.activeAICell.r === r && this.activeAICell.c === c) {
          cell.classList.add(this.activeAICell.state);
        }

        // Conflict
        if (this.conflicts.has(`${r},${c}`)) {
          cell.classList.add("conflict");
        }
      }
    }
  }

  // -------------------------------------------------------------------------
  // EVENT BINDINGS
  // -------------------------------------------------------------------------
  bindEvents() {
    // Navigation
    document.getElementById("btn-home-play").onclick = () => this.switchScreen("game");
    document.getElementById("btn-home-levels").onclick = () => this.switchScreen("levels");
    document.getElementById("btn-home-demo").onclick = () => {
      this.loadNewPuzzle(this.currentTier);
      this.switchScreen("game");
      this.aiSpeedId = "ultra_slow";
      this.toggleAISolver();
    };
    document.getElementById("btn-home-theme").onclick = () => this.toggleTheme();
    document.getElementById("btn-home-fs").onclick = () => this.toggleFullscreen();

    document.getElementById("btn-levels-back").onclick = () => this.switchScreen("home");
    document.getElementById("btn-levels-theme").onclick = () => this.toggleTheme();
    document.getElementById("btn-levels-fs").onclick = () => this.toggleFullscreen();

    document.getElementById("btn-game-home").onclick = () => this.switchScreen("home");
    document.getElementById("btn-game-levels").onclick = () => this.switchScreen("levels");
    document.getElementById("btn-game-theme").onclick = () => this.toggleTheme();
    document.getElementById("btn-game-fs").onclick = () => this.toggleFullscreen();

    // Game Actions
    this.btnAiSolve.onclick = () => this.toggleAISolver();
    this.btnAiStep.onclick = () => {
      if (this.aiRunning) this.stopAILoop();
      this.executeSingleAIStep();
    };
    this.btnHint.onclick = () => this.triggerHint();
    this.btnReset.onclick = () => this.resetBoard();
    this.btnNewPuzzle.onclick = () => {
      this.loadNewPuzzle(this.currentTier);
      this.showToast("Fresh puzzle loaded!", "info");
    };

    // Speed Buttons
    document.querySelectorAll(".btn-speed").forEach(btn => {
      btn.onclick = () => {
        document.querySelectorAll(".btn-speed").forEach(b => b.classList.remove("active"));
        btn.classList.add("active");
        this.aiSpeedId = btn.dataset.speed;
        if (this.aiRunning) this.startAILoop();
        this.showToast(`Speed: ${this.aiSpeeds[this.aiSpeedId].name}`, "info");
      };
    });

    // Numpad clicks
    document.querySelectorAll(".btn-num").forEach(btn => {
      btn.onclick = () => {
        if (!this.selectedCell) return;
        const num = btn.dataset.num;
        if (num) {
          this.setCellValue(this.selectedCell.r, this.selectedCell.c, parseInt(num, 10), "user");
        }
      };
    });
    document.getElementById("btn-erase").onclick = () => {
      if (this.selectedCell) {
        this.setCellValue(this.selectedCell.r, this.selectedCell.c, 0);
      }
    };

    // Victory modal
    document.getElementById("btn-vic-new").onclick = () => {
      this.victoryModal.classList.add("hidden");
      this.loadNewPuzzle(this.currentTier);
    };
    document.getElementById("btn-vic-levels").onclick = () => {
      this.victoryModal.classList.add("hidden");
      this.switchScreen("levels");
    };

    // Keyboard support
    window.addEventListener("keydown", e => {
      if (e.key === "F11") {
        e.preventDefault();
        this.toggleFullscreen();
      } else if (e.key.toLowerCase() === "t" && !["input", "textarea"].includes(document.activeElement.tagName.toLowerCase())) {
        this.toggleTheme();
      }

      if (this.currentScreen !== "game") return;

      if (e.key === "ArrowUp") {
        e.preventDefault();
        this.selectCell((this.selectedCell.r + 8) % 9, this.selectedCell.c);
      } else if (e.key === "ArrowDown") {
        e.preventDefault();
        this.selectCell((this.selectedCell.r + 1) % 9, this.selectedCell.c);
      } else if (e.key === "ArrowLeft") {
        e.preventDefault();
        this.selectCell(this.selectedCell.r, (this.selectedCell.c + 8) % 9);
      } else if (e.key === "ArrowRight") {
        e.preventDefault();
        this.selectCell(this.selectedCell.r, (this.selectedCell.c + 1) % 9);
      } else if (e.key >= "1" && e.key <= "9") {
        if (this.selectedCell) {
          this.setCellValue(this.selectedCell.r, this.selectedCell.c, parseInt(e.key, 10), "user");
        }
      } else if (["Backspace", "Delete", "0"].includes(e.key)) {
        if (this.selectedCell) {
          this.setCellValue(this.selectedCell.r, this.selectedCell.c, 0);
        }
      } else if (e.key.toLowerCase() === "h") {
        this.triggerHint();
      } else if (e.key === " " || e.key.toLowerCase() === "s") {
        e.preventDefault();
        this.toggleAISolver();
      } else if (e.key.toLowerCase() === "n") {
        this.loadNewPuzzle(this.currentTier);
        this.showToast("Fresh puzzle loaded!", "info");
      } else if (e.key.toLowerCase() === "r") {
        this.resetBoard();
      }
    });
  }
}

// Initialize on DOM ready
if (typeof document !== "undefined") {
  document.addEventListener("DOMContentLoaded", () => {
    window.app = new SudokuArenaApp();
  });
}

// Export for Node.js automated tests
if (typeof module !== "undefined" && module.exports) {
  module.exports = { SudokuSolver, SudokuGenerator, SudokuArenaApp };
}
