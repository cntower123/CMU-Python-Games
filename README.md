# CMU Python Games

Three games I built in Python for my Grade 12 Computer Science Class using CMU Graphics.
| Game | File | Demo |
| --- | --- | --- |
| Tower Defense | `tower_defense.py` | [Watch the demo](ADD-YOUTUBE-LINK) |
| Tetris | `tetris.py` | [Watch the demo](ADD-YOUTUBE-LINK) |
| Easter Egg Hunt (Pac-Man) | `easter_egg_hunt.py` | [Watch the demo](ADD-YOUTUBE-LINK) |

## Tower Defense

My Gr 12 CS summative capstone. Place towers on a grid to stop 10 waves of enemies walking a winding path.

- Object-oriented design with four classes: `Enemy`, `Tower`, `Projectile` and `Wave`, organized as Model-View-Controller.
- Three tower types (Arrow, Cannon, Sniper). Each targets the closest enemy in range; the cannon does splash damage.
- Towers upgrade to level 3 (+50% damage, +15% range, faster firing).
- Three enemy types (normal, fast, tank) whose health scales with the wave number.
- The path is defined as grid cells and converted to pixel waypoints by finding where it changes direction.

**Controls:** `1` / `2` / `3` select a tower, click to place or upgrade, `Space` sends the next wave, `R` restarts.

## Tetris

Built step by step through the CMU course, then extended with my own features.

- Rotation that keeps the piece centred, legality checks, hard drop and line clearing on a 15×10 board.
- Added: ghost piece showing where the piece will land, next-piece preview, pause, levels every 5 lines with increasing speed, and scoring that rewards multi-line clears (100 / 300 / 500 / 800 × level).

**Controls:** arrow keys move, `Up` rotates, `Space` hard drops, `P` pauses.

## Easter Egg Hunt

My creative project: an Easter take on Pac-Man. A bunny collects 18 eggs while dodging foxes.

- Animated chomping mouth drawn with arcs, and wrap-around movement at the edges.
- Foxes steer toward the bunny and bounce off walls. The golden carrot makes them vulnerable for a few seconds.
- Circle-overlap collision detection, 3 lives with a respawn flicker, and a Caesar-cipher secret message on the win screen.

**Controls:** arrow keys move, `Space` starts and restarts.

