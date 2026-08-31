import cv2
import turtle
import sys
import argparse

# --- CLI argument for image path (instead of hardcoding the filename) ---
parser = argparse.ArgumentParser(description="Recreate an image as an animated turtle sketch.")
parser.add_argument("image", nargs="?", default="spiderman.png", help="Path to the input image")
args = parser.parse_args()

image = args.image
img = cv2.imread(image)

if img is None:
    print(f"Error: Could not read the image '{image}'.")
    sys.exit(1)

# resize
height = 700
ratio = height / img.shape[0]
width = int(img.shape[1] * ratio)
img = cv2.resize(img, (width, height))
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

_, thresh = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY_INV)

contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# filter out tiny noise contours (small specks, antialiasing artifacts, etc.)
contours = [c for c in contours if cv2.contourArea(c) > 15]

# draw the biggest shapes first (usually the main silhouette of the character)
contours = sorted(contours, key=cv2.contourArea, reverse=True)

screen = turtle.Screen()
screen.bgcolor("white")
screen.setup(width=800, height=575)
screen.tracer(1, 5)  # we control updates manually for animation ctrl

pen = turtle.Turtle()
pen.speed(3)
pen.hideturtle()
pen.pensize(1)

scale = 0.8
UPDATE_EVERY = 3  # update the screen every N points drawn


def map_point(px, py):
    # map the point from image coordinates to turtle coordinates
    tx = (px - width / 2) * scale
    ty = (height / 2 - py) * scale
    return tx, ty


def average_color(contour_mask, image):
    """Sample the average BGR color of the original image inside a contour,
    convert it to a turtle-friendly RGB tuple in the 0-1 range."""
    mean_bgr = cv2.mean(image, mask=contour_mask)[:3]
    b, g, r = mean_bgr
    return (r / 255, g / 255, b / 255)


pointer_counter = 0
for contour in contours:
    points = contour.reshape(-1, 2)

    if len(points) < 2:
        continue

    # --- NEW: build a mask for this contour and sample its average color ---
    mask = cv2.drawContours(
        (0 * gray).copy(), [contour], -1, 255, thickness=cv2.FILLED
    )
    fill_color = average_color(mask, img)
    pen.color(fill_color, fill_color)  # outline + fill use the sampled color

    x0, y0 = map_point(points[0][0], points[0][1])
    pen.penup()
    pen.goto(x0, y0)
    pen.pendown()
    pen.begin_fill()

    for px, py in points[1:]:
        x, y = map_point(px, py)
        pen.goto(x, y)

        pointer_counter += 1
        if pointer_counter % UPDATE_EVERY == 0:
            screen.update()

    pen.goto(x0, y0)  # close the shape
    pen.end_fill()
    screen.update()  # final update for this shape

# --- FIXED: these now actually apply since they run before turtle.done() blocks ---
screen.tracer(0)
pen.speed(0)
screen.update()

turtle.done()  # keep the window open until closed by user
