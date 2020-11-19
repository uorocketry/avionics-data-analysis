import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.signal import savgol_filter
from scipy.signal import find_peaks

start = 42876 - 1
end = 43476 - 1
diff = end - start

with open("labels.csv") as file:
    line = file.readline()
    labels = line.split(',')

df_csv = pd.read_csv('./data/fixedData.txt', names=labels, index_col=False, header=None)[start:end]

x = np.arange(0, diff, 1)

# filter altitude
filtered_altitude = savgol_filter(df_csv["relativeBarometricAltitude"], 25, 3) 
# get peak
apogee_idx, _ = find_peaks(filtered_altitude, prominence=2, height=40)
print("Apogee: " + str(df_csv["relativeBarometricAltitude"].iloc[apogee_idx[0]]))

# filter if needed
filtered_velocity = savgol_filter(df_csv["velocityD"], 25, 3)
# get peak
max_velocity_index, _ = find_peaks(-filtered_velocity, prominence=2, height=15)
print("Max speed: " + str(df_csv["velocityD"].iloc[max_velocity_index[0]]))

timeStampSec = df_csv["timeStamp"]/1000000000
accX = df_csv["filteredXaccelerometer"].values
accY = df_csv["filteredYaccelerometer"].values
accZ = df_csv["filteredZaccelerometer"].values

acc = ((accX**2) + (accY**2) + (accZ**2))**(0.5)

# filter if needed
filtered_acc = savgol_filter(acc, 25, 3)

plt.plot(timeStampSec, filtered_velocity*-1, label="velocity (m/s)")
plt.plot(timeStampSec, filtered_acc, label="acceleration (m/s^2)")
plt.plot(timeStampSec, filtered_altitude, label="altitude (m)")
plt.axvline(x=timeStampSec.iloc[apogee_idx[0]], label="apogee", c="r")

plt.legend()
plt.show()