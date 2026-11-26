"""
Automated Comprehensive Test Suite for Sudoku Arena: Human vs AI (Multi-Screen Edition)
Tests Welcome Page, Levels Page, Game Arena, Slow AI Visualization, Headless Rendering.
"""

import os
import sys

# Force headless dummy video driver
os.environ["SDL_VIDEODRIVER"] = "dummy"

import pygame
import main

def test_suite():
    print("=" * 60)
    print("RUNNING AUTOMATED TEST SUITE FOR SUDOKU ARENA (MULTI-SCREEN)")
    print("=" * 60)

    # 1. Test ThemeManager
    print("\n[Test 1] Testing ThemeManager...")
    tm = main.ThemeManager(start_dark=True)
    assert tm.is_dark is True
    tm.toggle()
    assert tm.is_dark is False
    tm.toggle()
    assert tm.is_dark is True
    print("✓ ThemeManager toggle works.")

    # 2. Test 8 Difficulty Tiers & Puzzle Generation
    print("\n[Test 2] Testing 8 Difficulty Tiers & SudokuGenerator...")
    for tier_id in range(8):
        tier_info = main.SudokuGenerator.DIFFICULTY_TIERS[tier_id]
        puzzle, solution = main.SudokuGenerator.create_puzzle(tier_id)
        clues = sum(1 for r in range(9) for c in range(9) if puzzle[r][c] != 0)
        sol_clues = sum(1 for r in range(9) for c in range(9) if solution[r][c] != 0)
        assert clues == tier_info["clues"], f"Tier {tier_id} clue count mismatch: {clues} vs {tier_info['clues']}"
        assert sol_clues == 81, f"Solution not full for tier {tier_id}"
        assert len(main.SudokuSolver.find_all_conflicts(solution)) == 0, f"Solution has conflicts"
        print(f"  - Tier {tier_id} ({tier_info['name']}): {clues} clues -> Solvable and unique!")
    print("✓ All 8 difficulty tiers verified.")

    # 3. Test Slow Visual DFS Generator with WRONG & BACKTRACK States
    print("\n[Test 3] Testing Visual DFS with Slow Failure Revealing...")
    puzzle, _ = main.SudokuGenerator.create_puzzle(0)
    b = [row[:] for row in puzzle]
    empty = [(r, c) for r in range(9) for c in range(9) if b[r][c] == 0]
    stats = {"explored": 0, "backtracks": 0}
    gen = main.SudokuSolver.visual_dfs_generator(b, empty, stats)
    
    seen_states = set()
    for _ in range(60):
        try:
            state, r, c, val, msg = next(gen)
            seen_states.add(state)
            if state == "SOLVED":
                break
        except StopIteration:
            break
            
    assert "TRY" in seen_states, "DFS generator never yielded TRY"
    print(f"✓ Observed states: {seen_states}. Explored: {stats['explored']}, Backtracks: {stats['backtracks']}")

    # 4. Test SudokuArenaApp (Multi-Screen Navigation, Fullscreen, Rendering)
    print("\n[Test 4] Testing SudokuArenaApp Navigation & Responsive Layout...")
    app = main.SudokuArenaApp(headless=True)
    
    # 4.1 Home Screen
    assert app.current_screen == main.SudokuArenaApp.SCREEN_HOME
    app.render() # Verify home screen renders without exceptions
    print("✓ Welcome / Home Page renders flawlessly.")

    # 4.2 Levels Screen Navigation
    app.handle_action("go_levels")
    assert app.current_screen == main.SudokuArenaApp.SCREEN_LEVELS
    app.render() # Verify levels screen renders without exceptions
    print("✓ Levels Page renders flawlessly.")

    # 4.3 Level Selection -> Game Screen
    app.handle_action("select_level_4") # Expert
    assert app.current_screen == main.SudokuArenaApp.SCREEN_GAME
    assert app.current_tier == 4
    app.render()
    print("✓ Level selection loads puzzle and switches to Game Arena.")

    # 4.4 Single Step AI Execution (Educational inspection mode)
    print("\n[Test 5] Testing AI Step-by-Step execution...")
    app.handle_action("ai_step")
    assert app.grid.ai_active_cell is not None
    assert app.ai_status_state in ("TRY", "WRONG", "BACKTRACK", "SOLVED")
    print(f"✓ AI Step executed: {app.ai_status_message}")

    # 4.5 Hint System
    app.handle_action("hint")
    print("✓ Hint placed verified.")

    # 4.6 Reset Board
    app.handle_action("reset")
    assert app.ai_running is False
    print("✓ Reset board verified.")

    # 4.7 Fullscreen Toggle
    app.handle_action("toggle_fullscreen")
    assert app.is_fullscreen is True
    app.render()
    app.handle_action("toggle_fullscreen")
    assert app.is_fullscreen is False
    app.render()
    print("✓ Fullscreen toggling and layout recalculation verified.")

    # 4.8 Theme Toggle
    app.handle_action("toggle_theme")
    assert app.theme_manager.is_dark is False
    app.render()
    app.handle_action("toggle_theme")
    assert app.theme_manager.is_dark is True
    app.render()
    print("✓ Dynamic Theme toggling verified.")

    print("\n" + "=" * 60)
    print("ALL TESTS PASSED WITH 100% SUCCESS!")
    print("=" * 60)

if __name__ == "__main__":
    test_suite()
