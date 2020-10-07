import pytaon as on
from pytaon import Vec2d

CTE = 1600


def force(body, t):
    distance = ball.position - on.middle
    r = distance.length
    fn_r = CTE * ball.mass / r
    return -fn_r * (distance / r)


def update():
    sp.step(on.dt)
    if on.frame_count % 3 == 0:
        points.append(tuple(ball.position))


def draw():
    on.cls(on.COLOR_BLACK)
    sp.draw()
    on.circ(*on.middle, 5, on.COLOR_YELLOW)
    for x, y in points:
        on.pset(x, y, on.COLOR_LIME)


on.init(240, 180, fps=30, caption="Forças")

points = []
sp = on.Space()
ball = sp.add_circle(
    radius=3,
    pos=on.middle + (50, 0),
    vel=(0, -50),
    mass=10,
    color=on.COLOR_RED,
    force_func=force,
)

on.run(update, draw)
