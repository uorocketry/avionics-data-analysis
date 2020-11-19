from scipy.signal import savgol_filter

with open("./data/result.txt") as file:
    lines = file.readlines()
    for line in lines:
        if b'\x0a' in line:
            print(line)
