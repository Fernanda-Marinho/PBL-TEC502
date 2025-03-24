import random 

# for i in range(10):
#     print(random.randint(1,100))


def range_distance(start, stop, step):
    while start < stop:
        yield round(start, 10)  
        start += step

def set_distance():
    list_distance = []
    for i in range_distance(1,500,0.3):
        list_distance.append(i)
    return random.choice(list_distance)

for i in range(10):
    print(set_distance())    
