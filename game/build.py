"""Pack the Old Baker frames into one atlas and inline it into the kitchen page.

Atlas layout (80x80 cells, 8 columns):
  rows 0-7   idle  (4 frames) for each direction
  rows 8-15  walk  (6 frames) for each direction
  row  16    static rotations, one per direction
Direction order: south, south-east, east, north-east, north, north-west, west, south-west
"""
import base64, io, json, os
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SPR = os.path.join(HERE, "..", "sprites", "old_baker")
DIRS = ["south", "south-east", "east", "north-east", "north", "north-west", "west", "south-west"]
C = 80

atlas = Image.new("RGBA", (C * 8, C * 17), (0, 0, 0, 0))
for i, d in enumerate(DIRS):
    for row0, anim in ((0, "idle"), (8, "walk")):
        folder = os.path.join(SPR, "animations", anim, d)
        for j, f in enumerate(sorted(os.listdir(folder))):
            atlas.paste(Image.open(os.path.join(folder, f)).convert("RGBA"), (j * C, (row0 + i) * C))
    atlas.paste(Image.open(os.path.join(SPR, "rotations", d + ".png")).convert("RGBA"), (i * C, 16 * C))

# Feet line: lowest opaque row of the static south pose.
south = Image.open(os.path.join(SPR, "rotations", "south.png")).convert("RGBA")
foot_y = south.getchannel("A").getbbox()[3]

buf = io.BytesIO()
atlas.save(buf, "PNG", optimize=True)
uri = "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()

src = open(os.path.join(HERE, "bakehouse.src.html"), encoding="utf-8").read()
out = src.replace("__ATLAS__", uri).replace("__FOOT_Y__", str(foot_y))
open(os.path.join(HERE, "bakehouse.html"), "w", encoding="utf-8").write(out)
print("foot_y", foot_y, "atlas bytes", len(buf.getvalue()))
