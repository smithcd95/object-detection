# The Old Bakehouse

A pixel-art castle bakery where the Old Baker (Halvard) walks between the oven, flour sacks,
worktable, bread rack, water bucket, barrels and the two doorways.

- The room comes from PixelLab's room generator (top-down, 256x256, 32px cells) with its furniture
  cut out as separate pieces (`rooms/castle_bakery/`: `lit.png` is the empty floor, `pieces/` the furniture
  and shadows, `pieces.json` their positions and foot lines). `room.png` is the room as originally painted.
- Plain HTML5 canvas, no libraries, scaled up by whole pixels so the art stays crisp.
- A* pathfinding on an 8px grid; furniture is depth-sorted against the baker's feet so he walks behind it.
- Click/tap the floor to walk him there; WASD / arrow keys steer him directly; "Wandering" toggles his routine.

## Build
`bakehouse.src.html` is the source. `build.py` packs the frames from `../sprites/old_baker` into one atlas
and inlines it, writing the self-contained `bakehouse.html` (open it directly in a browser).

    python3 game/build.py

# Lighthouse Cliffs (village prototype)

`village.html` (built from `village.src.html` by the same `build.py`) puts the baker on the first full-detail
village section, `maps/lighthouse_village/section_01.png` (512x512, made with PixelLab from a crop of the
original painting with the baker sprite as the style image).

- Full-screen canvas; the camera shows about 300 world pixels on the shorter screen side (capped at the map size) and follows the baker.
- Walkable areas are hand-traced polygons (toggle "Show walkable paths"); A* on a 4px grid.
- Atmosphere (all code, no generations): flickering glow on every lamp and window, rising embers,
  glints moving on the sea, two layers of drifting mist, floating dust motes and an edge vignette.

# Tavern (interior prototype)

`tavern.html` (built from `tavern.src.html`) uses `maps/tavern/tavern_688x384.png`. Same controls and camera as the
village; the baker is drawn at 145% here (`SCALE`) so he reads at the right size next to the stools and tables.
Atmosphere: fireplace glow and flicker, rising embers, warm dust motes, edge vignette.

# World (village + tavern, connected)

`world.html` (built from `world.src.html`) is the playable game: one engine with a config per scene
(`SCENES.village`, `SCENES.tavern`) holding the base plate, walkable polygons, blocks, camera framing,
baker scale, lights, effects and exits.

- Doors: stop at the top of the stairs beside the lighthouse and a prompt offers "Enter the tavern?";
  in the tavern, the passage in the bottom-right corner offers "Head back out to the cliffs?".
  Choosing to go fades to black and loads the other scene at the matching spot. "Stay" (or walking off)
  dismisses it until he steps out of the zone; tapping the door zone again re-offers it.
- Paths shows walkable areas (green), blocks (red) and door zones (gold). Pace toggles calm/brisk.
- `window.__game.state()` exposes a read-only snapshot for automated checks.
- Characters: `SCENES.*.npcs` places other characters (atlas built by `build_atlas` in `build.py`). The Old Mechanic
  stands behind the tavern bar as the barkeep, breathes at the current pace and turns to face the baker when he is near.
  `fronts` are cut-out layers (`maps/tavern/front_bar.png`, the counter) drawn over characters standing behind them.
- Walking speed: calm = 60 world px/s at 100% size (about RuneScape's one tile per 0.6s tick), legs at 7 frames/s;
  brisk = 92 px/s at 10 frames/s. Scaled by the scene's `scale`.
- Talking: clicking a character with a `talk` key walks the baker to its `talkAt` spot and plays the next
  conversation from `TALKS` (lists of [speaker, line]; 'npc' or 'me'). Lines type out and are clicked through
  (click/tap, Space or Enter; Esc closes). Each line shows a RuneScape-style chathead built from the speaker's
  still front pose (`CAST.*.head`): enlarged, bobbing, mouth opening and closing while text types, blinking.
