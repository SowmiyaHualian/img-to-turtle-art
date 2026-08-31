import cv2
import turtle 

image = "spiderman.png"
img = cv2.imread(image)

if img is None:
    print("Error: Could not read the image.")
    exit()

# resize
height = 700
ratio = height / img.shape[0]
width = int(img.shape[1] * ratio)
img = cv2.resize(img, (width, height))
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

_, thresh = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY_INV)

contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#filter out tiny noise countours (small specks, antialising artifacts, etc.)
contours = [c for c in contours if cv2.contourArea(c) > 15]

#draw the biggest shapes first(usually the main silhouette of the character)
contours = sorted(contours, key=cv2.contourArea, reverse=True)

screen = turtle.Screen()
screen.bgcolor("white")
screen.setup(width = 800, height = 575)
screen.tracer(1,5) #we control updates manually for animation ctrl

pen = turtle.Turtle()
pen.speed(3)
pen.hideturtle()
pen.color("black")
pen.pensize(1)

scale = 0.8

UPDATE_EVERY = 3 #update the screen every N points drawn

def map_point(px, py):
    #map the point from image coordinates to turtle coordinates
    tx = (px - width/2) * scale
    ty = (height / 2 - py) * scale
    return tx, ty

pointer_counter = 0
for counter in contours:
    points = counter.reshape(-1, 2)

    if len(points) < 2:
        continue

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

    pen.goto(x0, y0) #close the shape
    pen.end_fill()  
    screen.update() #final update for this shape

screen.tracer(0) #turn off animation control
pen.speed(0) #fastest speed for final touches
turtle.done() #keep the window open until closed by user
