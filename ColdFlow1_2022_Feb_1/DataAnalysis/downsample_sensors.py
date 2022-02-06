# This script downsamples sensor suite data from 20kHz to 10Hz and 
# adds estimated timestamps based on average count and sample rate

import matplotlib.pyplot as plt

IN_FILE = './../data/attempt1/post_data-1643440871.4287357.txt'
OUT_FILE = './../data/attempt1/avg_data.csv'

SAMPLE_RATE = 20000
TARGET_RATE = 10
TARGET_SAMPLES = SAMPLE_RATE // TARGET_RATE

print('reading file')
with open(IN_FILE) as f:
    next(f)
    raw_data = [[float(x) for x in line.split(', ')] for line in f]

# 0  1  2  3  4  5
# C0 C1 C2 C3 DO AVG

print('summing')
sum_data = [[0]*6]
for line in raw_data:
    sum_data[-1] = [(s + l*line[5]) for s,l in zip(sum_data[-1][0:5], line[0:5])] + [sum_data[-1][5] + line[5]]
    if sum_data[-1][5] >= TARGET_SAMPLES:
        sum_data.append([0]*6)

print('averaging')
avg_data = [[0]*6]
for line in sum_data:
    avg_data.append([x/line[5] for x in line[0:5]] + [(line[5] + avg_data[-1][5])])
    avg_data[-2][5] /= SAMPLE_RATE
avg_data[-1][5] /= SAMPLE_RATE
avg_data = avg_data[2:]

print('writing output')
with open(OUT_FILE, 'w') as f:
    for line in avg_data:
        f.write(', '.join([str(d) for d in line]) + '\n')

x = [d[5] for d in avg_data]
plt.plot(x, [d[0] for d in avg_data], label='pinhole')
plt.plot(x, [d[1] for d in avg_data], label='mainfeed')
plt.plot(x, [d[2] for d in avg_data], label='loadcell')
#plt.plot(x, [d[3] for d in avg_data], label='unused')
#plt.plot(x, [d[4] for d in avg_data], label='unused')
plt.xlabel('time (s)')
plt.ylabel('value (kg, psi)')
plt.legend()
plt.show()
