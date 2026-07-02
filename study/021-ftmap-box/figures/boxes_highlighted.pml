set ambient, 0.25
set cartoon_transparency, 0
set field_of_view 20
set cartoon_discrete_colours, on
set antialias, 4

delete all
load F:\\FapC_VS\\study\\021-ftmap-box\\data\\9nqd.fftmap.cleared.pdb
dss

select entire, all

hide sticks
show cartoon
color gray, entire


python
from pymol import cmd
from pymol.cgo import LINEWIDTH, BEGIN, LINES, COLOR, VERTEX, END

def draw_box(name, cx, cy, cz, sx, sy, sz, r=1.0, g=1.0, b=1.0, linewidth=2.0):
    # PyMOL passes command-line arguments as strings, so cast to float
    cx, cy, cz = float(cx), float(cy), float(cz)
    sx, sy, sz = float(sx), float(sy), float(sz)
    r, g, b = float(r), float(g), float(b)
    linewidth = float(linewidth)

    x0, x1 = cx - sx / 2.0, cx + sx / 2.0
    y0, y1 = cy - sy / 2.0, cy + sy / 2.0
    z0, z1 = cz - sz / 2.0, cz + sz / 2.0

    corners = [
        (x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0),
        (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1),
    ]
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 0),
        (4, 5), (5, 6), (6, 7), (7, 4),
        (0, 4), (1, 5), (2, 6), (3, 7),
    ]

    obj = [LINEWIDTH, linewidth, BEGIN, LINES, COLOR, r, g, b]
    for i, j in edges:
        obj.extend([VERTEX, *corners[i]])
        obj.extend([VERTEX, *corners[j]])
    obj.append(END)

    cmd.load_cgo(obj, name)

cmd.extend("draw_box", draw_box)
python end

# ---- region_1: red -------------------------------------------------
draw_box box_region_1, 95, 120, 45, 30, 15, 30, 1.0, 0.2, 0.2

# ---- region_2: green -------------------------------------------------
draw_box box_region_2, 107, 91.5, 42, 30, 15, 30, 0.2, 1.0, 0.2

# ---- region_3: blue -------------------------------------------------
draw_box box_region_3, 95, 110, 25, 30, 30, 15, 0.2, 0.4, 1.0

print "Drew boxes: box_region_1, box_region_2, box_region_3"

set_view (\
     0.236147180,   -0.043538526,   -0.970740795,\
    -0.971699178,   -0.004417891,   -0.236181945,\
     0.005993601,    0.999041975,   -0.043349702,\
     0.000000000,    0.000000000, -245.405136108,\
   100.925071716,  106.901550293,   41.934860229,\
   193.479278564,  297.330993652,  -20.000000000 )
ray
png boxes_highlighted.png

