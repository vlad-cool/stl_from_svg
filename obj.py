import math
import time
import turtle

#####################
width = -2
height = 1
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

def get_tunnel(i):
    ans = ""

    ans += "f " + str(i * 4 + 1) + " " + str(i * 4 + 2) + " " + str((i + 1) * 4 + 2) + " " + str((i + 1) * 4 + 1) + "\n"
    ans += "f " + str(i * 4 + 2) + " " + str(i * 4 + 3) + " " + str((i + 1) * 4 + 3) + " " + str((i + 1) * 4 + 2) + "\n"
    ans += "f " + str(i * 4 + 3) + " " + str(i * 4 + 4) + " " + str((i + 1) * 4 + 4) + " " + str((i + 3) * 4 + 2) + "\n"
    ans += "f " + str(i * 4 + 4) + " " + str(i * 4 + 1) + " " + str((i + 1) * 4 + 3) + " " + str((i + 4) * 4 + 2) + "\n"

    return ans

svg = open('svg.svg', 'r')
obj = open('obj.obj', 'w')

svg.read(8)
s = svg.read()
s = s.rstrip(')')

s = s.replace(',', '')

x = list(map(float, s.split()[::2]))
y = list(map(float, s.split()[1::2]))

x1 = []
y1 = []

#obj.write("solid svg\n")

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

for i in range(le):
    obj.write("v " + str(x[i]) + " " + str(y[i]) + str(height) + "\n")
    obj.write("v " + str(x[i]) + " " + str(y[i]) + "0" + "\n")
    obj.write("v " + str(x1[i]) + " " + str(y1[i]) + str(height) + "\n")
    obj.write("v " + str(x1[i]) + " " + str(y1[i]) + "0" + "\n")


for i in range(le):
    obj.write(get_tunnel(i))

#obj.write(get_tunnel(x[le - 1] + minx, y[le - 1] + miny, x[0] + minx, y[0] + miny, x1[le - 1] + minx, y1[le - 1] + miny, x1[0] + minx, y1[0] + miny))

#obj.write("endsolid svg")
if draw:
    turtle.exitonclick()