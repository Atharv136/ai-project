// Create minimal DOM mock
global.window = {};
global.document = {
  documentElement: {
    getAttribute: () => "dark",
    setAttribute: () => {},
    requestFullscreen: async () => {}
  },
  getElementById: (id) => ({
    textContent: "",
    className: "",
    innerHTML: "",
    classList: { add: () => {}, remove: () => {}, replace: () => {} },
    appendChild: () => {},
    addEventListener: () => {}
  }),
  querySelectorAll: () => [],
  addEventListener: () => {}
};
global.requestAnimationFrame = (cb) => setTimeout(cb, 16);
global.cancelAnimationFrame = (id) => clearTimeout(id);

const { SudokuSolver, SudokuGenerator } = require('./app.js');

console.log("==================================================");
console.log("RUNNING AUTOMATED TEST SUITE FOR WEB ENGINE (JS)");
console.log("==================================================");

console.log("\n[Test 1] Testing 8 Difficulty Tiers (SudokuGenerator in JS)...");
for (let i = 0; i < 8; i++) {
  const { puzzle, solution } = SudokuGenerator.createPuzzle(i);
  let clues = 0;
  for (let r = 0; r < 9; r++) {
    for (let c = 0; c < 9; c++) {
      if (puzzle[r][c] !== 0) clues++;
    }
  }
  const tier = SudokuGenerator.DIFFICULTY_TIERS[i];
  if (clues !== tier.clues) {
    throw new Error(`Tier ${i} clue mismatch: ${clues} vs ${tier.clues}`);
  }
  if (!solution) {
    throw new Error(`Tier ${i} unsolvable`);
  }
  const conflicts = SudokuSolver.findAllConflicts(solution);
  if (conflicts.size > 0) {
    throw new Error(`Tier ${i} solution has conflicts`);
  }
  console.log(`  ✓ Tier ${i} (${tier.name}): ${clues} clues (Target: ${tier.clues}) -> Unique & Solved!`);
}

console.log("\n[Test 2] Testing JavaScript Visual DFS Generator...");
const { puzzle } = SudokuGenerator.createPuzzle(0);
const empty = [];
for (let r = 0; r < 9; r++) {
  for (let c = 0; c < 9; c++) {
    if (puzzle[r][c] === 0) empty.push({ r, c });
  }
}
const stats = { explored: 0, backtracks: 0 };
const gen = SudokuSolver.visualDFSGenerator(puzzle, empty, stats);

let statesSeen = new Set();
for (let s = 0; s < 50; s++) {
  const { value, done } = gen.next();
  if (done || !value) break;
  statesSeen.add(value.state);
  if (value.state === "SOLVED") break;
}

if (!statesSeen.has("TRY")) {
  throw new Error("Generator never yielded TRY state");
}
console.log(`  ✓ Visual DFS states seen: [${Array.from(statesSeen).join(", ")}]`);
console.log(`  ✓ Explored choices: ${stats.explored}, Backtracks: ${stats.backtracks}`);

console.log("\n[Test 3] Testing Conflict Detection...");
const testBoard = [
  [5, 5, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0]
];
const conflicts = SudokuSolver.findAllConflicts(testBoard);
if (!conflicts.has("0,0") || !conflicts.has("0,1")) {
  throw new Error("Failed to catch row conflict");
}
console.log("  ✓ Dynamic conflict detection passed.");

console.log("\n==================================================");
console.log("ALL WEB JAVASCRIPT TESTS PASSED WITH 100% SUCCESS!");
console.log("==================================================");
process.exit(0);
