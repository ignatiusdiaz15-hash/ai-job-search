# Stage 3 — Scale (draft, awaiting approval)

Source: source/bancoora_original.png (750x750). Render is a tilted-perspective 3D view:
horizontal walls stay level; N–S walls converge to a vanishing point at (u=466, v=-4791 px).
Scale therefore varies by image row and differs between horizontal and vertical directions.
All measurements are taken on wall-top bands (same height for all walls), so edges = wall faces.

Scale basis (inside face to inside face, tape totals):
- Horizontal: side wall -> shower far wall = 102 in (A 66 + B 36)
- Vertical:   back wall -> door wall       = 119 in (C 69.5 + D 49.5)

| row (orig px) | horizontal px/in | in/px | vertical px/in | in/px |
|---|---|---|---|---|
| 110 (top of unit) | 1.171 | 0.854 | 0.999 | 1.001 |
| 353 (primary bath) | 1.229 | 0.814 | 1.100 | 0.909 |
| 735 (garage bottom) | 1.321 | 0.757 | 1.270 | 0.788 |

Split points disagree with drawn walls by ~4 in (see bath_tape_vs_plan.png):
- A/B split: 66 in mark lands on shower glass = wall D's *east* face line (65.6 in), not west face (61.4 in).
- C/D split: plan puts shower end at 65.7 in from back wall (53.3 from door wall); tape says 69.5 / 49.5.

Area check (outside faces of exterior walls): living 1,287 sq ft (±2%), garage 392 sq ft,
living+garage 1,679. Listed 1,400–1,401 -> living is 8% below; unresolved.

## Update — built-in 4 in shower shelf (user, after draft)
User reports a ~4 in built-in shelf inside the shower. Interpreting it as a ledge across the shower's
end wall (door side), the render draws that ledge as solid wall:
| | Tape | Plan | Diff |
|---|---|---|---|
| A to shower glass | 66 | 65.6 | -0.4 |
| B glass to far wall | 36 | 36.4 | +0.4 |
| C − 4 in shelf (back wall to shelf face) | 65.5 | 65.7 | +0.2 |
| D + 4 in shelf (door wall to shelf face) | 53.5 | 53.3 | -0.2 |
All four within 0.5 in -> no tape errors flagged. Pending user confirmation of shelf position/depth.
