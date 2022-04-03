# This script downsamples sensor suite data from 20kHz to 10Hz and 
# adds estimated timestamps based on average count and sample rate

import matplotlib.pyplot as plt

IN_FILE = '../ColdFlow2_2022_Mar_29/data/coldflow-sensors-125.txt'
OUT_FILE = '../ColdFlow2_2022_Mar_29/data/coldflow-sensors-125-avg.csv'
OUT_SCALED_FILE = '../ColdFlow2_2022_Mar_29/data/coldflow-sensors-125-scaled.csv'

SAMPLE_RATE = 20000
TARGET_RATE = 10
TARGET_SAMPLES = SAMPLE_RATE // TARGET_RATE

def read_raw():
    print('reading file')
    with open(IN_FILE) as f:
        next(f)
        raw_data = [[float(x) for x in line.strip('[]\n').split(', ')] for line in f]

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

    

    # Write full (non-scaled) output
    print('writing output')
    with open(OUT_FILE, 'w') as f:
        for line in avg_data:
            f.write(', '.join([str(d) for d in line]) + '\n')

    return avg_data

def scale_data(avg_data):
    print('scaling')
    scaled_data = []
    for line in avg_data:
        time = line[5]
        pres_pinhole = line[0]*620.07 - 330.083
        pres_mainfeed = line[1]*625 - 313
        mass_loadcell = line[2]*6.235 + 0.0624
        scaled_data.append([time, pres_pinhole, pres_mainfeed, mass_loadcell])

    print('writing scaled output')
    with open(OUT_SCALED_FILE, 'w') as f:
        for line in scaled_data:
            f.write(', '.join([str(d) for d in line]) + '\n')
    
    return scaled_data

def read_avg():
    with open(OUT_FILE) as f:
        return [[float(x) for x in line.split(', ')] for line in f]

if __name__ == '__main__':
    avg_data = read_raw()
    #avg_data = read_avg()
    scaled_data = scale_data(avg_data)

    x = [d[0] for d in scaled_data]
    plt.plot(x, [d[1] for d in scaled_data], label='pinhole')
    plt.plot(x, [d[2] for d in scaled_data], label='mainfeed')
    plt.plot(x, [d[3] for d in scaled_data], label='loadcell')
    plt.xlabel('time (s)')
    plt.ylabel('value (psi, kg)')
    plt.legend()
    plt.show()
