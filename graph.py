import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.signal import savgol_filter
from scipy.signal import find_peaks
from matplotlib.ticker import FormatStrFormatter


# Desired lines in file
start = 42876 - 1
end = 43476 - 1
diff = end - start

# Timestamps
timeOffset = 924.3
touchDown = 6.8

# Open file
with open("labels.csv") as file:
    line = file.readline()
    labels = line.split(',')

# Parse file as a pandas object. Only take the desired lines (start and end)
df_csv = pd.read_csv('./data/fixedData.txt', names=labels, index_col=False, header=None)[start:end]

# Ajust the time stamp in second. Have 0 at the launch
df_csv["timeStamp"] = df_csv["timeStamp"]/1000000000 - timeOffset


# Calculate resulting acceleration
accX = df_csv["filteredXaccelerometer"].values
accY = df_csv["filteredYaccelerometer"].values
accZ = df_csv["filteredZaccelerometer"].values

acc = ((accX**2) + (accY**2) + (accZ**2))**(0.5)


# filter altitude
filtered_altitude = savgol_filter(df_csv["relativeBarometricAltitude"], 25, 3) 

# filter velocity
filtered_velocity = savgol_filter(df_csv["velocityD"], 25, 3)

# filter acceleration
filtered_acc = savgol_filter(acc, 25, 3)

# get peak for apogee
apogee_idx, _ = find_peaks(filtered_altitude, prominence=2, height=40)
print("Apogee: " + str(df_csv["relativeBarometricAltitude"].iloc[apogee_idx[0]]))


# get peak for velocity
max_velocity_index, _ = find_peaks(-filtered_velocity, prominence=2, height=15)
print("Max speed: " + str(df_csv["velocityD"].iloc[max_velocity_index[0]]))

# plot values
plt.plot(df_csv["timeStamp"], df_csv["velocityD"]*-1, label="Velocity (m/s)")
plt.plot(df_csv["timeStamp"], acc, label="Acceleration (m/s^2)")
plt.plot(df_csv["timeStamp"], df_csv["relativeBarometricAltitude"], label="Altitude (m)")
# plt.plot(df_csv["timeStamp"], df_csv["pitch"], label="Altitude (m)")

# plot lines
plt.axvline(x=df_csv["timeStamp"].iloc[apogee_idx[0]], label="Apogee", c="r", linestyle=":", linewidth=1)
plt.axvline(x=0, label="Liftoff", c="turquoise", linestyle=":", linewidth=1)
plt.axvline(x=touchDown, label="Touchdown", c="violet", linestyle=":", linewidth=1)


# Set x axis with t-1 t-0 t+1 t+2 notation
plt.gca().xaxis.set_major_formatter(lambda time, _ : (("t") if time < 0 else (("t-") if (time == 0) else ("t+"))) + f"{round(time, 5)}")

# if we want to rotate the x axis
# plt.xticks(rotation=-0)

# Config matplotlib
plt.tight_layout()
# show the graph
plt.legend()
plt.show()