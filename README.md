# HayDay
HayDayBot

I've create this for two reasons: 

1. The two other packages on GitHub for HayDay are viruses (bad ones at that).
2. It's a game to prays on your patience, so it's fun to automate.

Finally, I will not provide the full automation script as it's against terms of service. 
I will however, show the full work to get there. 

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

1. Color
   ![alt text](https://github.com/h8d13/HayDay/blob/main/capcapcap.JPG)
2. Thresholding
   

Then shape extraction. And to confirm it all, we can finalize with a template match. 



