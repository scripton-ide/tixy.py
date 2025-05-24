"""
tixy.py: a Python demo inspired by https://tixy.land/

Use Scripton's canvas toolkit for visualization:
    - Scripton IDE: https://scripton.dev/
    - Scripton Canvas API: https://docs.scripton.dev/api/visualize/canvas/overview
"""

from scripton.canvas import Canvas
from time import sleep, time
from math import sin, sqrt, atan, atan2, hypot


def tixy(
    # A callable that takes (t, i, x, y) and returns a value between -1 and 1
    # (values outside this range will be clamped)
    func,
    # The number of circles per row/column
    dim=16,
    # The maximum radius of the circles
    max_radius=8,
    # Space between circles (in pixels)
    gap=2,
    # Canvas background color
    canvas_fill='black',
    # Circle background for positive values
    positive_fill='white',
    # Circle background for negative values
    negative_fill='#FE2244',
    # The amount of time (in seconds) to wait between frames
    delay=0.05,
):
    length = dim * (2 * max_radius + gap) - gap
    num_circles = dim * dim
    canvas = Canvas(width=length, height=length)

    # The render function is invoked every frame
    def render(func, t):
        canvas.clear(fill=canvas_fill)
        for i in range(num_circles):
            x = i % dim
            y = i // dim
            radius = max(-1, min(1, func(t, i, x, y))) * max_radius
            canvas.draw_circle(
                x=max_radius * (2 * x + 1) + gap * x,
                y=max_radius * (2 * y + 1) + gap * y,
                radius=abs(radius),
                fill=positive_fill if radius > 0 else negative_fill
            )

    # Start the animation loop
    start_time = time()
    while True:
        with canvas.sync():
            render(func, time() - start_time)
        sleep(delay)


if __name__ == '__main__':
    # Try out some examples or write your own!
    examples = {
        'flip': lambda t, i, x, y: y - t,
        'triangle': lambda t, i, x, y: y - x,
        'pattern': lambda t, i, x, y: i % 4 - y % 4,
        'mondrian': lambda t, i, x, y: (y - 6) * (x - 6),
        'stripes': lambda t, i, x, y: sin(t + (x + y) / 2),
        'ripples': lambda t, i, x, y: sin(t - sqrt((x - 7.5)**2 + (y - 6)**2)),  # by @thespite
        'invader': lambda t, i, x, y: (ord('p}¶¼<¼¶}p'[x]) if x < 9 else 0) & 2**y,  # by @keithclarkcouk + @zozuar
        'rotation': lambda t, i, x, y: sin(2 * atan((y - 7.5) / (x - 7.5)) + 5 * t),
        'spiral': lambda t, i, x, y: sin(t + atan2(y - 7.5, x - 7.5) + hypot(x - 7.5, y - 7.5))
    }
    tixy(examples['spiral'])
