
import textwrap
import Image, ImageDraw

im = Image.new("RGB", (200, 200))
draw = ImageDraw.Draw(im)

draw.text((0, 0), "blah blah blah")

testmsg = """
The polygon outline consists of straight lines between the given-coordinates,
plus a straight line between the last and the first coordinate.

The coordinate list can be any sequence object containing either 2-tuples [ (x,
y), ... ] or numeric values [ x, y, ... ]. It should contain at least three
coordinates.

thisiswaytoolongofastringhereitwillnotwrap
"""

draw.textwrap((0, 20), testmsg, 200, 1.0)

del draw
im.save("out.png", "PNG")
