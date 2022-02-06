# Spray Pattern Analysis

## Problem

I noticed some irregular flow patterns of the CO2 in the video. I wanted to know if the oscillation was at a specific frequency or not (because it might be caused by instability in the piping).


## Solution

I took the video at 30fps, I took a region of image where the variation was apparent and the variation over time of those pixels. 

![image](https://user-images.githubusercontent.com/50854503/152700501-0683c10a-378f-4bbb-870e-501ad2feffc3.png)

It looks like we can clearly see the variation of brightness over time. 

![image](https://user-images.githubusercontent.com/50854503/152700510-29f899d1-16a3-41db-b5e5-145af1f76472.png)

Then, I did a Fourrier analysis on this data in the time domaine to see if there was any apparent resonant frequency in the frequency domain.

![image](https://user-images.githubusercontent.com/50854503/152700695-8d0baa4f-acf1-4a20-8ff7-f4a63167fae6.png)

We can see that we found that the flow rate doesn't oscillate at a specific frequency.

I Also repeated the process with multiple different regions of images and reached the same conclusion (near injector plate, smaller regions, bigger regions, ...).  



## Conclusionn
We can't rule out instability of pipe flow. We also don't have any evidence of this phenomena happening so far. The variations we see there are likely caused by other factors (random noise, wind or flow catching on burrs in the feed or injector plates).
