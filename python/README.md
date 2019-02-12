# How to detect LEDs that are on ?

Ideas:
* Search for the brightest spots (sort, threshold)
* Compare with the previous image (where the LED was off)
* Search for high frequences (high-pass filter)
* Compute a shape's circularity (area over squared perimeter)
* Put a pattern near the LED and search for it (e.g. black paint around)
