import turtle
import math
import colorsys

# Canvas setup
screen = turtle.Screen()
screen.setup(width=750, height=750)
screen.bgcolor("#080511")  # Deep cosmic background
screen.title("Mathematical Fourier & Modular Caustic Heart")
screen.tracer(0)

t = turtle.Turtle()
t.hideturtle()
t.speed(0)

# Precompute sample points along a parametric 4-harmonic heart
TOTAL_POINTS = 360
heart_points = []

for i in range(TOTAL_POINTS):
    theta = 2 * math.pi * i / TOTAL_POINTS
    # Parametric Fourier decomposition of a heart
    x = 16 * (math.sin(theta) ** 3)
    y = (
        13 * math.cos(theta)
        - 5 * math.cos(2 * theta)
        - 2 * math.cos(3 * theta)
        - math.cos(4 * theta)
    )
    scale = 18
    heart_points.append((x * scale, (y * scale) + 40))

# Animation State
chord_index = 0
MULTIPLIER = 2.0  # Modular multiplier factor (creates cardioid caustic envelope)

def render_frame():
    global chord_index
    t.clear()

    # 1. Draw glowing background outer halo using harmonic scaling
    t.pensize(1)
    for layer in range(1, 4):
        glow_scale = 1.0 + (layer * 0.035)
        alpha_hue = (chord_index * 0.002) % 1.0
        r, g, b = colorsys.hsv_to_rgb(alpha_hue, 0.8, 0.25 / layer)
        t.pencolor(r, g, b)
        
        t.penup()
        t.goto(heart_points[0][0] * glow_scale, heart_points[0][1] * glow_scale)
        t.pendown()
        for pt in heart_points[1:] + [heart_points[0]]:
            t.goto(pt[0] * glow_scale, pt[1] * glow_scale)

    # 2. Draw the Modular String Caustics (i -> (i * MULTIPLIER) % N)
    # Renders in timed progressive sweeps
    t.pensize(1)
    lines_to_draw = min(chord_index, TOTAL_POINTS)
    for i in range(lines_to_draw):
        target = int((i * MULTIPLIER)) % TOTAL_POINTS
        
        p1 = heart_points[i]
        p2 = heart_points[target]

        # Color changes as a function of chord geometry and iteration
        chord_len = math.hypot(p2[0] - p1[0], p2[1] - p1[1])
        hue = (i / TOTAL_POINTS + chord_len * 0.0015) % 1.0
        r, g, b = colorsys.hsv_to_rgb(hue, 0.9, 0.85)
        
        t.pencolor(r, g, b)
        t.penup()
        t.goto(p1)
        t.pendown()
        t.goto(p2)

    # 3. Draw Fourier Orbit Epicycle Head (Leading Tracer)
    lead_idx = chord_index % TOTAL_POINTS
    lead_pt = heart_points[lead_idx]

    # Draw epicyclic vector indicators
    t.pensize(1.5)
    t.pencolor(1, 1, 1)
    t.penup()
    t.goto(lead_pt)
    t.dot(7, (1, 0.9, 0.9))

    # Outer perimeter boundary glow
    t.pensize(2.5)
    t.penup()
    t.goto(heart_points[0])
    t.pendown()
    for i in range(1, lead_idx + 1):
        hue = (i / TOTAL_POINTS + 0.5) % 1.0
        r, g, b = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
        t.pencolor(r, g, b)
        t.goto(heart_points[i])

    screen.update()
    chord_index += 2

    # Stop once the internal envelope is fully woven
    if chord_index <= TOTAL_POINTS + 120:
        screen.ontimer(render_frame, 16)  # ~60 FPS update tick

# Begin timed render
render_frame()
screen.exitonclick()