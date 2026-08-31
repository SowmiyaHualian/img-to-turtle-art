# Image to Turtle Drawing

Converts an image into line art and redraws it live using Python's `turtle` graphics module — the turtle traces the contours of the image as if sketching it by hand.

## How It Works

1. **Load & resize** — Reads the image with OpenCV and resizes it to a fixed height (700px), preserving aspect ratio.
2. **Grayscale + threshold** — Converts to grayscale, then applies binary inverse thresholding to separate the subject from the background.
3. **Contour detection** — Uses `cv2.findContours` to extract the outlines of shapes in the thresholded image.
4. **Noise filtering** — Drops tiny contours (area < 15px²) caused by antialiasing artifacts or specks.
5. **Sort by size** — Largest contours (usually the main silhouette) are drawn first.
6. **Coordinate mapping** — Image pixel coordinates are mapped to turtle screen coordinates (centered, scaled).
7. **Draw & fill** — Each contour is traced and filled with `pen.begin_fill()` / `pen.end_fill()`, with periodic `screen.update()` calls for a live animated drawing effect.

## Requirements

```bash
pip install opencv-python
```

`turtle` ships with Python's standard library (requires Tk support — usually preinstalled, but on some Linux distros you may need `sudo apt-get install python3-tk`).

## Usage

1. Place your image in the same directory as the script.
2. Update the `image` variable with your filename:
   ```python
   image = "spiderman.png"
   ```
3. Run the script:
   ```bash
   python turtle_draw.py
   ```
4. A window will open and the turtle will draw the image contour-by-contour. Close the window to exit.

## Configuration

| Variable | Description | Default |
|---|---|---|
| `height` | Target image height in pixels (width scales proportionally) | `700` |
| `scale` | Scale factor applied to turtle coordinates | `0.8` |
| `UPDATE_EVERY` | Draw N points before refreshing the screen (lower = smoother but slower) | `3` |
| Threshold value (`180`) | Grayscale cutoff for binary inversion — lower to capture more detail, raise to simplify | `180` |
| `pen.speed(3)` | Turtle drawing speed (0 = fastest, 1–10 = slow to fast) | `3` |

## Tips

- **Best results**: High-contrast images with a clear subject against a plain background (e.g., logos, silhouettes, line art).
- **Too much noise?** Increase the `cv2.contourArea(c) > 15` threshold to filter out more small contours.
- **Missing details?** Lower the threshold value (`180`) to pick up finer/lighter lines.
- **Faster drawing?** Increase `UPDATE_EVERY` or set `pen.speed(0)`.
- **Window size**: Adjust `screen.setup(width=800, height=575)` to fit your image/display.

## Known Limitations

- Only external contours are detected (`cv2.RETR_EXTERNAL`), so internal details/holes within shapes won't be drawn.
- Complex or highly detailed images can result in long draw times.
- `screen.tracer(0)` and `pen.speed(0)` at the end of the script run *after* `turtle.done()` is effectively reached in the loop, so they have no visible effect — these lines can be removed or moved earlier if you want to fast-forward the finishing touches.
