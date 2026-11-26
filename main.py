"""
Sudoku Arena: Human vs AI (Professional 3D Edition)
===================================================
A modern, luxury-grade, high-performance Pygame application featuring:
- Full 3D tactile UI with physical drop shadows, beveled edges, mechanical click response
- 100% Procedurally Drawn Crisp Vector Icons (Zero broken Unicode / missing glyph boxes)
- Multi-Screen Architecture: Welcome / Home Page, Levels Page, Game Arena
- Fullscreen & Dynamic Responsive Scaling (F11 or on-screen toggle)
- Educational Slow-Motion AI Visualizer showing candidate testing, mistake detection
  (cell flashing in vivid 3D crimson red), and backtracking
- Instant Hint System powered by Minimum Remaining Values (MRV) heuristic
- 8 Distinct Difficulty Tiers (Beginner to Impossible, 60 down to 17 minimal clues)
- Human vs AI Race Mode with 3D recessed timer gauges
- Dynamic Conflict Detection & Soft 3D Crosshair Highlighting
- Dynamic 3D Dark & Light Themes
"""

import os
import sys
import copy
import time
import math
import random
import pygame

# Initialize Pygame core modules
pygame.init()
pygame.font.init()

# ---------------------------------------------------------------------------
# COLOR UTILITIES & THEME MANAGER
# ---------------------------------------------------------------------------
def adjust_brightness(color, factor):
    """Safely adjusts RGB brightness by a factor."""
    return tuple(max(0, min(255, int(c * factor))) for c in color[:3])

class ThemeManager:
    """
    Manages luxury 3D palettes for Dark Mode (Obsidian / Titanium Slate)
    and Light Mode (Frosted Ceramic / Polished Paper).
    """
    DARK = {
        "name": "dark",
        "bg": (14, 17, 26),
        "panel_bg": (22, 27, 40),
        "panel_border": (38, 47, 70),
        "panel_shadow": (7, 9, 14),
        "card_bg": (25, 31, 46),
        "card_border": (44, 54, 80),
        "card_shadow": (8, 10, 16),
        "gauge_bg": (16, 20, 30),
        "gauge_border": (32, 40, 60),
        "grid_tray_bg": (12, 15, 23),
        "grid_tray_border": (34, 43, 64),
        "grid_bg": (18, 22, 33),
        "grid_line_thin": (36, 45, 68),
        "grid_line_thick": (78, 98, 145),
        "grid_groove": (8, 10, 16),
        "cell_base": (22, 28, 42),
        "cell_crosshair": (28, 36, 56),
        "cell_same_digit": (36, 48, 76),
        "cell_selected": (38, 62, 106),
        "cell_selected_border": (96, 165, 250),
        "cell_initial": (245, 248, 255),
        "cell_user": (147, 197, 253),
        "cell_hint": (251, 191, 36),
        "cell_conflict_bg": (136, 24, 24),
        "cell_conflict_fg": (254, 202, 202),
        "ai_searching_bg": (180, 120, 15),
        "ai_searching_fg": (254, 240, 138),
        "ai_wrong_bg": (195, 28, 28),
        "ai_wrong_fg": (255, 235, 235),
        "ai_backtrack_bg": (120, 22, 22),
        "ai_backtrack_fg": (252, 165, 165),
        "ai_solved_bg": (6, 95, 70),
        "ai_solved_fg": (167, 243, 208),
        "text_primary": (243, 246, 251),
        "text_secondary": (150, 165, 188),
        "text_muted": (100, 116, 140),
        "accent_blue": (59, 130, 246),
        "accent_purple": (139, 92, 246),
        "accent_emerald": (16, 185, 129),
        "accent_amber": (245, 158, 11),
        "accent_rose": (244, 63, 94),
        "btn_primary_bg": (45, 115, 235),
        "btn_secondary_bg": (32, 40, 60),
        "btn_accent_bg": (124, 78, 230),
        "btn_danger_bg": (210, 35, 35),
        "btn_warning_bg": (217, 119, 6),
        "star_gold": (250, 204, 21),
        "star_empty": (55, 66, 92),
    }

    LIGHT = {
        "name": "light",
        "bg": (242, 245, 250),
        "panel_bg": (255, 255, 255),
        "panel_border": (218, 226, 238),
        "panel_shadow": (200, 208, 222),
        "card_bg": (255, 255, 255),
        "card_border": (222, 230, 242),
        "card_shadow": (205, 213, 228),
        "gauge_bg": (240, 244, 250),
        "gauge_border": (215, 224, 236),
        "grid_tray_bg": (230, 235, 245),
        "grid_tray_border": (205, 215, 230),
        "grid_bg": (255, 255, 255),
        "grid_line_thin": (226, 232, 240),
        "grid_line_thick": (71, 85, 105),
        "grid_groove": (200, 208, 222),
        "cell_base": (255, 255, 255),
        "cell_crosshair": (240, 245, 255),
        "cell_same_digit": (230, 240, 255),
        "cell_selected": (219, 234, 254),
        "cell_selected_border": (37, 99, 235),
        "cell_initial": (15, 23, 42),
        "cell_user": (29, 78, 216),
        "cell_hint": (180, 83, 9),
        "cell_conflict_bg": (254, 226, 226),
        "cell_conflict_fg": (185, 28, 28),
        "ai_searching_bg": (254, 240, 138),
        "ai_searching_fg": (133, 77, 14),
        "ai_wrong_bg": (254, 202, 202),
        "ai_wrong_fg": (185, 28, 28),
        "ai_backtrack_bg": (254, 226, 226),
        "ai_backtrack_fg": (185, 28, 28),
        "ai_solved_bg": (187, 247, 208),
        "ai_solved_fg": (6, 95, 70),
        "text_primary": (15, 23, 42),
        "text_secondary": (71, 85, 105),
        "text_muted": (140, 155, 175),
        "accent_blue": (37, 99, 235),
        "accent_purple": (124, 58, 237),
        "accent_emerald": (5, 150, 105),
        "accent_amber": (217, 119, 6),
        "accent_rose": (225, 29, 72),
        "btn_primary_bg": (37, 99, 235),
        "btn_secondary_bg": (238, 242, 248),
        "btn_accent_bg": (124, 58, 237),
        "btn_danger_bg": (220, 38, 38),
        "btn_warning_bg": (217, 119, 6),
        "star_gold": (234, 179, 8),
        "star_empty": (203, 213, 225),
    }

    def __init__(self, start_dark=True):
        self.is_dark = start_dark
        self.palette = self.DARK if start_dark else self.LIGHT

    def toggle(self):
        self.is_dark = not self.is_dark
        self.palette = self.DARK if self.is_dark else self.LIGHT
        return self.palette


# ---------------------------------------------------------------------------
# VECTOR GRAPHICS & 3D DRAWING HELPERS (ZERO BROKEN GLYPHS)
# ---------------------------------------------------------------------------
class Draw3D:
    """
    Renders high-fidelity, procedurally calculated vector icons and 3D panels.
    Guarantees crisp graphics with zero missing font glyphs or Unicode boxes.
    """
    @staticmethod
    def draw_star(surface, cx, cy, r_out, r_in, fill_col, border_col=None):
        pts = []
        for i in range(10):
            angle = -math.pi / 2 + i * (math.pi / 5)
            r = r_out if i % 2 == 0 else r_in
            pts.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
        pygame.draw.polygon(surface, fill_col, pts)
        if border_col:
            pygame.draw.polygon(surface, border_col, pts, 1)

    @classmethod
    def draw_stars(cls, surface, start_x, cy, filled_count, total=5, r_out=7, r_in=3.5, gap=18, gold_col=(250, 204, 21), empty_col=(60, 70, 95)):
        for i in range(total):
            x = start_x + i * gap
            is_filled = (i < filled_count)
            col = gold_col if is_filled else empty_col
            b_col = adjust_brightness(col, 0.75)
            cls.draw_star(surface, x, cy, r_out, r_in, col, b_col)

    @staticmethod
    def draw_play_icon(surface, cx, cy, size, color):
        pts = [
            (cx - size * 0.35, cy - size * 0.5),
            (cx + size * 0.5, cy),
            (cx - size * 0.35, cy + size * 0.5)
        ]
        pygame.draw.polygon(surface, color, pts)

    @staticmethod
    def draw_pause_icon(surface, cx, cy, size, color):
        bw = max(2, int(size * 0.26))
        bh = int(size * 0.8)
        pygame.draw.rect(surface, color, (cx - size * 0.35, cy - bh // 2, bw, bh), border_radius=1)
        pygame.draw.rect(surface, color, (cx + size * 0.09, cy - bh // 2, bw, bh), border_radius=1)

    @staticmethod
    def draw_step_icon(surface, cx, cy, size, color):
        pts = [
            (cx - size * 0.45, cy - size * 0.45),
            (cx + size * 0.15, cy),
            (cx - size * 0.45, cy + size * 0.45)
        ]
        pygame.draw.polygon(surface, color, pts)
        bw = max(2, int(size * 0.22))
        pygame.draw.rect(surface, color, (cx + size * 0.28, cy - size * 0.45, bw, int(size * 0.9)), border_radius=1)

    @staticmethod
    def draw_fullscreen_icon(surface, cx, cy, size, color):
        s = size * 0.55
        arm = size * 0.28
        th = 2
        # Top-left
        pygame.draw.line(surface, color, (cx - s, cy - s), (cx - s + arm, cy - s), th)
        pygame.draw.line(surface, color, (cx - s, cy - s), (cx - s, cy - s + arm), th)
        # Top-right
        pygame.draw.line(surface, color, (cx + s, cy - s), (cx + s - arm, cy - s), th)
        pygame.draw.line(surface, color, (cx + s, cy - s), (cx + s, cy - s + arm), th)
        # Bottom-left
        pygame.draw.line(surface, color, (cx - s, cy + s), (cx - s + arm, cy + s), th)
        pygame.draw.line(surface, color, (cx - s, cy + s), (cx - s, cy + s - arm), th)
        # Bottom-right
        pygame.draw.line(surface, color, (cx + s, cy + s), (cx + s - arm, cy + s), th)
        pygame.draw.line(surface, color, (cx + s, cy + s), (cx + s, cy + s - arm), th)

    @staticmethod
    def draw_home_icon(surface, cx, cy, size, color):
        pts = [(cx, cy - size * 0.5), (cx - size * 0.5, cy), (cx + size * 0.5, cy)]
        pygame.draw.polygon(surface, color, pts)
        rw = size * 0.65
        rh = size * 0.45
        pygame.draw.rect(surface, color, (cx - rw // 2, cy, rw, rh), border_radius=1)

    @staticmethod
    def draw_back_icon(surface, cx, cy, size, color):
        th = 2
        pygame.draw.line(surface, color, (cx + size * 0.3, cy - size * 0.45), (cx - size * 0.35, cy), th)
        pygame.draw.line(surface, color, (cx - size * 0.35, cy), (cx + size * 0.3, cy + size * 0.45), th)

    @staticmethod
    def draw_theme_icon(surface, cx, cy, size, is_dark, theme):
        r = int(size * 0.45)
        pygame.draw.circle(surface, theme["text_secondary"], (cx, cy), r, 2)
        # Inner two-tone representation
        rect = pygame.Rect(cx - r, cy - r, r, r * 2)
        pygame.draw.circle(surface, theme["accent_amber" if is_dark else "accent_blue"], (cx, cy), r - 3)

    @staticmethod
    def draw_bulb_icon(surface, cx, cy, size, color):
        r = int(size * 0.32)
        pygame.draw.circle(surface, color, (cx, cy - int(size * 0.15)), r)
        base_w = int(size * 0.35)
        base_h = int(size * 0.28)
        pygame.draw.rect(surface, color, (cx - base_w // 2, cy + int(size * 0.12), base_w, base_h), border_radius=1)

    @staticmethod
    def draw_del_icon(surface, cx, cy, size, color):
        # Backspace tag polygon
        w = size * 0.8
        h = size * 0.65
        pts = [
            (cx - w * 0.5, cy),
            (cx - w * 0.15, cy - h * 0.5),
            (cx + w * 0.5, cy - h * 0.5),
            (cx + w * 0.5, cy + h * 0.5),
            (cx - w * 0.15, cy + h * 0.5)
        ]
        pygame.draw.polygon(surface, color, pts, 2)
        # Inner 'x'
        arm = size * 0.14
        mid_x = cx + size * 0.12
        pygame.draw.line(surface, color, (mid_x - arm, cy - arm), (mid_x + arm, cy + arm), 2)
        pygame.draw.line(surface, color, (mid_x - arm, cy + arm), (mid_x + arm, cy - arm), 2)

    @staticmethod
    def draw_reset_icon(surface, cx, cy, size, color):
        r = int(size * 0.38)
        rect = pygame.Rect(cx - r, cy - r, r * 2, r * 2)
        pygame.draw.arc(surface, color, rect, math.pi * 0.2, math.pi * 1.8, 2)
        # Arrowhead
        ax = cx + int(r * math.cos(math.pi * 0.2))
        ay = cy - int(r * math.sin(math.pi * 0.2))
        pts = [(ax - 4, ay - 4), (ax + 4, ay), (ax - 4, ay + 4)]
        pygame.draw.polygon(surface, color, pts)

    @staticmethod
    def draw_levels_icon(surface, cx, cy, size, color):
        # 3 ascending step bars
        bw = int(size * 0.22)
        gap = int(size * 0.10)
        start_x = cx - bw - gap
        pygame.draw.rect(surface, color, (start_x, cy + int(size * 0.1), bw, int(size * 0.3)), border_radius=1)
        pygame.draw.rect(surface, color, (start_x + bw + gap, cy - int(size * 0.1), bw, int(size * 0.5)), border_radius=1)
        pygame.draw.rect(surface, color, (start_x + (bw + gap) * 2, cy - int(size * 0.35), bw, int(size * 0.75)), border_radius=1)

    @staticmethod
    def draw_3d_panel(surface, rect, bg, border, shadow, depth=4, radius=10, inset=False):
        r = pygame.Rect(rect)
        if not inset:
            # Physical Drop Shadow
            s_rect = pygame.Rect(r.x, r.y + depth, r.w, r.h)
            pygame.draw.rect(surface, shadow, s_rect, border_radius=radius)
            # Body
            pygame.draw.rect(surface, bg, r, border_radius=radius)
            # Top-edge light bevel
            hl = adjust_brightness(bg, 1.25)
            pygame.draw.line(surface, hl, (r.x + radius, r.y + 1), (r.right - radius, r.y + 1), 1)
            # Outer border
            pygame.draw.rect(surface, border, r, 1, border_radius=radius)
        else:
            # Recessed Inset (Gauge/Display Look)
            pygame.draw.rect(surface, bg, r, border_radius=radius)
            # Inner top/left shadow line
            sh = adjust_brightness(bg, 0.65)
            pygame.draw.line(surface, sh, (r.x + radius, r.y + 1), (r.right - radius, r.y + 1), 1)
            pygame.draw.line(surface, sh, (r.x + 1, r.y + radius), (r.x + 1, r.bottom - radius), 1)
            pygame.draw.rect(surface, border, r, 1, border_radius=radius)

    @staticmethod
    def draw_led_indicator(surface, cx, cy, state):
        """Draws a tactile hardware instrument LED jewel indicator."""
        # Metallic outer bezel
        pygame.draw.circle(surface, (60, 72, 95), (cx, cy), 7)
        pygame.draw.circle(surface, (25, 32, 45), (cx, cy), 6)

        # Core LED color
        if state == "TRY":
            core = (245, 158, 11)   # Amber
        elif state == "WRONG":
            core = (239, 68, 68)   # Crimson Red Alert
        elif state == "BACKTRACK":
            core = (59, 130, 246)  # Blue
        elif state == "SOLVED":
            core = (16, 185, 129)  # Emerald
        else:
            core = (100, 116, 139) # Idle Gray

        pygame.draw.circle(surface, core, (cx, cy), 5)
        # Specular light gleam on glass
        pygame.draw.circle(surface, (255, 255, 255), (cx - 2, cy - 2), 1)


# ---------------------------------------------------------------------------
# TACTILE 3D BUTTON (WITH PHYSICAL CLICK DEPTH)
# ---------------------------------------------------------------------------
class Button:
    """
    Tactile 3D button that depresses mechanically when clicked, lifts on hover,
    and renders crisp procedural vector icons with ZERO broken Unicode boxes.
    """
    def __init__(self, rect, text, action_id, btn_type="secondary", icon=None, subtext=None):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.action_id = action_id
        self.btn_type = btn_type  # 'primary', 'secondary', 'accent', 'danger', 'warning'
        self.icon = icon          # 'play', 'pause', 'step', 'fullscreen', 'home', 'back', 'theme', 'bulb', 'reset', 'del', 'levels'
        self.subtext = subtext
        self.is_hovered = False
        self.is_pressed = False
        self.is_active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.is_pressed = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            was_pressed = self.is_pressed
            self.is_pressed = False
            if was_pressed and self.rect.collidepoint(event.pos):
                return self.action_id
        return None

    def render(self, surface, theme, fonts):
        bg_key = f"btn_{self.btn_type}_bg"
        bg_col = theme.get(bg_key, (45, 55, 75))
        if self.is_active:
            bg_col = theme["accent_blue"]

        # Mechanical 3D Elevation
        elevation = 1 if self.is_pressed else (5 if self.is_hovered else 4)
        shadow_col = theme.get("panel_shadow", (8, 10, 16))

        # 1. Base shadow
        s_rect = pygame.Rect(self.rect.x, self.rect.y + 4, self.rect.w, self.rect.h)
        pygame.draw.rect(surface, shadow_col, s_rect, border_radius=8)

        # 2. Front physical surface
        front_y = self.rect.y + (4 - elevation)
        front_rect = pygame.Rect(self.rect.x, front_y, self.rect.w, self.rect.h)
        pygame.draw.rect(surface, bg_col, front_rect, border_radius=8)

        # 3. Top-edge light bevel highlight
        hl = adjust_brightness(bg_col, 1.35)
        pygame.draw.line(surface, hl, (front_rect.x + 8, front_rect.y + 1), (front_rect.right - 8, front_rect.y + 1), 1)

        # 4. Bottom-edge dark bevel shade
        sh = adjust_brightness(bg_col, 0.70)
        pygame.draw.line(surface, sh, (front_rect.x + 8, front_rect.bottom - 1), (front_rect.right - 8, front_rect.bottom - 1), 1)

        # Border
        b_col = theme["card_border"] if self.btn_type == "secondary" and not self.is_active else adjust_brightness(bg_col, 1.15)
        pygame.draw.rect(surface, b_col, front_rect, 1, border_radius=8)

        # Text and Vector Icon rendering
        txt_col = (255, 255, 255) if (self.is_hovered or self.is_active or self.btn_type != "secondary") else theme["text_primary"]
        font = fonts["btn_bold"] if len(self.text) <= 12 else fonts["btn"]

        # Icon offset calculation
        icon_size = 14
        has_icon = (self.icon is not None)
        text_surf = font.render(self.text, True, txt_col)

        if has_icon and self.text:
            total_w = icon_size + 8 + text_surf.get_width()
            start_x = front_rect.centerx - total_w // 2
            icon_cx = start_x + icon_size // 2
            text_x = start_x + icon_size + 8

            self._draw_icon(surface, icon_cx, front_rect.centery, icon_size, txt_col, theme)
            surface.blit(text_surf, text_surf.get_rect(midleft=(text_x, front_rect.centery)))

        elif has_icon and not self.text:
            self._draw_icon(surface, front_rect.centerx, front_rect.centery, icon_size, txt_col, theme)

        else:
            if self.subtext:
                surface.blit(text_surf, text_surf.get_rect(center=(front_rect.centerx, front_rect.centery - 8)))
                sub_surf = fonts["caption"].render(self.subtext, True, theme["text_muted"])
                surface.blit(sub_surf, sub_surf.get_rect(center=(front_rect.centerx, front_rect.centery + 10)))
            else:
                surface.blit(text_surf, text_surf.get_rect(center=front_rect.center))

    def _draw_icon(self, surface, cx, cy, size, color, theme):
        if self.icon == "play":
            Draw3D.draw_play_icon(surface, cx, cy, size, color)
        elif self.icon == "pause":
            Draw3D.draw_pause_icon(surface, cx, cy, size, color)
        elif self.icon == "step":
            Draw3D.draw_step_icon(surface, cx, cy, size, color)
        elif self.icon == "fullscreen":
            Draw3D.draw_fullscreen_icon(surface, cx, cy, size, color)
        elif self.icon == "home":
            Draw3D.draw_home_icon(surface, cx, cy, size, color)
        elif self.icon == "back":
            Draw3D.draw_back_icon(surface, cx, cy, size, color)
        elif self.icon == "theme":
            Draw3D.draw_theme_icon(surface, cx, cy, size, theme["name"] == "dark", theme)
        elif self.icon == "bulb":
            Draw3D.draw_bulb_icon(surface, cx, cy, size, color)
        elif self.icon == "reset":
            Draw3D.draw_reset_icon(surface, cx, cy, size, color)
        elif self.icon == "del":
            Draw3D.draw_del_icon(surface, cx, cy, size, color)
        elif self.icon == "levels":
            Draw3D.draw_levels_icon(surface, cx, cy, size, color)


# ---------------------------------------------------------------------------
# SUDOKU SOLVER: DFS WITH SLOW STEP-BY-STEP BACKTRACKING & MRV
# ---------------------------------------------------------------------------
class SudokuSolver:
    """
    Theoretical AI Foundations of the Sudoku Solver:
    -------------------------------------------------
    1. Constraint Satisfaction Problem (CSP):
       - Variables: 81 cells X_rc for r, c in [0..8].
       - Domain: D_rc subset of {1, 2, ..., 9}.
       - Constraints: All-Diff across each Row, Column, and 3x3 Box.

    2. Educational Step-by-Step Visual AI Solver:
       - Uses Depth-First Search (DFS) with recursive backtracking.
       - Implemented as a Python generator (`yield`), enabling non-blocking
         synchronization with the Pygame frame loop.
       - Deliberately exposes each micro-step of AI reasoning:
           a) 'TRY' -> Candidate digit placed in 3D Amber.
           b) 'WRONG' -> Dead-end detected downstream. Flashes the cell in
              bright 3D CRIMSON RED to clearly show the AI making a mistake and realizing it!
           c) 'BACKTRACK' -> Erases the digit from the cell and backtracks up
              the search tree to explore the next candidate.
           d) 'SOLVED' -> Marks completion.

    3. Minimum Remaining Values (MRV) Heuristic:
       - Background solver for hints and instant validation.
       - Chooses the cell with the smallest domain size (fail-first principle).
    """

    @staticmethod
    def get_candidates(board, r, c):
        if board[r][c] != 0:
            return set()
        used = set(board[r])
        for i in range(9):
            used.add(board[i][c])
        br, bc = (r // 3) * 3, (c // 3) * 3
        for i in range(3):
            for j in range(3):
                used.add(board[br + i][bc + j])
        return set(range(1, 10)) - used

    @staticmethod
    def is_valid_placement(board, r, c, val):
        for i in range(9):
            if i != c and board[r][i] == val:
                return False
            if i != r and board[i][c] == val:
                return False
        br, bc = (r // 3) * 3, (c // 3) * 3
        for i in range(3):
            for j in range(3):
                nr, nc = br + i, bc + j
                if (nr != r or nc != c) and board[nr][nc] == val:
                    return False
        return True

    @staticmethod
    def find_all_conflicts(board):
        conflicts = set()
        for r in range(9):
            seen = {}
            for c in range(9):
                val = board[r][c]
                if val != 0:
                    if val in seen:
                        conflicts.add((r, c))
                        conflicts.add((r, seen[val]))
                    else:
                        seen[val] = c

        for c in range(9):
            seen = {}
            for r in range(9):
                val = board[r][c]
                if val != 0:
                    if val in seen:
                        conflicts.add((r, c))
                        conflicts.add((seen[val], c))
                    else:
                        seen[val] = r

        for br in range(0, 9, 3):
            for bc in range(0, 9, 3):
                seen = {}
                for i in range(3):
                    for j in range(3):
                        r, c = br + i, bc + j
                        val = board[r][c]
                        if val != 0:
                            if val in seen:
                                conflicts.add((r, c))
                                conflicts.add(seen[val])
                            else:
                                seen[val] = (r, c)
        return conflicts

    @classmethod
    def solve_mrv(cls, board):
        b = [row[:] for row in board]

        def _solve(current):
            empty_cells = []
            for r in range(9):
                for c in range(9):
                    if current[r][c] == 0:
                        cands = cls.get_candidates(current, r, c)
                        if not cands:
                            return None
                        empty_cells.append((len(cands), r, c, cands))

            if not empty_cells:
                return current

            empty_cells.sort(key=lambda item: item[0])
            _, r, c, cands = empty_cells[0]

            for val in sorted(cands):
                current[r][c] = val
                res = _solve(current)
                if res is not None:
                    return res
                current[r][c] = 0

            return None

        return _solve(b)

    @classmethod
    def count_solutions(cls, board, limit=2):
        count = 0

        def _solve(b):
            nonlocal count
            if count >= limit:
                return
            empty_cells = []
            for r in range(9):
                for c in range(9):
                    if b[r][c] == 0:
                        cands = cls.get_candidates(b, r, c)
                        if not cands:
                            return
                        empty_cells.append((len(cands), r, c, cands))
            if not empty_cells:
                count += 1
                return

            empty_cells.sort(key=lambda x: x[0])
            _, r, c, cands = empty_cells[0]
            for val in cands:
                b[r][c] = val
                _solve(b)
                b[r][c] = 0
                if count >= limit:
                    return

        _solve([row[:] for row in board])
        return count

    @classmethod
    def visual_dfs_generator(cls, board, empty_cells, stats):
        """
        Educational Visual DFS Generator with Slow Mistake & Backtrack Revealing.
        -----------------------------------------------------------------------
        Yields state tuples:
            ('TRY', r, c, val, message)
            ('WRONG', r, c, val, message)      -> Flashes the failed digit in 3D RED
            ('BACKTRACK', r, c, 0, message)    -> Erases the cell and steps back
            ('SOLVED', None, None, None, message)
            ('UNSOLVABLE', None, None, None, message)
        """
        def _dfs_step(idx):
            if idx >= len(empty_cells):
                yield ("SOLVED", None, None, None, "PUZZLE SOLVED: All constraints satisfied!")
                return True

            r, c = empty_cells[idx]

            # Try candidate digits 1 through 9
            for digit in range(1, 10):
                if cls.is_valid_placement(board, r, c, digit):
                    # 1. TRY: Assign candidate and advance branch
                    board[r][c] = digit
                    stats["explored"] += 1
                    yield ("TRY", r, c, digit, f"TESTING candidate {digit} at Row {r+1}, Col {c+1}")

                    # Recursive search downstream
                    solved = yield from _dfs_step(idx + 1)
                    if solved:
                        return True

                    # 2. WRONG: Downstream branch encountered a dead end!
                    # Make it crystal clear to the user that this digit was wrong:
                    stats["backtracks"] += 1
                    yield ("WRONG", r, c, digit, f"DEAD END! Candidate {digit} at Row {r+1}, Col {c+1} failed downstream.")

                    # 3. BACKTRACK: Clear cell and revert
                    board[r][c] = 0
                    yield ("BACKTRACK", r, c, 0, f"BACKTRACK: Erased ({r+1}, {c+1}) to test next digit.")

            return False

        has_solution = yield from _dfs_step(0)
        if not has_solution:
            yield ("UNSOLVABLE", None, None, None, "No valid solution exists for this board.")


# ---------------------------------------------------------------------------
# SUDOKU GENERATOR (8 DIFFICULTY TIERS)
# ---------------------------------------------------------------------------
class SudokuGenerator:
    """
    Generates authentic, mathematically guaranteed puzzles across 8 tiers:
      1. Beginner     : 60 Clues (~21 empty cells)
      2. Easy         : 52 Clues (~29 empty cells)
      3. Medium       : 44 Clues (~37 empty cells)
      4. Hard         : 38 Clues (~43 empty cells)
      5. Expert       : 32 Clues (~49 empty cells)
      6. Master       : 27 Clues (~54 empty cells)
      7. Grandmaster  : 22 Clues (~59 empty cells)
      8. Impossible   : 17 Clues (~64 empty cells - Theoretical Minimum!)
    """
    DIFFICULTY_TIERS = [
        {"id": 0, "name": "Beginner", "clues": 60, "stars": 1, "desc": "Gentle warmup, ample clues"},
        {"id": 1, "name": "Easy", "clues": 52, "stars": 1, "desc": "Casual logical solving"},
        {"id": 2, "name": "Medium", "clues": 44, "stars": 2, "desc": "Standard balanced puzzle"},
        {"id": 3, "name": "Hard", "clues": 38, "stars": 3, "desc": "Advanced candidate filtering"},
        {"id": 4, "name": "Expert", "clues": 32, "stars": 4, "desc": "Complex elimination chains"},
        {"id": 5, "name": "Master", "clues": 27, "stars": 4, "desc": "Sparse clues, deep logic"},
        {"id": 6, "name": "Grandmaster", "clues": 22, "stars": 5, "desc": "Extreme deductive challenge"},
        {"id": 7, "name": "Impossible", "clues": 17, "stars": 5, "desc": "17-Clue minimal boundary"},
    ]

    BASE_17_STR = "000000010400000000020000000000050407008000300001090000300400200050100000000806000"
    _BASE_SOL = None

    @classmethod
    def apply_isomorphism(cls, board):
        b = [row[:] for row in board]
        # 1. Permute digits 1..9
        mapping = list(range(1, 10))
        random.shuffle(mapping)
        digit_map = {i + 1: mapping[i] for i in range(9)}
        digit_map[0] = 0
        b = [[digit_map[cell] for cell in row] for row in b]

        # 2. Permute rows within bands
        for band in range(0, 9, 3):
            rows = [0, 1, 2]
            random.shuffle(rows)
            band_rows = [b[band + r] for r in rows]
            for r in range(3):
                b[band + r] = band_rows[r]

        # 3. Permute columns within stacks
        for stack in range(0, 9, 3):
            cols = [0, 1, 2]
            random.shuffle(cols)
            for r in range(9):
                orig = [b[r][stack + c] for c in range(3)]
                for c in range(3):
                    b[r][stack + c] = orig[cols[c]]

        # 4. Permute bands
        bands = [0, 1, 2]
        random.shuffle(bands)
        new_b = []
        for band_idx in bands:
            new_b.extend(b[band_idx * 3:(band_idx + 1) * 3])
        b = new_b

        # 5. Permute stacks
        stacks = [0, 1, 2]
        random.shuffle(stacks)
        for r in range(9):
            row_copy = b[r][:]
            for s_idx, target_s in enumerate(stacks):
                for c in range(3):
                    b[r][s_idx * 3 + c] = row_copy[target_s * 3 + c]

        # 6. Random reflection
        if random.random() < 0.5:
            b = [[b[r][c] for r in range(9)] for c in range(9)]

        return b

    @classmethod
    def create_puzzle(cls, difficulty_tier_id):
        tier = cls.DIFFICULTY_TIERS[difficulty_tier_id]
        target_clues = tier["clues"]

        raw_17 = [[int(c) for c in cls.BASE_17_STR[r * 9:(r + 1) * 9]] for r in range(9)]
        if cls._BASE_SOL is None:
            cls._BASE_SOL = SudokuSolver.solve_mrv(raw_17)

        extra_clues_needed = target_clues - 17
        empty_cells = [(r, c) for r in range(9) for c in range(9) if raw_17[r][c] == 0]
        revealed_coords = random.sample(empty_cells, extra_clues_needed)

        base_board = [row[:] for row in raw_17]
        for r, c in revealed_coords:
            base_board[r][c] = cls._BASE_SOL[r][c]

        puzzle = cls.apply_isomorphism(base_board)
        solution = SudokuSolver.solve_mrv(puzzle)
        return puzzle, solution


# ---------------------------------------------------------------------------
# SUDOKU GRID CLASS: 3D TACTILE TILES & BOARD RENDERING
# ---------------------------------------------------------------------------
class SudokuGrid:
    """
    Manages the 9x9 board state, selection crosshairs, cell tagging,
    conflict tracking, and physical 3D tile rendering.
    """
    def __init__(self, puzzle, solution):
        self.initial_board = [row[:] for row in puzzle]
        self.current_board = [row[:] for row in puzzle]
        self.solution_board = [row[:] for row in solution]

        self.cell_types = {}
        for r in range(9):
            for c in range(9):
                if self.initial_board[r][c] != 0:
                    self.cell_types[(r, c)] = "initial"
                else:
                    self.cell_types[(r, c)] = "empty"

        self.selected_cell = (0, 0)
        self.conflicts = set()
        self.ai_active_cell = None
        self.ai_cell_state = None  # 'TRY', 'WRONG', 'BACKTRACK', 'SOLVED'
        self.update_conflicts()

    def update_conflicts(self):
        self.conflicts = SudokuSolver.find_all_conflicts(self.current_board)

    def select(self, r, c):
        if 0 <= r < 9 and 0 <= c < 9:
            self.selected_cell = (r, c)

    def move_selection(self, dr, dc):
        if self.selected_cell is None:
            self.selected_cell = (0, 0)
        else:
            r = (self.selected_cell[0] + dr) % 9
            c = (self.selected_cell[1] + dc) % 9
            self.selected_cell = (r, c)

    def set_cell_value(self, r, c, val, tag="user"):
        if self.cell_types.get((r, c)) == "initial":
            return False

        if val == 0:
            self.current_board[r][c] = 0
            self.cell_types[(r, c)] = "empty"
        else:
            self.current_board[r][c] = val
            self.cell_types[(r, c)] = tag

        self.update_conflicts()
        return True

    def reset_to_initial(self):
        for r in range(9):
            for c in range(9):
                if self.cell_types.get((r, c)) != "initial":
                    self.current_board[r][c] = 0
                    self.cell_types[(r, c)] = "empty"
        self.ai_active_cell = None
        self.ai_cell_state = None
        self.update_conflicts()

    def is_solved(self):
        if len(self.conflicts) > 0:
            return False
        for r in range(9):
            for c in range(9):
                if self.current_board[r][c] == 0:
                    return False
        return True

    def get_crosshair_cells(self):
        if self.selected_cell is None:
            return set()
        sel_r, sel_c = self.selected_cell
        cells = set()
        for i in range(9):
            cells.add((sel_r, i))
            cells.add((i, sel_c))
        br, bc = (sel_r // 3) * 3, (sel_c // 3) * 3
        for i in range(3):
            for j in range(3):
                cells.add((br + i, bc + j))
        return cells

    def render(self, surface, rect, theme, fonts):
        x_start, y_start, width, height = rect
        cell_size = width / 9.0

        # 1. 3D Recessed Grid Tray Base & Shadow
        Draw3D.draw_3d_panel(surface, (x_start - 6, y_start - 6, width + 12, height + 12),
                             theme["grid_tray_bg"], theme["grid_tray_border"], theme["panel_shadow"], depth=6, radius=12)

        # 2. Main Board Inner Surface
        pygame.draw.rect(surface, theme["grid_bg"], (x_start, y_start, width, height), border_radius=8)

        crosshair_cells = self.get_crosshair_cells()
        active_val = None
        if self.selected_cell:
            active_val = self.current_board[self.selected_cell[0]][self.selected_cell[1]]

        # 3. Individual 3D Cell Tiles
        for r in range(9):
            for c in range(9):
                tile_rect = pygame.Rect(
                    round(x_start + c * cell_size) + 2,
                    round(y_start + r * cell_size) + 2,
                    round(cell_size) - 3,
                    round(cell_size) - 3,
                )

                bg_color = theme["cell_base"]

                # Crosshair illumination
                if (r, c) in crosshair_cells:
                    bg_color = theme["cell_crosshair"]

                # Same digit illumination
                val = self.current_board[r][c]
                if active_val and active_val != 0 and val == active_val:
                    bg_color = theme["cell_same_digit"]

                # Selected Cell
                if self.selected_cell == (r, c):
                    bg_color = theme["cell_selected"]

                # AI Visualization States
                if self.ai_active_cell == (r, c):
                    if self.ai_cell_state == "TRY":
                        bg_color = theme["ai_searching_bg"]
                    elif self.ai_cell_state == "WRONG":
                        bg_color = theme["ai_wrong_bg"]
                    elif self.ai_cell_state == "BACKTRACK":
                        bg_color = theme["ai_backtrack_bg"]
                    elif self.ai_cell_state == "SOLVED":
                        bg_color = theme["ai_solved_bg"]

                # Conflict
                if (r, c) in self.conflicts:
                    bg_color = theme["cell_conflict_bg"]

                # Draw 3D cell tile with top highlight bevel
                pygame.draw.rect(surface, bg_color, tile_rect, border_radius=4)
                hl_line = adjust_brightness(bg_color, 1.25)
                pygame.draw.line(surface, hl_line, (tile_rect.x + 2, tile_rect.y + 1), (tile_rect.right - 2, tile_rect.y + 1), 1)

        # 4. Grid Divider Lines (with 3D groove depth)
        for i in range(10):
            is_thick = (i % 3 == 0)
            thickness = 3 if is_thick else 1
            line_color = theme["grid_line_thick"] if is_thick else theme["grid_line_thin"]

            y = round(y_start + i * cell_size)
            if is_thick and 0 < i < 9:
                # 3D groove shadow underneath 3x3 divider
                pygame.draw.line(surface, theme["grid_groove"], (x_start, y + 2), (x_start + width, y + 2), 1)
            pygame.draw.line(surface, line_color, (x_start, y), (x_start + width, y), thickness)

            x = round(x_start + i * cell_size)
            if is_thick and 0 < i < 9:
                pygame.draw.line(surface, theme["grid_groove"], (x + 2, y_start), (x + 2, y_start + height), 1)
            pygame.draw.line(surface, line_color, (x, y_start), (x, y_start + height), thickness)

        # 5. Glowing 3D Selected Cell Frame
        if self.selected_cell:
            sr, sc = self.selected_cell
            sel_rect = pygame.Rect(
                round(x_start + sc * cell_size) + 1,
                round(y_start + sr * cell_size) + 1,
                round(cell_size) - 1,
                round(cell_size) - 1,
            )
            pygame.draw.rect(surface, theme["cell_selected_border"], sel_rect, 3, border_radius=4)

        # 6. Digits (Crisp high-contrast rendering)
        for r in range(9):
            for c in range(9):
                val = self.current_board[r][c]
                if val != 0:
                    tag = self.cell_types.get((r, c), "empty")

                    if (r, c) in self.conflicts:
                        fg_color = theme["cell_conflict_fg"]
                    elif self.ai_active_cell == (r, c):
                        if self.ai_cell_state == "TRY":
                            fg_color = theme["ai_searching_fg"]
                        elif self.ai_cell_state == "WRONG":
                            fg_color = theme["ai_wrong_fg"]
                        elif self.ai_cell_state == "BACKTRACK":
                            fg_color = theme["ai_backtrack_fg"]
                        else:
                            fg_color = theme["ai_solved_fg"]
                    elif tag == "initial":
                        fg_color = theme["cell_initial"]
                    elif tag == "hint":
                        fg_color = theme["cell_hint"]
                    else:
                        fg_color = theme["cell_user"]

                    font_to_use = fonts["num_bold"] if tag == "initial" else fonts["num"]
                    text_surf = font_to_use.render(str(val), True, fg_color)
                    cx = round(x_start + (c + 0.5) * cell_size)
                    cy = round(y_start + (r + 0.5) * cell_size)
                    surface.blit(text_surf, text_surf.get_rect(center=(cx, cy)))


# ---------------------------------------------------------------------------
# MAIN APPLICATION CONTROLLER
# ---------------------------------------------------------------------------
class SudokuArenaApp:
    """
    Main Application Manager coordinating Fullscreen, Page Routing
    (Welcome, Levels, Game Arena), Timers, 3D Rendering, and Slow AI Visualization.
    """
    SCREEN_HOME = 0
    SCREEN_LEVELS = 1
    SCREEN_GAME = 2

    def __init__(self, headless=False):
        self.headless = headless
        if headless:
            os.environ["SDL_VIDEODRIVER"] = "dummy"

        self.is_fullscreen = False
        self.screen_w = 1240
        self.screen_h = 700

        flags = pygame.RESIZABLE
        self.screen = pygame.display.set_mode((self.screen_w, self.screen_h), flags)
        pygame.display.set_caption("Sudoku Arena: Human vs AI")

        self.clock = pygame.time.Clock()
        self.theme_manager = ThemeManager(start_dark=True)
        self.theme = self.theme_manager.palette
        self._init_fonts()

        # Navigation State
        self.current_screen = self.SCREEN_HOME

        # AI Speed Presets (Educational Pace)
        self.speed_presets = {
            "ultra_slow": {"name": "0.6s (Ultra Slow)", "interval": 0.60},
            "slow": {"name": "0.25s (Slow)", "interval": 0.25},
            "medium": {"name": "0.08s (Normal)", "interval": 0.08},
            "fast": {"name": "Fast (0.02s)", "interval": 0.02},
            "instant": {"name": "Instant (Max)", "interval": 0.00},
        }
        self.speed_id = "ultra_slow"
        self.ai_last_step_time = 0.0

        # Game State
        self.current_tier = 2  # Medium (44 clues) by default
        self.grid = None
        self.human_time = 0.0
        self.ai_time = 0.0
        self.is_human_active = True
        self.ai_running = False
        self.ai_generator = None
        self.ai_stats = {"explored": 0, "backtracks": 0}
        self.ai_status_message = "Ready. Press 'AI SOLVE' or 'STEP AI >' to start."
        self.ai_status_state = "IDLE"
        self.race_status = "HUMAN IN CONTROL"
        self.game_won = False
        self.won_by = None
        self.toast = None

        self._load_new_puzzle(self.current_tier)
        self._recalculate_layout()

    def _init_fonts(self):
        sys_fonts = ["segoeui", "arial", "helvetica", "dejavusans"]
        self.fonts = {
            "hero": pygame.font.SysFont(sys_fonts, 36, bold=True),
            "title": pygame.font.SysFont(sys_fonts, 24, bold=True),
            "subtitle": pygame.font.SysFont(sys_fonts, 13, bold=True),
            "btn": pygame.font.SysFont(sys_fonts, 12, bold=False),
            "btn_bold": pygame.font.SysFont(sys_fonts, 12, bold=True),
            "btn_large": pygame.font.SysFont(sys_fonts, 15, bold=True),
            "num": pygame.font.SysFont(sys_fonts, 26, bold=False),
            "num_bold": pygame.font.SysFont(sys_fonts, 26, bold=True),
            "small": pygame.font.SysFont(sys_fonts, 12, bold=False),
            "small_bold": pygame.font.SysFont(sys_fonts, 12, bold=True),
            "caption": pygame.font.SysFont(sys_fonts, 11, bold=False),
            "caption_bold": pygame.font.SysFont(sys_fonts, 11, bold=True),
            "mono_large": pygame.font.SysFont(["consolas", "courier"], 22, bold=True),
            "mono_medium": pygame.font.SysFont(["consolas", "courier"], 15, bold=True),
        }

    def toggle_fullscreen(self):
        self.is_fullscreen = not self.is_fullscreen
        if self.is_fullscreen:
            info = pygame.display.Info()
            self.screen_w = info.current_w
            self.screen_h = info.current_h
            self.screen = pygame.display.set_mode((self.screen_w, self.screen_h), pygame.FULLSCREEN | pygame.RESIZABLE)
        else:
            self.screen_w = 1240
            self.screen_h = 700
            self.screen = pygame.display.set_mode((self.screen_w, self.screen_h), pygame.RESIZABLE)
        self._recalculate_layout()
        self.set_toast(f"Fullscreen: {'ENABLED' if self.is_fullscreen else 'WINDOWED'}", "info", 1.5)

    def set_toast(self, message, m_type="info", duration=2.5):
        self.toast = (message, m_type, time.time() + duration)

    def _load_new_puzzle(self, tier_id):
        self.current_tier = tier_id
        puzzle, solution = SudokuGenerator.create_puzzle(self.current_tier)
        self.grid = SudokuGrid(puzzle, solution)
        self.human_time = 0.0
        self.ai_time = 0.0
        self.is_human_active = True
        self.ai_running = False
        self.ai_generator = None
        self.ai_stats = {"explored": 0, "backtracks": 0}
        self.ai_status_message = "Ready. Watch AI solve step-by-step or solve it yourself!"
        self.ai_status_state = "IDLE"
        self.race_status = "HUMAN IN CONTROL"
        self.game_won = False
        self.won_by = None

    def _recalculate_layout(self):
        w = self.screen_w
        h = self.screen_h

        # 1. HOME SCREEN CONTROLS
        cx = w // 2
        cy = h // 2
        btn_w, btn_h = 280, 48
        self.home_btn_play = Button((cx - btn_w // 2, cy - 25, btn_w, btn_h), "PLAY GAME", "go_game", "primary", icon="play")
        self.home_btn_levels = Button((cx - btn_w // 2, cy + 36, btn_w, btn_h), "SELECT DIFFICULTY", "go_levels", "secondary", icon="levels")
        self.home_btn_demo = Button((cx - btn_w // 2, cy + 97, btn_w, btn_h), "WATCH AI SOLVE (DEMO)", "demo_ai", "accent", icon="step")

        util_w = 135
        self.home_btn_theme = Button((cx - util_w - 6, cy + 160, util_w, 36), "THEME", "toggle_theme", "secondary", icon="theme")
        self.home_btn_fs = Button((cx + 6, cy + 160, util_w, 36), "FULLSCREEN", "toggle_fullscreen", "secondary", icon="fullscreen")

        # 2. LEVELS SCREEN CONTROLS
        self.levels_btn_back = Button((40, 25, 130, 36), "BACK TO HOME", "go_home", "secondary", icon="back")
        self.levels_btn_theme = Button((w - 260, 25, 105, 36), "THEME", "toggle_theme", "secondary", icon="theme")
        self.levels_btn_fs = Button((w - 145, 25, 105, 36), "SCREEN", "toggle_fullscreen", "secondary", icon="fullscreen")

        # 8 Level Cards in 4x2 grid
        card_w = min(260, (w - 120) // 4)
        card_h = 125
        grid_start_x = (w - (card_w * 4 + 30)) // 2
        grid_start_y = 125

        self.level_cards = []
        for i, tier in enumerate(SudokuGenerator.DIFFICULTY_TIERS):
            col = i % 4
            row = i // 4
            bx = grid_start_x + col * (card_w + 10)
            by = grid_start_y + row * (card_h + 16)
            btn = Button((bx, by, card_w, card_h), f"LEVEL {i+1}: {tier['name'].upper()}", f"select_level_{i}", "secondary", subtext=f"{tier['clues']} CLUES")
            self.level_cards.append(btn)

        # 3. GAME ARENA CONTROLS
        top_y = 16
        self.game_btn_home = Button((30, top_y, 90, 36), "HOME", "go_home", "secondary", icon="home")
        self.game_btn_levels = Button((128, top_y, 95, 36), "LEVELS", "go_levels", "secondary", icon="levels")
        self.game_btn_theme = Button((w - 230, top_y, 95, 36), "THEME", "toggle_theme", "secondary", icon="theme")
        self.game_btn_fs = Button((w - 128, top_y, 98, 36), "SCREEN", "toggle_fullscreen", "secondary", icon="fullscreen")

        # Responsive Sudoku Grid placement
        grid_size = min(530, h - 170)
        left_area_w = w * 0.54
        gx = max(30, int((left_area_w - grid_size) // 2))
        gy = 68
        self.grid_rect = (gx, gy, grid_size, grid_size)

        # Tactile 3D Numpad directly beneath board
        pad_y = gy + grid_size + 14
        pad_btn_w = (grid_size - 45) // 10
        pad_btn_h = 42
        self.game_numpad_buttons = []
        for n in range(1, 10):
            nx = gx + (n - 1) * (pad_btn_w + 5)
            self.game_numpad_buttons.append(Button((nx, pad_y, pad_btn_w, pad_btn_h), str(n), f"num_{n}", "secondary"))
        # Erase key
        nx = gx + 9 * (pad_btn_w + 5)
        self.game_btn_erase = Button((nx, pad_y, pad_btn_w, pad_btn_h), "DEL", "erase", "danger", icon="del")
        self.game_numpad_buttons.append(self.game_btn_erase)

        # Right Panel Placement
        px = max(gx + grid_size + 35, int(left_area_w + 10))
        pw = min(470, w - px - 30)

        # Card 1: Race Timers
        self.game_card1_rect = pygame.Rect(px, 68, pw, 78)

        # Card 2: AI Solver & Status Box
        self.game_card2_rect = pygame.Rect(px, 156, pw, 185)

        # Speed buttons inside Card 2
        sp_x = px + 16
        sp_y = 295
        sp_w = (pw - 32 - 16) // 5
        self.game_speed_buttons = []
        for i, (sid, sinfo) in enumerate([
            ("ultra_slow", "0.6s"),
            ("slow", "0.25s"),
            ("medium", "0.08s"),
            ("fast", "FAST"),
            ("instant", "MAX"),
        ]):
            bx = sp_x + i * (sp_w + 4)
            self.game_speed_buttons.append(Button((bx, sp_y, sp_w, 28), sinfo, f"speed_{sid}", "secondary"))

        # Card 3: Action Buttons
        act_y = 352
        act_w = (pw - 12) // 2
        self.game_btn_solve = Button((px, act_y, act_w, 42), "AI SOLVE", "ai_solve", "accent", icon="play")
        self.game_btn_step = Button((px + act_w + 12, act_y, act_w, 42), "STEP AI >", "ai_step", "primary", icon="step")

        self.game_btn_hint = Button((px, act_y + 50, act_w, 40), "HINT (MRV)", "hint", "warning", icon="bulb")
        self.game_btn_reset = Button((px + act_w + 12, act_y + 50, act_w, 40), "RESET BOARD", "reset", "danger", icon="reset")

        self.game_btn_new = Button((px, act_y + 98, pw, 40), "NEW PUZZLE", "new_game", "secondary")
        self.game_action_buttons = [
            self.game_btn_solve, self.game_btn_step, self.game_btn_hint,
            self.game_btn_reset, self.game_btn_new
        ]

        # Card 4: Keyboard Shortcuts
        self.game_card4_rect = pygame.Rect(px, 502, pw, 135)

    def trigger_hint(self):
        if self.game_won:
            return

        target_r, target_c = None, None
        if self.grid.selected_cell:
            sr, sc = self.grid.selected_cell
            if self.grid.current_board[sr][sc] == 0:
                target_r, target_c = sr, sc

        if target_r is None:
            empty_cells = []
            for r in range(9):
                for c in range(9):
                    if self.grid.current_board[r][c] == 0:
                        cands = SudokuSolver.get_candidates(self.grid.current_board, r, c)
                        empty_cells.append((len(cands), r, c))
            if not empty_cells:
                self.set_toast("Board is already full!", "warn", 1.5)
                return
            empty_cells.sort(key=lambda x: x[0])
            _, target_r, target_c = empty_cells[0]

        correct_val = self.grid.solution_board[target_r][target_c]
        self.grid.set_cell_value(target_r, target_c, correct_val, tag="hint")
        self.grid.select(target_r, target_c)
        self.set_toast(f"Hint: Placed {correct_val} at Row {target_r+1}, Col {target_c+1}", "success", 2.0)

        if self.grid.is_solved():
            self._handle_victory("HUMAN")

    def toggle_ai_solver(self):
        if self.game_won:
            return

        if self.ai_running:
            self.ai_running = False
            self.ai_status_message = "AI Solver Paused."
            self.race_status = "AI SOLVER PAUSED"
            self.set_toast("AI Solver paused.", "warn", 1.5)
            return

        self.is_human_active = False
        self.ai_running = True
        self.race_status = "AI SOLVING (STEP-BY-STEP)..."

        if self.ai_generator is None:
            for r in range(9):
                for c in range(9):
                    if self.grid.cell_types.get((r, c)) not in ("initial", "hint"):
                        self.grid.current_board[r][c] = 0
                        self.grid.cell_types[(r, c)] = "empty"
            self.grid.update_conflicts()

            empty_cells = [
                (r, c) for r in range(9) for c in range(9)
                if self.grid.current_board[r][c] == 0
            ]
            self.ai_stats = {"explored": 0, "backtracks": 0}
            self.ai_generator = SudokuSolver.visual_dfs_generator(
                self.grid.current_board, empty_cells, self.ai_stats
            )
            self.set_toast("AI Solver started!", "info", 1.5)

    def execute_single_ai_step(self):
        """Advances exactly 1 AI step for manual study."""
        if self.ai_generator is None:
            self.is_human_active = False
            for r in range(9):
                for c in range(9):
                    if self.grid.cell_types.get((r, c)) not in ("initial", "hint"):
                        self.grid.current_board[r][c] = 0
                        self.grid.cell_types[(r, c)] = "empty"
            self.grid.update_conflicts()
            empty_cells = [
                (r, c) for r in range(9) for c in range(9)
                if self.grid.current_board[r][c] == 0
            ]
            self.ai_stats = {"explored": 0, "backtracks": 0}
            self.ai_generator = SudokuSolver.visual_dfs_generator(
                self.grid.current_board, empty_cells, self.ai_stats
            )

        try:
            state, r, c, val, msg = next(self.ai_generator)
            self.ai_status_message = msg
            self.ai_status_state = state

            if state == "TRY":
                self.grid.ai_active_cell = (r, c)
                self.grid.ai_cell_state = "TRY"
                self.grid.cell_types[(r, c)] = "ai"

            elif state == "WRONG":
                self.grid.ai_active_cell = (r, c)
                self.grid.ai_cell_state = "WRONG"
                self.grid.current_board[r][c] = val

            elif state == "BACKTRACK":
                self.grid.ai_active_cell = (r, c)
                self.grid.ai_cell_state = "BACKTRACK"
                self.grid.current_board[r][c] = 0
                self.grid.cell_types[(r, c)] = "empty"

            elif state == "SOLVED":
                self.ai_running = False
                self.grid.ai_active_cell = None
                self.grid.ai_cell_state = None
                self.grid.update_conflicts()
                self._handle_victory("AI")

            elif state == "UNSOLVABLE":
                self.ai_running = False
                self.set_toast("Puzzle has no solution!", "error", 3.0)

        except StopIteration:
            self.ai_running = False

    def advance_ai_loop(self, dt):
        if not self.ai_running or self.ai_generator is None:
            return

        interval = self.speed_presets[self.speed_id]["interval"]
        current_time = time.time()

        if interval == 0.0:
            t0 = time.time()
            while self.ai_running and (time.time() - t0 < 0.035):
                self.execute_single_ai_step()
        else:
            if current_time - self.ai_last_step_time >= interval:
                self.ai_last_step_time = current_time
                self.execute_single_ai_step()

    def _handle_victory(self, winner):
        self.game_won = True
        self.won_by = winner
        self.ai_running = False
        if winner == "HUMAN":
            self.race_status = f"HUMAN WON ({self.human_time:.1f}s)!"
            self.set_toast(f"VICTORY! Solved in {self.human_time:.1f}s!", "success", 6.0)
        else:
            self.race_status = f"AI SOLVED IN {self.ai_time:.2f}s!"
            self.set_toast(f"AI Defeated Board in {self.ai_time:.2f}s!", "success", 6.0)

    def handle_cell_click(self, mouse_pos):
        gx, gy, gw, gh = self.grid_rect
        mx, my = mouse_pos
        if gx <= mx <= gx + gw and gy <= my <= gy + gh:
            cell_size = gw / 9.0
            col = int((mx - gx) // cell_size)
            row = int((my - gy) // cell_size)
            if 0 <= row < 9 and 0 <= col < 9:
                self.grid.select(row, col)

    def handle_action(self, action_id):
        if not action_id:
            return

        if action_id == "go_home":
            self.current_screen = self.SCREEN_HOME
        elif action_id == "go_levels":
            self.current_screen = self.SCREEN_LEVELS
        elif action_id == "go_game":
            self.current_screen = self.SCREEN_GAME

        elif action_id == "demo_ai":
            self._load_new_puzzle(self.current_tier)
            self.current_screen = self.SCREEN_GAME
            self.speed_id = "ultra_slow"
            self.toggle_ai_solver()

        elif action_id == "toggle_theme":
            self.theme = self.theme_manager.toggle()
        elif action_id == "toggle_fullscreen":
            self.toggle_fullscreen()

        elif action_id.startswith("select_level_"):
            tier_idx = int(action_id.split("_")[2])
            self._load_new_puzzle(tier_idx)
            self.current_screen = self.SCREEN_GAME
            self.set_toast(f"Loaded: {SudokuGenerator.DIFFICULTY_TIERS[tier_idx]['name']} Tier", "info", 2.0)

        elif action_id == "ai_solve":
            self.toggle_ai_solver()
        elif action_id == "ai_step":
            if self.ai_running:
                self.ai_running = False
            self.execute_single_ai_step()
        elif action_id == "hint":
            self.trigger_hint()
        elif action_id == "reset":
            self.grid.reset_to_initial()
            self.ai_running = False
            self.ai_generator = None
            self.ai_status_message = "Board reset to initial clues."
            self.ai_status_state = "IDLE"
            self.game_won = False
            self.set_toast("Board reset to initial clues.", "warn", 1.5)
        elif action_id == "new_game":
            self._load_new_puzzle(self.current_tier)
            self.set_toast("Fresh puzzle generated!", "info", 1.5)

        elif action_id.startswith("speed_"):
            self.speed_id = action_id.replace("speed_", "")
            s_name = self.speed_presets[self.speed_id]["name"]
            self.set_toast(f"AI Speed: {s_name}", "info", 1.5)

        elif action_id.startswith("num_"):
            val = int(action_id.split("_")[1])
            if self.grid.selected_cell:
                r, c = self.grid.selected_cell
                self.grid.set_cell_value(r, c, val, tag="user")
                if self.grid.is_solved():
                    self._handle_victory("HUMAN")
        elif action_id == "erase":
            if self.grid.selected_cell:
                r, c = self.grid.selected_cell
                self.grid.set_cell_value(r, c, 0)

    # -----------------------------------------------------------------------
    # RENDERING: SCREEN_HOME (WELCOME PAGE)
    # -----------------------------------------------------------------------
    def render_home_screen(self):
        w, h = self.screen_w, self.screen_h
        self.screen.fill(self.theme["bg"])

        cx = w // 2
        cy = h // 2

        # 3D Main Card Container
        card_w, card_h = 720, 500
        card_rect = pygame.Rect(cx - card_w // 2, cy - card_h // 2, card_w, card_h)
        Draw3D.draw_3d_panel(self.screen, card_rect, self.theme["panel_bg"], self.theme["panel_border"], self.theme["panel_shadow"], depth=8, radius=18)

        # Top Badge
        badge_surf = self.fonts["caption_bold"].render("TOURNAMENT EDITION  *  AI CSP ENGINE", True, self.theme["accent_blue"])
        self.screen.blit(badge_surf, badge_surf.get_rect(center=(cx, cy - 190)))

        # Title
        title_surf = self.fonts["hero"].render("SUDOKU ARENA", True, self.theme["text_primary"])
        self.screen.blit(title_surf, title_surf.get_rect(center=(cx, cy - 145)))

        # Subtitle
        sub_surf = self.fonts["subtitle"].render("HUMAN VS ARTIFICIAL INTELLIGENCE", True, self.theme["text_secondary"])
        self.screen.blit(sub_surf, sub_surf.get_rect(center=(cx, cy - 105)))

        # Subtle divider groove
        pygame.draw.line(self.screen, self.theme["gauge_border"], (cx - 260, cy - 70), (cx + 260, cy - 70), 1)

        # Primary Buttons
        self.home_btn_play.render(self.screen, self.theme, self.fonts)
        self.home_btn_levels.render(self.screen, self.theme, self.fonts)
        self.home_btn_demo.render(self.screen, self.theme, self.fonts)

        # Utility Buttons
        self.home_btn_theme.render(self.screen, self.theme, self.fonts)
        self.home_btn_fs.render(self.screen, self.theme, self.fonts)

        # Footer
        cur_tier_name = SudokuGenerator.DIFFICULTY_TIERS[self.current_tier]["name"].upper()
        clues = SudokuGenerator.DIFFICULTY_TIERS[self.current_tier]["clues"]
        tier_sub = f"CURRENT TIER: {cur_tier_name} ({clues} CLUES)  |  PRESS F11 FOR FULLSCREEN"
        info_surf = self.fonts["caption"].render(tier_sub, True, self.theme["text_muted"])
        self.screen.blit(info_surf, info_surf.get_rect(center=(cx, cy + 220)))

    # -----------------------------------------------------------------------
    # RENDERING: SCREEN_LEVELS (DIFFICULTY SELECTION PAGE)
    # -----------------------------------------------------------------------
    def render_levels_screen(self):
        w, h = self.screen_w, self.screen_h
        self.screen.fill(self.theme["bg"])

        # Top Bar
        self.levels_btn_back.render(self.screen, self.theme, self.fonts)
        self.levels_btn_theme.render(self.screen, self.theme, self.fonts)
        self.levels_btn_fs.render(self.screen, self.theme, self.fonts)

        # Headers
        t_surf = self.fonts["title"].render("CHOOSE DIFFICULTY TIER", True, self.theme["text_primary"])
        self.screen.blit(t_surf, t_surf.get_rect(center=(w // 2, 45)))

        sub_surf = self.fonts["small"].render("8 mathematically calibrated tiers from 60 generous clues down to 17 minimal clues", True, self.theme["text_secondary"])
        self.screen.blit(sub_surf, sub_surf.get_rect(center=(w // 2, 75)))

        # 8 Level Cards
        for i, card in enumerate(self.level_cards):
            card.is_active = (i == self.current_tier)
            card.render(self.screen, self.theme, self.fonts)

            # Draw 5 Procedural 3D Vector Stars inside each card
            tier_info = SudokuGenerator.DIFFICULTY_TIERS[i]
            star_start_x = card.rect.centerx - 36
            star_y = card.rect.centery + 10
            Draw3D.draw_stars(self.screen, star_start_x, star_y, tier_info["stars"], total=5,
                              gold_col=self.theme["star_gold"], empty_col=self.theme["star_empty"])

            # Description
            desc_surf = self.fonts["caption"].render(tier_info["desc"], True, self.theme["text_secondary"] if card.is_active else self.theme["text_muted"])
            self.screen.blit(desc_surf, desc_surf.get_rect(center=(card.rect.centerx, card.rect.bottom - 16)))

        # Bottom Tip
        tip_surf = self.fonts["caption"].render("Every puzzle has a mathematically guaranteed unique solution.", True, self.theme["text_muted"])
        self.screen.blit(tip_surf, tip_surf.get_rect(center=(w // 2, h - 35)))

    # -----------------------------------------------------------------------
    # RENDERING: SCREEN_GAME (3D GAME ARENA)
    # -----------------------------------------------------------------------
    def render_game_screen(self):
        w, h = self.screen_w, self.screen_h
        self.screen.fill(self.theme["bg"])

        # Top Navigation Bar
        self.game_btn_home.render(self.screen, self.theme, self.fonts)
        self.game_btn_levels.render(self.screen, self.theme, self.fonts)
        self.game_btn_theme.render(self.screen, self.theme, self.fonts)
        self.game_btn_fs.render(self.screen, self.theme, self.fonts)

        # Current Level Pill
        cur_tier = SudokuGenerator.DIFFICULTY_TIERS[self.current_tier]
        level_str = f"LEVEL {self.current_tier + 1}: {cur_tier['name'].upper()} ({cur_tier['clues']} CLUES)"
        l_surf = self.fonts["subtitle"].render(level_str, True, self.theme["accent_blue"])
        self.screen.blit(l_surf, l_surf.get_rect(center=(w // 2, 34)))

        # 1. 3D Sudoku Board (Left Column)
        self.grid.render(self.screen, self.grid_rect, self.theme, self.fonts)

        # 3D Tactile Numpad
        for btn in self.game_numpad_buttons:
            btn.render(self.screen, self.theme, self.fonts)

        # 2. Right Side: Card 1 (Timers with Recessed Gauges)
        c1 = self.game_card1_rect
        Draw3D.draw_3d_panel(self.screen, c1, self.theme["card_bg"], self.theme["card_border"], self.theme["card_shadow"], depth=4, radius=10)

        # Human Timer Recessed Gauge
        gauge_w = (c1.width - 36) // 2
        g1_rect = pygame.Rect(c1.x + 12, c1.y + 12, gauge_w, c1.height - 24)
        Draw3D.draw_3d_panel(self.screen, g1_rect, self.theme["gauge_bg"], self.theme["gauge_border"], None, inset=True, radius=6)

        h_min = int(self.human_time) // 60
        h_sec = self.human_time % 60
        h_col = self.theme["accent_blue"] if self.is_human_active and not self.game_won else self.theme["text_primary"]
        self.screen.blit(self.fonts["caption"].render("HUMAN TIME", True, self.theme["text_secondary"]), (g1_rect.x + 10, g1_rect.y + 6))
        self.screen.blit(self.fonts["mono_large"].render(f"{h_min:02d}:{h_sec:04.1f}", True, h_col), (g1_rect.x + 10, g1_rect.y + 24))

        # AI Timer Recessed Gauge
        g2_rect = pygame.Rect(c1.x + 24 + gauge_w, c1.y + 12, gauge_w, c1.height - 24)
        Draw3D.draw_3d_panel(self.screen, g2_rect, self.theme["gauge_bg"], self.theme["gauge_border"], None, inset=True, radius=6)

        ai_col = self.theme["accent_amber"] if self.ai_running else self.theme["text_primary"]
        self.screen.blit(self.fonts["caption"].render("AI TIME", True, self.theme["text_secondary"]), (g2_rect.x + 10, g2_rect.y + 6))
        self.screen.blit(self.fonts["mono_large"].render(f"{self.ai_time:05.2f} s", True, ai_col), (g2_rect.x + 10, g2_rect.y + 24))

        # 3. Right Side: Card 2 (AI Visual Telemetry)
        c2 = self.game_card2_rect
        Draw3D.draw_3d_panel(self.screen, c2, self.theme["card_bg"], self.theme["card_border"], self.theme["card_shadow"], depth=4, radius=10)

        self.screen.blit(self.fonts["small_bold"].render("AI VISUAL SOLVER (DFS + BACKTRACKING)", True, self.theme["text_secondary"]), (c2.x + 16, c2.y + 14))

        # 3D Recessed Display Box with Hardware LED Jewel Indicator
        stat_box_rect = pygame.Rect(c2.x + 16, c2.y + 36, c2.width - 32, 44)
        Draw3D.draw_3d_panel(self.screen, stat_box_rect, self.theme["gauge_bg"], self.theme["gauge_border"], None, inset=True, radius=6)

        # Draw LED
        led_x = stat_box_rect.x + 16
        led_y = stat_box_rect.centery
        Draw3D.draw_led_indicator(self.screen, led_x, led_y, self.ai_status_state)

        # Status text
        msg_col = self.theme["accent_rose"] if self.ai_status_state == "WRONG" else (self.theme["accent_amber"] if self.ai_status_state == "TRY" else self.theme["text_primary"])
        msg_surf = self.fonts["btn_bold"].render(self.ai_status_message, True, msg_col)
        self.screen.blit(msg_surf, msg_surf.get_rect(midleft=(stat_box_rect.x + 32, stat_box_rect.centery)))

        # Counters
        col_w = (c2.width - 32) // 3
        self.screen.blit(self.fonts["caption"].render("Explored Choices:", True, self.theme["text_muted"]), (c2.x + 16, c2.y + 90))
        self.screen.blit(self.fonts["mono_medium"].render(f"{self.ai_stats['explored']:,}", True, self.theme["text_primary"]), (c2.x + 16, c2.y + 106))

        self.screen.blit(self.fonts["caption"].render("Backtracks (Wrong):", True, self.theme["text_muted"]), (c2.x + 16 + col_w, c2.y + 90))
        self.screen.blit(self.fonts["mono_medium"].render(f"{self.ai_stats['backtracks']:,}", True, self.theme["accent_rose"]), (c2.x + 16 + col_w, c2.y + 106))

        ratio = 0.0
        if self.ai_stats["explored"] > 0:
            ratio = (self.ai_stats["backtracks"] / self.ai_stats["explored"]) * 100
        self.screen.blit(self.fonts["caption"].render("Prune Ratio:", True, self.theme["text_muted"]), (c2.x + 16 + 2 * col_w, c2.y + 90))
        self.screen.blit(self.fonts["mono_medium"].render(f"{ratio:4.1f}%", True, self.theme["text_secondary"]), (c2.x + 16 + 2 * col_w, c2.y + 106))

        # Speed Selection label & pills
        self.screen.blit(self.fonts["caption"].render("AI Speed (Slow Decision Inspection):", True, self.theme["text_muted"]), (c2.x + 16, c2.y + 136))
        for btn in self.game_speed_buttons:
            btn.is_active = (btn.action_id == f"speed_{self.speed_id}")
            btn.render(self.screen, self.theme, self.fonts)

        # 4. Right Side: Card 3 (Action Controls)
        if self.ai_running:
            self.game_btn_solve.text = "PAUSE AI"
            self.game_btn_solve.icon = "pause"
            self.game_btn_solve.btn_type = "warning"
        else:
            self.game_btn_solve.text = "AI SOLVE"
            self.game_btn_solve.icon = "play"
            self.game_btn_solve.btn_type = "accent"

        for btn in self.game_action_buttons:
            btn.render(self.screen, self.theme, self.fonts)

        # 5. Right Side: Card 4 (Shortcuts)
        c4 = self.game_card4_rect
        Draw3D.draw_3d_panel(self.screen, c4, self.theme["card_bg"], self.theme["card_border"], self.theme["card_shadow"], depth=4, radius=10)

        self.screen.blit(self.fonts["caption_bold"].render("KEYBOARD SHORTCUTS", True, self.theme["text_secondary"]), (c4.x + 16, c4.y + 10))

        shortcuts = [
            ("Arrows", "Move cell"),
            ("1 - 9", "Place number"),
            ("Del / 0", "Erase cell"),
            ("H", "MRV Hint"),
            ("Space / S", "AI Solve / Pause"),
            ("F11", "Toggle Fullscreen"),
            ("N", "New Puzzle"),
            ("T", "Toggle Theme"),
        ]

        for i, (k, desc) in enumerate(shortcuts):
            col = 0 if i < 4 else 1
            row = i % 4
            kx = c4.x + 16 if col == 0 else c4.x + c4.width // 2 + 8
            ky = c4.y + 32 + row * 24

            k_surf = self.fonts["caption_bold"].render(f"[{k}]", True, self.theme["accent_blue"])
            self.screen.blit(k_surf, (kx, ky))
            d_surf = self.fonts["caption"].render(desc, True, self.theme["text_muted"])
            self.screen.blit(d_surf, (kx + k_surf.get_width() + 6, ky))

        # 6. Victory 3D Modal Overlay
        if self.game_won:
            modal_rect = pygame.Rect(self.grid_rect[0] + 40, self.grid_rect[1] + 160, self.grid_rect[2] - 80, 160)
            Draw3D.draw_3d_panel(self.screen, modal_rect, self.theme["card_bg"], self.theme["accent_blue"], self.theme["panel_shadow"], depth=10, radius=14)

            vic_title = "HUMAN VICTORY!" if self.won_by == "HUMAN" else "AI SOLVED THE BOARD!"
            t_surf = self.fonts["title"].render(vic_title, True, self.theme["text_primary"])
            self.screen.blit(t_surf, t_surf.get_rect(center=(modal_rect.centerx, modal_rect.y + 40)))

            time_str = f"Time: {self.human_time:.1f}s" if self.won_by == "HUMAN" else f"Time: {self.ai_time:.2f}s | Choices: {self.ai_stats['explored']} | Backtracks: {self.ai_stats['backtracks']}"
            sub_surf = self.fonts["btn_bold"].render(time_str, True, self.theme["accent_blue"])
            self.screen.blit(sub_surf, sub_surf.get_rect(center=(modal_rect.centerx, modal_rect.y + 75)))

            btn_sub = self.fonts["small_bold"].render("Press [N] for New Game or choose [LEVELS] at top", True, self.theme["text_muted"])
            self.screen.blit(btn_sub, btn_sub.get_rect(center=(modal_rect.centerx, modal_rect.y + 115)))

    def render_toasts(self):
        if self.toast:
            text, t_type, exp_time = self.toast
            if time.time() < exp_time:
                toast_rect = pygame.Rect(self.screen_w // 2 - 200, 12, 400, 36)
                bg_col = self.theme["ai_solved_bg"] if t_type == "success" else self.theme["btn_primary_bg"]
                if t_type == "warn":
                    bg_col = self.theme["btn_warning_bg"]
                elif t_type == "error":
                    bg_col = self.theme["btn_danger_bg"]

                Draw3D.draw_3d_panel(self.screen, toast_rect, bg_col, adjust_brightness(bg_col, 1.25), self.theme["panel_shadow"], depth=4, radius=8)
                t_surf = self.fonts["btn_bold"].render(text, True, (255, 255, 255))
                self.screen.blit(t_surf, t_surf.get_rect(center=toast_rect.center))
            else:
                self.toast = None

    def render(self):
        if self.current_screen == self.SCREEN_HOME:
            self.render_home_screen()
        elif self.current_screen == self.SCREEN_LEVELS:
            self.render_levels_screen()
        elif self.current_screen == self.SCREEN_GAME:
            self.render_game_screen()

        self.render_toasts()
        pygame.display.flip()

    def update(self, dt):
        if self.current_screen == self.SCREEN_GAME:
            if self.is_human_active and not self.game_won:
                self.human_time += dt

            if self.ai_running and not self.game_won:
                self.ai_time += dt
                self.advance_ai_loop(dt)

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            return False

        if event.type == pygame.VIDEORESIZE:
            self.screen_w = max(1000, event.w)
            self.screen_h = max(650, event.h)
            self.screen = pygame.display.set_mode((self.screen_w, self.screen_h), pygame.RESIZABLE)
            self._recalculate_layout()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                self.toggle_fullscreen()
            elif event.key == pygame.K_t:
                self.theme = self.theme_manager.toggle()

        # Route events by screen
        if self.current_screen == self.SCREEN_HOME:
            for btn in [self.home_btn_play, self.home_btn_levels, self.home_btn_demo,
                        self.home_btn_theme, self.home_btn_fs]:
                act = btn.handle_event(event)
                if act:
                    self.handle_action(act)

        elif self.current_screen == self.SCREEN_LEVELS:
            for btn in [self.levels_btn_back, self.levels_btn_theme, self.levels_btn_fs] + self.level_cards:
                act = btn.handle_event(event)
                if act:
                    self.handle_action(act)

        elif self.current_screen == self.SCREEN_GAME:
            for btn in ([self.game_btn_home, self.game_btn_levels, self.game_btn_theme, self.game_btn_fs]
                        + self.game_speed_buttons + self.game_action_buttons + self.game_numpad_buttons):
                act = btn.handle_event(event)
                if act:
                    self.handle_action(act)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.handle_cell_click(event.pos)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.grid.move_selection(-1, 0)
                elif event.key == pygame.K_DOWN:
                    self.grid.move_selection(1, 0)
                elif event.key == pygame.K_LEFT:
                    self.grid.move_selection(0, -1)
                elif event.key == pygame.K_RIGHT:
                    self.grid.move_selection(0, 1)

                elif pygame.K_1 <= event.key <= pygame.K_9:
                    val = event.key - pygame.K_0
                    if self.grid.selected_cell:
                        r, c = self.grid.selected_cell
                        self.grid.set_cell_value(r, c, val, tag="user")
                        if self.grid.is_solved():
                            self._handle_victory("HUMAN")

                elif pygame.K_KP1 <= event.key <= pygame.K_KP9:
                    val = event.key - pygame.K_KP1 + 1
                    if self.grid.selected_cell:
                        r, c = self.grid.selected_cell
                        self.grid.set_cell_value(r, c, val, tag="user")
                        if self.grid.is_solved():
                            self._handle_victory("HUMAN")

                elif event.key in (pygame.K_BACKSPACE, pygame.K_DELETE, pygame.K_0, pygame.K_KP0):
                    if self.grid.selected_cell:
                        r, c = self.grid.selected_cell
                        self.grid.set_cell_value(r, c, 0)

                elif event.key == pygame.K_h:
                    self.trigger_hint()
                elif event.key in (pygame.K_s, pygame.K_SPACE):
                    self.toggle_ai_solver()
                elif event.key == pygame.K_n:
                    self.handle_action("new_game")
                elif event.key == pygame.K_r:
                    self.handle_action("reset")

        return True

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(60) / 1000.0

            for event in pygame.event.get():
                if not self.handle_event(event):
                    running = False

            self.update(dt)
            self.render()

        pygame.quit()
        sys.exit()


# ---------------------------------------------------------------------------
# ENTRY POINT
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    app = SudokuArenaApp()
    app.run()
