import math
import time
import turtle

#####################
width = 2
height = 1
mult = 4
#####################

def ang(x, y):
    ln = math.sqrt(x ** 2 + y ** 2)
    #if (ln == 0):
    #    return math.pi
    try:
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
    except:
        input()
        return 0

svg = open('svg.svg', 'r')
svg_out = open('svg_out.svg', 'w')

svg.read(8)
s = svg.read()
s = s.rstrip(')')

s = s.replace(',', '')

x = list(map(float, s.split()[::2]))
y = list(map(float, s.split()[1::2]))

x1 = []
y1 = []

le = len(x)

xs = 343 * mult
ys = -452 * mult

turtle.up()

for i in range(le + 1):
    a1 = ang(x[(i - 1 + le) % le] - x[i % le], y[(i - 1 + le) % le] - y[i % le])
    a2 = ang(x[(i + 1 + le) % le] - x[i % le], y[(i + 1 + le) % le] - y[i % le])
    a = a1 + a2

    l = width / math.sin((a2 - a1) / 2)

    xa = l * math.cos(a / 2)
    ya = l * math.sin(a / 2)

    xa = x[i % le] - xa
    ya = y[i % le] - ya
    
    turtle.goto(xa * mult + xs, ya * mult + ys)
    turtle.down()
    x1.append(xa)
    y1.append(ya)

input()

turtle.up()

for i in range(le + 1):
    xa = x[i % le]
    ya = y[i % le]

    turtle.goto(xa * mult + xs, ya * mult + ys)
    turtle.down()

minx = 0
miny = 0

for i in range(le - 1):
    minx = min(minx, x[i], x1[i])
    miny = min(miny, y[i], y1[i])

minx = -minx
miny = -miny

print(minx)
print(miny)

svg_out.write("polygon(")

for i in range(len(x)):
    svg_out.write(str(x1[i]) + " " + str(y1[i]) + ", ")

svg_out.write(")")

turtle.exitonclick()