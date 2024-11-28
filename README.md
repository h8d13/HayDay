# HayDay
HayDayBot

I've create this for two reasons: 

1. The two other packages on GitHub for HayDay are viruses (bad ones at that).
2. It's a game to prays on your patience, so it's fun to automate.

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

3. **Shape matching**

Then we can use cv2 built-in ```cv2.approxPolyDP``` 




