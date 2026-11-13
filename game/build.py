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
def data_uri(path):
    return "data:image/png;base64," + base64.b64encode(open(path, "rb").read()).decode()

# Castle bakery room from PixelLab's room generator: empty floor + cut-out furniture pieces.
ROOM_DIR = os.path.join(HERE, "rooms", "castle_bakery")
pieces = []
for i, p in enumerate(json.load(open(os.path.join(ROOM_DIR, "pieces.json")))):
    img = next(f for f in os.listdir(os.path.join(ROOM_DIR, "pieces")) if f.startswith(f"{i}_") and "shadow" not in f)
    entry = {"name": p["name"], "x": p["x"], "y": p["y"], "foot": p["foot"], "img": data_uri(os.path.join(ROOM_DIR, "pieces", img))}
    if p.get("shadow"):
        entry["shadow"] = {"x": p["shadow"]["x"], "y": p["shadow"]["y"], "img": data_uri(os.path.join(ROOM_DIR, p["shadow"]["file"]))}
    pieces.append(entry)
room = {"floor": data_uri(os.path.join(ROOM_DIR, "lit.png")), "pieces": pieces}

out = src.replace("__ATLAS__", uri).replace("__FOOT_Y__", str(foot_y)).replace("__ROOM__", json.dumps(room))
open(os.path.join(HERE, "bakehouse.html"), "w", encoding="utf-8").write(out)
print("foot_y", foot_y, "atlas bytes", len(buf.getvalue()))

# Lighthouse village prototype: base plate + the same baker atlas.
vsrc = open(os.path.join(HERE, "village.src.html"), encoding="utf-8").read()
vout = (vsrc.replace("__ATLAS__", uri).replace("__FOOT_Y__", str(foot_y))
        .replace("__PLATE__", data_uri(os.path.join(HERE, "maps", "lighthouse_village", "section_01.png"))))
open(os.path.join(HERE, "village.html"), "w", encoding="utf-8").write(vout)
print("village.html written")

# Tavern interior prototype.
tsrc = open(os.path.join(HERE, "tavern.src.html"), encoding="utf-8").read()
tout = (tsrc.replace("__ATLAS__", uri).replace("__FOOT_Y__", str(foot_y))
        .replace("__PLATE__", data_uri(os.path.join(HERE, "maps", "tavern", "tavern_688x384.png"))))
open(os.path.join(HERE, "tavern.html"), "w", encoding="utf-8").write(tout)
print("tavern.html written")

# Combined world: village + tavern with doors between them.
wsrc = open(os.path.join(HERE, "world.src.html"), encoding="utf-8").read()
wout = (wsrc.replace("__ATLAS__", uri).replace("__FOOT_Y__", str(foot_y))
        .replace("__VILLAGE__", data_uri(os.path.join(HERE, "maps", "lighthouse_village", "section_01.png")))
        .replace("__TAVERN__", data_uri(os.path.join(HERE, "maps", "tavern", "tavern_full_560x448.png"))))
open(os.path.join(HERE, "world.html"), "w", encoding="utf-8").write(wout)
print("world.html written")
