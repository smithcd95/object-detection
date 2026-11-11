# The Old Bakehouse

A small pixel-art kitchen scene where the Old Baker (Halvard) walks between the oven,
counter, work table, flour sacks, water barrels, cooling rack, window and door.

- Plain HTML5 canvas, no libraries. The room is drawn in code at 512x368 and scaled up with nearest-neighbour.
- 8-direction A* pathfinding on a 32px tile grid; furniture is depth-sorted against the baker's feet.
- Click/tap the floor to walk him there; WASD / arrow keys steer him directly; "Wandering" toggles his routine.

## Build
`bakehouse.src.html` is the source. `build.py` packs the frames from `../sprites/old_baker` into one atlas
and inlines it, writing the self-contained `bakehouse.html` (open it directly in a browser).

    python3 game/build.py
