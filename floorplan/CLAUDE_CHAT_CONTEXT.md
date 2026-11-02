# The Bancoora: floor plan measurement context

Paste or upload this file into a Claude chat to continue the project. It is the complete record: the source plan, the scale model, every measurement, the owner's tape measurements, the corrections made, and what is still open.

## 1. Instructions for Claude (read first)

- You are helping the resident of an apartment measure it from a to-scale 3D floor plan render. All lengths are inches unless marked; feet-and-inches are given for convenience.
- **Source of truth order:** (1) the resident's tape measurements (section 4), (2) values derived from the drawing and scaled by the tape (section 5, `Source` column), (3) standard building sizes (Dream sheet, section 9). Never present a standard size or a guess as a measurement.
- When the resident gives a new tape measurement: compare it to the drawing value for the same span, report the % difference, update that room, and say whether it supports or changes the house-wide correction (section 3).
- Flag anything that differs from the drawing by more than 2 in as a possible tape error or drawing error, and ask before choosing one.
- Room names, IDs (R1, R6, ...) and wall names (N/S/E/W) are defined in section 5. North = top of the plan = front of the house (living-room windows).

## 2. Property and source plan

- **Plan:** The Bancoora, Ellery at Lake Sherwood, 8008 Balasands Blvd, Orlando, FL 32818. 3 bed / 2 bath, listed 1,400-1,401 sq ft (garage not included). 2-car attached garage.
- **Plan image:** official file https://media.apts247.info/07/079b724f82ff4840931632fe7a912077/floorplans/Bancoora_1401_183475.png (750 x 750 px), from https://www.elleryapartments.com/floorplans/?floorplan=the-bancoora. No 2D or larger version exists online (checked the property site and major listing sites).
- **Interactive viewer:** https://claude.ai/artifact/5xNDSaUXJe5SnkT8Z9BBjQ (private to the owner). Plan with overlays, room grid/midpoint, measure tool, furniture fit, Dream sheet, CSV export.
- **Repo copy:** `floorplan/` on branch `claude/floorplan-measurement-analyzer-1vqmr7` of `ignatiusdiaz15-hash/ai-job-search` (`measurements.json`, `bancoora_measurements.csv`, `bancoora_viewer.html`).

## 3. How the scale was found (and its limits)

- The image is a **tilted-perspective 3D render**, not a flat plan. Horizontal walls stay level; north-south walls converge to a vanishing point at image (u=466.4, v=-4791) px. Scale therefore changes by image row and differs between the two directions.
- Measurements were taken on the wall-top bands (all walls same height), whose edges are the wall faces. The plan was then straightened to a true top-down view.
- **Scale anchor:** the primary bathroom tape (102 in side wall to shower far wall = 66 + 36; 119 in back wall to door wall = 69.5 + 49.5). In the primary bath, 1 px = 0.81 in across and 0.91 in up-down (0.76-1.00 in over the whole image).
- Model (image px u,v -> plan inches X,Y): `X = Sh*(u-u0)/(v-v_vp)`, `Y = -Sv/(v-v_vp)` with Sh=4184.590, Sv=24045636.5, u0=466.425, v_vp=-4790.734. Frame used in this file: x = X - (-337.411), y = Y - (-5010.197); x grows east, y grows south, origin at the unit's north-west outer wall faces.
- **The drawing is not to one scale everywhere.** The primary bathroom matched the drawing, but the tape shows other rooms are larger than drawn: living room +4.7% side to side / +2.0% front to back; primary bedroom +3.9% / +0.5%. Rooms not yet taped are scaled by the average: **x 1.0433 side to side, x 1.0119 front to back**.
- **Area check:** drawing footprint (outside of exterior walls, garage excluded) = 1287 sq ft +/- 25; projected with the tape correction = **~1,354 sq ft** vs 1,400 listed. Garage footprint 392 sq ft.

## 4. Tape measurements taken by the resident

| Room | What was measured | Tape | Drawing | Difference |
|---|---|---|---|---|
| Primary bathroom | A: back wall, side wall to shower glass | 66 in (5' 6") | 65.6 in | +0.4 in (+0.6%) |
| Primary bathroom | B: shower width, glass to far wall | 36 in (3' 0") | 36.4 in | -0.4 in (-1.1%) |
| Primary bathroom | C: shower length, back wall to end wall (measured above the shelf) | 69.5 in (5' 9.5") | 65.7 in | +3.8 in (+5.8%) |
| Primary bathroom | D: door wall to shower corner | 49.5 in (4' 1.5") | 53.3 in | -3.8 in (-7.1%) |
| Living / dining | Front windows to corner by kitchen arch | 250 in (20' 10") | 245.2 in | +4.8 in (+2.0%) |
| Living / dining | Side to side, not counting the TV nook | 181 in (15' 1") | 172.8 in | +8.2 in (+4.7%) |
| Primary bedroom | Side to side (door wall to opposite wall) | 167 in (13' 11") | 160.8 in | +6.2 in (+3.9%) |
| Primary bedroom | Back to front, wall to wall including closet | 167 in (13' 11") | 166.2 in | +0.8 in (+0.5%) |

Notes from the resident: the primary shower has a built-in ledge ~4 in deep, floor to ~chest height (~4 ft, not taped), at the back-wall end (opposite the showerhead); the wall above it is set back 4 in. C (69.5) was measured above the ledge. The drawing draws the shower end wall where the ledge face would be (~3.8 in short), so C+D still total 119 in = the room depth.

## 5. Rooms

`Source`: tape = resident measured; scaled = drawing x house-wide tape correction (estimate); drawing = drawing only (primary-bath wing, anchored by the bath tape). Coordinates are inside wall faces in the frame above.

| ID | Room | Width E-W | Depth N-S | Area sq ft | Source | Confidence | Drawing showed | Frame x0-x1, y0-y1 |
|---|---|---|---|---|---|---|---|---|
| R1 | Primary bedroom | 167.0 (13' 11") | 167.0 (13' 11") | 193.7 +/-3.9 | tape | high | 160.8 x 166.2 | 4.5-165.2, 105.2-271.5 |
| R2 | Primary bathroom | 61.0 (5' 1") | 119.0 (9' 11") | 50.4 +/-2.1 | drawing | high | - | 4.5-65.5, 275.2-394.2 |
| R2s | Primary shower | 36.4 (3' 0.4") | 65.7 (5' 5.7") | 16.6 +/-0.9 | drawing | high | - | 70.0-106.4, 328.6-394.3 |
| R3 | Primary walk-in closet | 99.9 (8' 3.9") | 49.6 (4' 1.6") | 34.4 +/-1.5 | scaled | medium | 95.8 x 49.0 | 69.8-165.5, 275.2-324.2 |
| R3b | Linen closet (by kitchen) | 20.0 (1' 8") | 49.6 (4' 1.6") | 7.0 +/-0.4 | scaled | medium | 19.2 x 49.0 | 169.2-188.5, 275.2-324.2 |
| R4 | Laundry | 81.2 (6' 9.2") | 66.3 (5' 6.3") | 37.4 +/-1.6 | scaled | medium | 77.8 x 65.5 | 110.5-188.2, 328.8-394.2 |
| R5 | Kitchen | 135.4 (11' 3.4") | 119.6 (9' 11.6") | 112.4 +/-10.2 | scaled | medium | 129.8 x 118.2 | 192.5-322.2, 275.2-393.5 |
| R6 | Living / dining | 205.9 (17' 1.9") | 250.0 (20' 10") | 346.7 +/-6.9 | tape | high | 196.5 x 245.2 | 169.2-365.8, 30.0-275.2 |
| R6e | Entry closet / nook (walled in drawing) | 44.0 (3' 8") | 72.1 (6' 0.1") | 22.1 +/-2.5 | scaled | medium | 42.2 x 71.2 | 122.8-164.9, 30.0-101.2 |
| R7 | Bedroom 2 | 144.5 (12' 0.5") | 160.4 (13' 4.4") | 160.9 +/-14.3 | scaled | medium | 138.5 x 158.5 | 370.2-508.8, 4.2-162.8 |
| R7c | Closet (bedroom 2 side) | 21.4 (1' 9.4") | 83.8 (6' 11.8") | 12.5 +/-1.7 | scaled | medium | 20.5 x 82.8 | 345.5-366.0, 4.2-87.0 |
| R8 | Bathroom 2 | 117.4 (9' 9.4") | 64.3 (5' 4.3") | 52.4 +/-5.2 | scaled | medium | 112.5 x 63.5 | 419.2-531.8, 166.5-230.0 |
| R8v | Hall vestibule (bath 2) | 51.6 (4' 3.6") | 64.3 (5' 4.3") | 23.0 +/-2.5 | scaled | medium | 49.5 x 63.5 | 365.8-415.2, 166.5-230.0 |
| R9 | Bedroom 3 | 145.2 (12' 1.2") | 119.6 (9' 11.6") | 120.7 +/-10.9 | scaled | medium | 139.2 x 118.2 | 369.8-509.0, 234.0-352.2 |
| R10 | Storage / pantry hall | 41.7 (3' 5.7") | 120.4 (10' 0.4") | 34.9 +/-3.7 | scaled | medium | 40.0 x 119.0 | 326.2-366.2, 275.2-394.2 |
| R10b | Storage closet (lower right) | 83.7 (6' 11.7") | 38.7 (3' 2.7") | 22.5 +/-2.5 | scaled | medium | 80.2 x 38.2 | 366.2-446.5, 356.0-394.2 |
| G | Garage | 213.0 (17' 9") | 258.9 (21' 6.9") | 383.0 +/-32.2 | scaled | medium | 204.2 x 255.8 | 161.5-365.8, 403.2-659.0 |
| P | Patio / balcony | 87.0 (7' 3") | 37.2 (3' 1.2") | 22.5 +/-4.8 | drawing | low | - | 32.0-119.0, 64.0-101.2 |

Totals: rooms inside walls 1247.6 sq ft; garage 383.0 sq ft; patio 22.5 sq ft (railing edges, low confidence).

- **Living / dining is L-shaped.** Outline (frame inches): (169.2, 30.0), (342.0, 30.0), (342.0, 91.2), (365.8, 91.2), (365.8, 275.2), (169.2, 275.2). Tape-measured: 181 in side to side, not counting the TV nook; 250 in front windows to the corner by the kitchen arch.
- **Primary bathroom and shower:** use the tape values in section 4. Shower = 36 in wide x 69.5 in long above the ledge (65.5 in at the floor in front of the 4 in ledge); main bath floor 66 in from side wall to shower glass, 119 in back wall to door wall. The R2s row above is the drawing, which places the shower end wall ~3.8 in short.
- Primary bedroom: wall-to-wall depth includes a reach-in closet (~24-30 in deep, louvered doors); depth without it is ~137 in.
- Room centers (midpoints) are at half the width and half the depth from the walls above.

## 6. Openings, doors

| ID | Room | Item | Value | +/- | Confidence |
|---|---|---|---|---|---|
| O2 | R5 | Kitchen walkway, left of peninsula (peninsula meets right counter, so no walkway on the right) | 42.9 in (3' 6.9") | 5.1 | low |
| O4 | R8v | Hall opening to bedroom vestibule | 36.0 in (3' 0") | 2.4 | medium |
| O5 | R10 | Storage hall to lower storage closet | 40.4 in (3' 4.4") | 2.6 | medium |
| O6 | G | Garage overhead door opening | 174.0 in (14' 6") | 8.0 | medium |
| O7 | G | Garage side opening to entry landing | 36.6 in (3' 0.6") | 2.5 | medium |
| D2 | R1 | Primary bedroom door - ASSUMED standard width (not measured) | 32 in (2' 8") | 4.0 | low |
| D3 | R2 | Primary bathroom door - ASSUMED standard width (not measured) | 30 in (2' 6") | 4.0 | low |
| D4 | R3 | Primary walk-in closet door - ASSUMED standard width (not measured) | 28 in (2' 4") | 4.0 | low |
| D5 | R4 | Laundry door (kitchen side) - ASSUMED standard width (not measured) | 30 in (2' 6") | 4.0 | low |
| D6 | R4 | Laundry to garage door - ASSUMED standard width (not measured) | 32 in (2' 8") | 4.0 | low |
| D7 | R7 | Bedroom 2 door - ASSUMED standard width (not measured) | 30 in (2' 6") | 4.0 | low |
| D8 | R8 | Bathroom 2 door - ASSUMED standard width (not measured) | 28 in (2' 4") | 4.0 | low |
| D9 | R9 | Bedroom 3 door - ASSUMED standard width (not measured) | 30 in (2' 6") | 4.0 | low |
| D10 | R3b | Linen closet door (leaf drawn swinging into kitchen) - ASSUMED standard width (not measured) | 24 in (2' 0") | 4.0 | low |

Door widths **cannot be measured** from this render (a solid header is drawn over every doorway and door leaves lean in 3D); the values above are standard sizes assumed for swing arcs.

## 7. Fixtures (as drawn) and clearances (estimated)

Fixtures are stock 3D symbols. Because of the tilted view, anything shorter than the walls is drawn shifted toward the south-east and looks deeper (its front faces show). Treat fixture sizes as low confidence.

| Item | Width E-W x Depth N-S as drawn | Room |
|---|---|---|
| Primary bath double vanity (top incl. visible front face) | 33 x 70 in | R2 |
| Primary bath toilet | 35 x 23 in | R2 |
| Washer (stock symbol) | 16 x 22 in | R4 |
| Dryer (stock symbol) | 16 x 23 in | R4 |
| Kitchen peninsula (dark top, sink + dishwasher) | 68 x 38 in | R5 |
| Kitchen counter run - right wall | 17.2 x 99 in | R5 |
| Kitchen counter run - back wall (front edge partly hidden) | 129.8 x 12.5 in | R5 |
| White appliance, back-left (range or fridge - drawing unclear) | 24 x 18 in | R5 |
| Bath 2 tub (visible part; top hidden by wall face) | 47.8 x 36.0 in | R8 |
| Water heater (round) | 21 x 23 in | G |
| Primary bedroom reach-in closet zone (louvered doors) | 95 x 36.8 in | R1 |

| Clearance (estimated) | Estimate | Drawing showed | Basis |
|---|---|---|---|
| Toilet front to shower glass | 36.0 in +/-6.0 | 20.0 in | 66 in (tape) minus a ~30 in toilet; drawing shows 20 in because the toilet symbol is drawn shifted ~14 in east |
| Vanity front to shower glass (walkway) | 44.0 in +/-6.0 | 25.0 in | 66 in minus a standard 22 in vanity; drawn vanity includes its leaning front face |
| Toilet centerline to back wall (side clearance) | 18.0 in +/-6.0 | 10.8 in | drawing shifts the toilet ~7 in toward the back wall; code minimum is 15 in |
| Toilet centerline to end of vanity | 21.5 in +/-6.0 | 21.5 in | toilet and vanity shift by about the same amount, so the drawn value stands |
| Washer/dryer front to opposite wall | 48.0 in +/-6.0 | 42.2 in | 77.8 in laundry width minus ~30 in full-size machines (the drawn symbols are only 16 in deep) |
| Kitchen aisle, peninsula to back counter | 53.5 in +/-6.0 | 65.0 in | back counter front edge is hidden in the drawing; assumes a standard 25.5 in counter |

## 8. Corrections and audit history

- **Removed things the drawing does not show.** A 50 in "foyer to living room" opening and a front-door swing were artifacts: the drawing has a solid wall there, and the small walled space is now listed as an entry closet or nook. Two kitchen "openings" were split by the dark peninsula; it is one 43 in walkway on the left.
- **Fixtures are drawn shifted by the 3D view.** Anything shorter than the walls appears pushed toward the camera (south-east) and looks deeper because its front faces show. Drawn clearances around the toilet, vanity, washer/dryer and kitchen were biased; the estimates use your tape plus standard fixture depths.
- **Shower end wall moved 3.8 in toward the door.** Your tape (69.5 in + 49.5 in) adds to the room depth exactly, and the plan draws that wall where the 4 in shelf face would be. Best estimate uses your tape.
- **Closet and laundry share that wall.** If the wall really is 3.8 in further from the back wall, the walk-in closet is about 45 in deep and the laundry about 69 in. Tape these two before buying shelving or appliances.
- **Door widths are standard-size assumptions.** The render covers every doorway with a header and draws 3D leaning door leaves, so no door width could be measured. Swing arcs use typical sizes.
- **Fixtures use typical sizes.** Toilets, washer/dryer, tub, fridge and vanity are stock 3D symbols. Real appliances listed for this plan (full-size laundry, side-by-side fridge) are larger than drawn.
- **Living room tape explains most of the area gap.** Your living room is 4.7% wider and 2.0% deeper than drawn and your primary bedroom 3.9% wider and 0.5% deeper, while the primary bathroom matched the drawing. If the rest of the house is off the same way, the living area is about 1,354 sq ft against 1,400 listed, instead of 1,287. Bedroom 2 and 3 will confirm it.
- The living room and its east strip (TV wall) were merged into one L-shaped room at the resident's request.

## 9. Dream sheet (best estimates)

| Group | Item | Drawing | Best estimate | Likely range | Why | Confidence |
|---|---|---|---|---|---|---|
| Primary bathroom | Back wall, side wall to shower glass | 65.6 (plan) | 66 in (5' 6") | 64.5 - 67.5 in | Your tape (A). Plan agrees within 0.4 in. | high |
| Primary bathroom | Shower width, glass to far wall | 36.4 (plan) | 36 in (3' 0") | 34.5 - 37.5 in | Your tape (B). | high |
| Primary bathroom | Shower length, back wall to end wall (above shelf) | 65.7 (plan) | 69.5 in (5' 9.5") | 68 - 71 in | Your tape (C). Plan draws the end wall ~3.8 in short. | high |
| Primary bathroom | Shower floor length (in front of 4 in shelf) | - | 65.5 in (5' 5.5") | 63.5 - 67.5 in | 69.5 minus the 4 in built-in shelf at the back end (shelf ~4 ft tall, not tape-measured). | medium |
| Primary bathroom | Wall from door wall to shower corner | 53.3 (plan) | 49.5 in (4' 1.5") | 48 - 51 in | Your tape (D). Plan puts the corner ~3.8 in further from the door. | high |
| Primary bathroom | Room depth, back wall to door wall | 119.0 (plan) | 119 in (9' 11") | 117.5 - 120.5 in | Tape C + D; plan agrees exactly. | high |
| Primary bathroom | Main floor width, side wall to wall beside shower | 61.0 (plan) | 61 in (5' 1") | 59.6 - 62.4 in | Plan, inside faces. Not taped. | high |
| Primary walk-in closet | Depth (door wall to shower/laundry wall) | 49.0 (drawing) | 45.2 in (3' 9.2") | 43.5 - 49.5 in | If the shower end wall is 3.8 in off in the drawing and runs straight across (as drawn), the closet is that much shallower. Verify. | medium |
| Laundry | Depth (closet wall to back wall) | 65.5 (drawing) | 69.3 in (5' 9.3") | 65 - 71 in | Same wall as above: laundry gains what the closet loses. Verify. | medium |
| Living / dining | Depth, front windows to corner by kitchen arch | 245.2 (drawing) | 250 in (20' 10") | 248.5 - 251.5 in | Your tape. Drawing is 2.0% short here. | high |
| Living / dining | Width, side to side without the TV nook | 172.8 (drawing) | 181 in (15' 1") | 179.5 - 182.5 in | Your tape. Drawing is 4.7% narrow here. | high |
| Living / dining | Width to the TV wall | 196.5 (drawing) | 205.9 in (17' 1.9") | 202.9 - 208.9 in | Drawn width scaled by your tape (not taped directly). | medium |
| Primary bedroom | Side to side (door wall to opposite wall) | 160.8 (drawing) | 167 in (13' 11") | 165.5 - 168.5 in | Your tape. Drawing is 3.9% narrow here. | high |
| Primary bedroom | Back to front, wall to wall including closet | 166.2 (drawing) | 167 in (13' 11") | 165.5 - 168.5 in | Your tape. Drawing is within 1 in. | high |
| Kitchen | width (E-W) | 129.8 (drawing) | 135.4 in (11' 3.4") | 128.8 - 139.1 in | Best estimate: drawing scaled by the average of your living-room and bedroom tape (+4.3% side to side, +1.2% front to back). Not taped yet. | medium |
| Kitchen | depth (N-S) | 118.2 (drawing) | 119.6 in (9' 11.6") | 117.2 - 123 in | Best estimate: drawing scaled by the average of your living-room and bedroom tape (+4.3% side to side, +1.2% front to back). Not taped yet. | medium |
| Entry closet / nook (walled in drawing) | width (E-W) | 42.2 (drawing) | 44 in (3' 8") | 41.2 - 45.9 in | Best estimate: drawing scaled by the average of your living-room and bedroom tape (+4.3% side to side, +1.2% front to back). Not taped yet. | medium |
| Entry closet / nook (walled in drawing) | depth (N-S) | 71.2 (drawing) | 72.1 in (6' 0.1") | 70.2 - 74.5 in | Best estimate: drawing scaled by the average of your living-room and bedroom tape (+4.3% side to side, +1.2% front to back). Not taped yet. | medium |
| Bedroom 2 | width (E-W) | 138.5 (drawing) | 144.5 in (12' 0.5") | 137.5 - 148.4 in | Best estimate: drawing scaled by the average of your living-room and bedroom tape (+4.3% side to side, +1.2% front to back). Not taped yet. | medium |
| Bedroom 2 | depth (N-S) | 158.5 (drawing) | 160.4 in (13' 4.4") | 157.5 - 164.6 in | Best estimate: drawing scaled by the average of your living-room and bedroom tape (+4.3% side to side, +1.2% front to back). Not taped yet. | medium |
| Bathroom 2 | width (E-W) | 112.5 (drawing) | 117.4 in (9' 9.4") | 111.5 - 120.7 in | Best estimate: drawing scaled by the average of your living-room and bedroom tape (+4.3% side to side, +1.2% front to back). Not taped yet. | medium |
| Bathroom 2 | depth (N-S) | 63.5 (drawing) | 64.3 in (5' 4.3") | 62.5 - 66.6 in | Best estimate: drawing scaled by the average of your living-room and bedroom tape (+4.3% side to side, +1.2% front to back). Not taped yet. | medium |
| Bedroom 3 | width (E-W) | 139.2 (drawing) | 145.2 in (12' 1.2") | 138.2 - 149.1 in | Best estimate: drawing scaled by the average of your living-room and bedroom tape (+4.3% side to side, +1.2% front to back). Not taped yet. | medium |
| Bedroom 3 | depth (N-S) | 118.2 (drawing) | 119.6 in (9' 11.6") | 117.2 - 123 in | Best estimate: drawing scaled by the average of your living-room and bedroom tape (+4.3% side to side, +1.2% front to back). Not taped yet. | medium |
| Storage / pantry hall | width (E-W) | 40.0 (drawing) | 41.7 in (3' 5.7") | 39 - 43.5 in | Best estimate: drawing scaled by the average of your living-room and bedroom tape (+4.3% side to side, +1.2% front to back). Not taped yet. | medium |
| Storage / pantry hall | depth (N-S) | 119.0 (drawing) | 120.4 in (10' 0.4") | 118 - 123.8 in | Best estimate: drawing scaled by the average of your living-room and bedroom tape (+4.3% side to side, +1.2% front to back). Not taped yet. | medium |
| Storage closet (lower right) | width (E-W) | 80.2 (drawing) | 83.7 in (6' 11.7") | 79.2 - 86.4 in | Best estimate: drawing scaled by the average of your living-room and bedroom tape (+4.3% side to side, +1.2% front to back). Not taped yet. | medium |
| Storage closet (lower right) | depth (N-S) | 38.2 (drawing) | 38.7 in (3' 2.7") | 37.2 - 40.5 in | Best estimate: drawing scaled by the average of your living-room and bedroom tape (+4.3% side to side, +1.2% front to back). Not taped yet. | medium |
| Garage | width (E-W) | 204.2 (drawing) | 213 in (17' 9") | 203.2 - 218.3 in | Best estimate: drawing scaled by the average of your living-room and bedroom tape (+4.3% side to side, +1.2% front to back). Not taped yet. | medium |
| Garage | depth (N-S) | 255.8 (drawing) | 258.9 in (21' 6.9") | 254.8 - 265.1 in | Best estimate: drawing scaled by the average of your living-room and bedroom tape (+4.3% side to side, +1.2% front to back). Not taped yet. | medium |
| Primary bedroom | Depth excluding the reach-in closet | 167.0 (your tape, wall to wall) | 137 in (11' 5") | 130 - 143 in | Your 167 in minus a typical 24-30 in reach-in closet; the drawn closet zone (37 in) includes the leaning door faces. | medium |
| Clearances (estimated) | Toilet front to shower glass | 20.0 (drawn) | 36 in (3' 0") | 30 - 42 in | 66 in (tape) minus a ~30 in toilet; drawing shows 20 in because the toilet symbol is drawn shifted ~14 in east | low |
| Clearances (estimated) | Vanity front to shower glass (walkway) | 25.0 (drawn) | 44 in (3' 8") | 38 - 50 in | 66 in minus a standard 22 in vanity; drawn vanity includes its leaning front face | low |
| Clearances (estimated) | Toilet centerline to back wall (side clearance) | 10.8 (drawn) | 18 in (1' 6") | 12 - 24 in | drawing shifts the toilet ~7 in toward the back wall; code minimum is 15 in | low |
| Clearances (estimated) | Toilet centerline to end of vanity | 21.5 (drawn) | 21.5 in (1' 9.5") | 15.5 - 27.5 in | toilet and vanity shift by about the same amount, so the drawn value stands | low |
| Clearances (estimated) | Washer/dryer front to opposite wall | 42.2 (drawn) | 48 in (4' 0") | 42 - 54 in | 77.8 in laundry width minus ~30 in full-size machines (the drawn symbols are only 16 in deep) | low |
| Clearances (estimated) | Kitchen aisle, peninsula to back counter | 65.0 (drawn) | 53.5 in (4' 5.5") | 47.5 - 59.5 in | back counter front edge is hidden in the drawing; assumes a standard 25.5 in counter | low |
| Doors | Primary bedroom door | not measurable | 32 in (2' 8") | 28 - 36 in | Standard size ASSUMED. The render draws a solid header over every doorway, so widths cannot be measured. | low |
| Doors | Primary bathroom door | not measurable | 30 in (2' 6") | 26 - 34 in | Standard size ASSUMED. The render draws a solid header over every doorway, so widths cannot be measured. | low |
| Doors | Primary walk-in closet door | not measurable | 28 in (2' 4") | 24 - 32 in | Standard size ASSUMED. The render draws a solid header over every doorway, so widths cannot be measured. | low |
| Doors | Laundry door (kitchen side) | not measurable | 30 in (2' 6") | 26 - 34 in | Standard size ASSUMED. The render draws a solid header over every doorway, so widths cannot be measured. | low |
| Doors | Laundry to garage door | not measurable | 32 in (2' 8") | 28 - 36 in | Standard size ASSUMED. The render draws a solid header over every doorway, so widths cannot be measured. | low |
| Doors | Bedroom 2 door | not measurable | 30 in (2' 6") | 26 - 34 in | Standard size ASSUMED. The render draws a solid header over every doorway, so widths cannot be measured. | low |
| Doors | Bathroom 2 door | not measurable | 28 in (2' 4") | 24 - 32 in | Standard size ASSUMED. The render draws a solid header over every doorway, so widths cannot be measured. | low |
| Doors | Bedroom 3 door | not measurable | 30 in (2' 6") | 26 - 34 in | Standard size ASSUMED. The render draws a solid header over every doorway, so widths cannot be measured. | low |
| Doors | Linen closet door (leaf drawn swinging into kitchen) | not measurable | 24 in (2' 0") | 20 - 28 in | Standard size ASSUMED. The render draws a solid header over every doorway, so widths cannot be measured. | low |
| Doors | Garage overhead door opening | 174.0 (gap in wall) | 174 in (14' 6") | 166 - 182 in | Measured gap in the garage front wall. A 16 ft (192 in) door would not fit the 17 ft garage as drawn, so 14 ft 6 in is plausible. Verify. | medium |
| Fixtures (typical sizes, not measured) | Primary bath double vanity - typical 60 or 72 long x 21-22 deep | ~33 x 70 (top + leaning front face) | 66 in (5' 6") | 60 - 72 in | Stock symbol drawn with its front face, so it looks deeper than a real vanity. | low |
| Fixtures (typical sizes, not measured) | Primary bath toilet - typical ~20 wide x 28-30 deep | 35 x 23 footprint | 29 in (2' 5") | 27 - 31 in | Stock symbol. Drawn centerline is only 10.8 in from the back wall; code minimum is 15 in, so the real toilet sits further out. | low |
| Fixtures (typical sizes, not measured) | Washer and dryer (each) - typical 27 wide x 30-32 deep | 16 x 22 (each) | 27 in (2' 3") | 27 - 29 in | Listing says full-size; the symbols are far too small. | low |
| Fixtures (typical sizes, not measured) | Bath 2 tub - typical 60 long x 30 wide (alcove tub) | visible part only | 60 in (5' 0") | 59 - 61 in | Bathroom 2 is 63.5 in deep, which fits a standard 60 in tub. | low |
| Fixtures (typical sizes, not measured) | Refrigerator (position not identifiable in the drawing) - typical 33-36 wide x 30-34 deep | not identified | 36 in (3' 0") | 33 - 36 in | Listing says side-by-side; those are 33-36 in wide. | low |
| Fixtures (typical sizes, not measured) | Kitchen base counters - typical 25.5 deep | 14 deep visible (back run) | 25.5 in (2' 1.5") | 24 - 26 in | Standard counter depth; the back run's front edge is hidden by the 3D wall face. | low |
| Fixtures (typical sizes, not measured) | Kitchen aisle, peninsula to back counter - typical ~53.5 | 65.0 (to visible edge) | 53.5 in (4' 5.5") | 48 - 58 in | If the back counter is the standard 25.5 in deep. | low |
| Fixtures (typical sizes, not measured) | Water heater - typical 20-22 diameter | 20.8 x 22.2 | 21.5 in (1' 9.5") | 20 - 22 in | Typical 40-50 gallon tank; measured size agrees. | low |

## 10. Still open: what to measure next

1. **Bedroom 2:** door wall to opposite outside wall, and outside wall to the wall shared with bathroom 2 (estimate 144.5 x 160.4 in). Confirms whether the house-wide correction holds.
2. **Bedroom 3:** both walls (estimate 145.2 x 119.6 in).
3. **Primary walk-in closet depth** (best estimate ~45 in, drawing 49) and **laundry depth** (best estimate ~69 in, drawing 65.5): tests the shower-end-wall offset.
4. **Garage:** side to side and house wall to garage door (estimate 213.0 x 258.9 in).
5. Real fixture sizes and door widths, if needed for furniture or appliance decisions.

## 11. Prompt to start a new chat

```
I'm attaching the measurement record for my apartment (The Bancoora floor plan). Read section 1 first and treat my tape measurements as the source of truth. I'll give you new tape measurements or ask fit/layout questions; update the numbers and tell me how each new measurement compares to the drawing.
```

_Generated 2026-11-02 from floorplan/stage4/measurements.json and floorplan/stage5/dream.json._
