import math
import time
import turtle

#####################
width = 2
height = 100
mult = 5

draw = False
swap = False
#####################

def ang(x, y):
    ln = math.sqrt(x ** 2 + y ** 2)
    if (ln == 0):
        sin = 0
        cos = 0
    else:
        sin = y / ln
        cos = x / ln
    if x >= 0 and y >= 0:
        return math.asin(sin)
    if x < 0 and y >= 0:
        return math.pi  - math.asin(sin)
    if x < 0 and y < 0:
        return math.pi - math.asin(sin)
    if x >= 0 and y < 0:
        return math.pi * 2 - math.acos(cos)

def get_loop(x1, y1, z1, x2, y2, z2, x3, y3, z3):
    if swap:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
    
    prec = 7
    return "facet normal 0 0 0\nouter loop\nvertex " + str(x1)[:prec] + " " + str(y1)[:prec] + " " + str(z1)[:prec] + "\nvertex " + str(x2)[:prec] + " " + str(y2)[:prec] + " " + str(z2)[:prec] + "\nvertex " + str(x3)[:prec] + " " + str(y3)[:prec] + " " + str(z3)[:prec] +"\nendloop\nendfacet\n\n"

def get_tunnel(x1, y1, x2, y2, x3, y3, x4, y4):
    ans = ""

    ans += get_loop(x1, y1, 0, x2, y2, height, x1, y1, height) + "\n"

    ans += get_loop(x1, y1, height, x2, y2, height, x3, y3, height) + "\n"
    ans += get_loop(x3, y3, height, x2, y2, height, x4, y4, height) + "\n"

    ans += get_loop(x3, y3, height, x4, y4, height, x3, y3, 0) + "\n"
    ans += get_loop(x3, y3, 0, x4, y4, height, x4, y4, 0) + "\n"

    ans += get_loop(x3, y3, 0, x4, y4, 0, x1, y1, 0) + "\n"
    ans += get_loop(x1, y1, 0, x4, y4, 0, x2, y2, 0) + "\n"

    ans += get_loop(x1, y1, 0, x2, y2, 0, x2, y2, height) + "\n"

    return ans

svg = open('svg.svg', 'r')
stl = open('stl.stl', 'w')

svg.read(8)
s = svg.read()
s = s.rstrip(')')

s = s.replace(',', '')

x = list(map(float, s.split()[::2]))
y = list(map(float, s.split()[1::2]))

x1 = []
y1 = []

stl.write("solid svg\n")

le = len(x)

xs = 270 * mult
ys = -450 * mult

for i in range(le):
    a1 = ang(x[(i - 1 + le) % le] - x[i], y[(i - 1 + le) % le] - y[i])
    a2 = ang(x[(i + 1 + le) % le] - x[i], y[(i + 1 + le) % le] - y[i])
    a = a1 + a2

    l = width / math.sin((a2 - a1) / 2)

    xa = l * math.cos(a / 2)
    ya = l * math.sin(a / 2)

    xa = x[i] - xa
    ya = y[i] - ya
    
    if draw:
        turtle.goto(xa * mult + xs, ya * mult + ys)
    x1.append(xa)
    y1.append(ya)

for i in range(le):
    xa = x[i]
    ya = y[i]

    if draw:
        turtle.goto(xa * mult + xs, ya * mult + ys)

minx = 0
miny = 0
#minx = min(x[0], x1[0], minx)
#miny = min(y[0], y1[0], miny)


for i in range(le - 1):
    minx = min(minx, x[i], x1[i])
    miny = min(miny, y[i], y1[i])

minx = -minx
miny = -miny

print(minx)
print(miny)

for i in range(le - 1):
    stl.write(get_tunnel(x[i] + minx, y[i] + miny, x[i + 1] + minx, y[i + 1] + miny, x1[i] + minx, y1[i] + miny, x1[i + 1] + minx, y1[i + 1] + miny))

stl.write(get_tunnel(x[le - 1] + minx, y[le - 1] + miny, x[0] + minx, y[0] + miny, x1[le - 1] + minx, y1[le - 1] + miny, x1[0] + minx, y1[0] + miny))

stl.write("endsolid svg")
if draw:
    turtle.exitonclick()