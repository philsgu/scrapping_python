import time

print ("Press ENTER to start timer")
input()
start = time.time()
end = time.time()
print ("Timer started")
end = start

count = 0 

try: 
    while True:
        input()

        stopwatch = round(time.time() - end, 2)
        count += 1
        print (f"The amount time passed in sec: {stopwatch}")
        break   
except:
    print ("CTRL-D Pressed")