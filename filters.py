from scipy.signal import savgol_filter

with open("./data/result.txt", "rb") as file:
    lines = file.readlines()
    for line in lines:
        # try:
        print(line.decode().split(",")[24])
        # except:
            # pass
