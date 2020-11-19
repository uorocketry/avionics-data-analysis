
with open("./data/fixedData.txt", "w") as writeFile:
    with open("./data/result.txt", "r") as file:
        lines = file.readlines()
        i = 0

        while i < len(lines):
            line = lines[i]
            lineWrite = ""
            if(len(line.split(",")) < 43):
                lineWrite += line[:-1]
                lineWrite += lines[i+1]
                i += 1
                print("correct")
            else:
                lineWrite += line
            
            writeFile.write(lineWrite)
            
            i+=1
            
