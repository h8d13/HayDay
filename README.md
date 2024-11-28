# HayDay Farm
HayDay Bot Python

I've create this for two reasons: 

1. The two other packages on GitHub for HayDay are viruses (bad ones at that).
Please reset your computer if you've ran these programs at all. 

3. It's a game to prays on your patience, so it's fun to automate.

Finally, I will not provide the full automation script as it's against terms of service. 
I will however, show the full work to get there. Also thanks to @claritycoders for inspiration with the fishing bot. 

As per any automation problem we should break down the exercise:

## InfiniFarm

- Automatically detect the soil
- Plant Wheat (most profitable)
- Sell during growth (downtime)
- Harvest
- Repeat
  

# Soil detection

![alt text](https://github.com/h8d13/HayDay/blob/main/soil.JPG)

As we determined above, the most important will be to detect the area the bot can use to grow crops. 

To do this we can do a couple of things:

1. **Color**
   
   ![alt text](https://github.com/h8d13/HayDay/blob/main/capcapcap.JPG)

How to do it: 

```
class SoilDetector
  def __init__(self):
      template_path = os.path.join(os.path.dirname(__file__), 'templates', 'soil.JPG')
      self.template = cv2.imread(template_path)
      self.template_color = np.mean(self.template, axis=(0,1))
      self.color_threshold = 15
  def detect(self, screen):
      diff = np.abs(screen - self.template_color)
      current_mask = (np.mean(diff, axis=2) < self.color_threshold).astype(np.uint8) * 255
````
   
2. **Thresholding/Masking/Countours**

   ![alt text](https://github.com/h8d13/HayDay/blob/main/capcapcapcap.JPG)

```
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
largest = max(contours, key=cv2.contourArea)
epsilon = 0.02 * cv2.arcLength(largest, True)
```


3. **Shape matching**

Then we can use cv2 built-in ```approx = cv2.approxPolyDP(largest, epsilon, True)``` 
This is a complex algorithm but essentially will adapt the rectangle to fit the perspective of the game. 

# Centroid
Having a uneven amount of tiles is essential (see screenshot above, 21 tiles works because the center will be accurate, while 24 tiles will not as the center will be ambiguous) but could be corrected easily by using square closest to viewport. 

But I'm lazy:

```
M = cv2.moments(contour)
if M["m00"] != 0:
    cx = int(M["m10"] / M["m00"])
    cy = int(M["m01"] / M["m00"])
```

M00 represents the total area
M10 represents the sum of all x-coordinates
M01 represents the sum of all y-coordinates

Dividing first order moments by zero order moment gives the average (center) position

# Planting

Well now that we have a reliable middle point you know what time it is... Offsets...
This is horrible code example but hey, if it works...

```
            # Planting phase
            while True:
                if not self.paused:
                    pag.click(cx, cy)
                    while self.paused:  # Wait if paused
                        time.sleep(0.1)
                    time.sleep(3)

                    if not self.paused:
                        wheat_x_offset=-100
                        wheat_y_offset=-150
                        pag.click((cx+(wheat_x_offset)), (cy+(wheat_y_offset))) # Wheat
                        while self.paused:
                            time.sleep(0.1)
                        time.sleep(1)
                        
                        if not self.paused:
                            pag.mouseDown() # START DRAGGING OVER COUNTOURS
                            contour_points = contour.reshape(-1, 2)
                            
                            for point in contour_points:
                                if self.paused:
                                    pag.mouseUp()  # Release mouse if paused
                                    while self.paused:
                                        time.sleep(0.1)
                                    pag.mouseDown()  # Resume mouse down when unpaused
                                    

                                x, y = point
                                pag.moveTo(cx+35,cy-20, duration=1) # Make sure we drag low enough for planting to begin
                                steps = 50
                                for i in range(steps):
                                    if self.paused:
                                        break
                                    ix = cx + (x - cx) * (i/steps)
                                    iy = cy + (y - cy) * (i/steps)
                                    
                                    jiggle_x, jiggle_y = self.add_jiggle(int(ix), int(iy))
                                    pag.moveTo(jiggle_x, jiggle_y, duration=0.1)

                                if not self.paused:
                                    pag.moveTo(int(x), int(y), duration=3)
                                    time.sleep(0.5)

                            pag.moveTo(cx,cy) # RELEASE AT MIDDLE SAFE POINT
                            pag.mouseUp()

```

# Harvesting

Well we just reverse the sequence above and use a slightly different offset for the tool:

```
                print("Time to harvest!")    
                if not self.paused:
                    pag.click(cx, cy)  # Click middle of field again
                    time.sleep(1) # Wait for tool to appear
                    pag.moveTo(cx-110, cy-10, duration= 1) # Move mouse to harvest tool offset
                    # Then same as planting movements...
```

# Jiggle

```
    def add_jiggle(self, x, y, amplitude=45):
        jiggle_x = x + np.random.randint(-amplitude, amplitude)
        jiggle_y = y + np.random.randint(-amplitude, amplitude)*2 #MORE HORIZONTAL MOVEMENTS THAN VERTICAL
        return jiggle_x, jiggle_y
```

This helps get the whole field 98% of the time. 

# Inventory management

```
                print("Starting 2 minute timer until harvest...")
                start_time = time.time()
                elapsed_time = 0
                wheat_harvest = 110 # Seconds - Time to plant
                has_sold = False
                while elapsed_time < wheat_harvest:  # 2 minutes WHEAT --offset 10 secs
                    if not self.paused:
                        elapsed_time = time.time() - start_time
                        
                        if not has_sold and not self.paused:
                            go_sell()
                            sell()
                            close()
                            has_sold=True
                            pag.moveTo(cx, cy)
                    # GO SELL DURING GROW
                    time.sleep(0.1)
```


Then the ```go_sell, sell, close``` are simple automation scripts that use the shop to unload storage. 
The only thign was to make a loop that would replant directly (so we still have wheat, then sell as much as possible, or what's left) 

Here is a preview in x16 speed. 

https://github.com/user-attachments/assets/61e6eb0d-7297-40b4-b07c-09263a126e35

