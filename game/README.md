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
