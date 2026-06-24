file_reset = open('reset.out','w')
file_switch = open('switch.out','w')

reset = 0
switch = [0,0,0,0]

for ptr in range(100000):
    reset = 1
    
    if (ptr == 100):
        reset = 0
        switch = [1,0,0,0]
        
    if (ptr == 20000):
        reset = 0
        switch = [1,1,0,0]
        
    if (ptr == 30000):
        reset = 0
        switch = [1,0,1,0]
        
    if (ptr == 40000):
        reset = 0
        switch = [1,1,1,0]
        
    if (ptr == 50000):
        reset = 0
        switch = [1,1,1,1]
        
    if (ptr == 60000):
        switch = [0,1,1,1]

    if (ptr == 70000):
        reset = 0
        switch = [0,1,1,1]

    file_reset.write('%d\n'%reset)
    file_switch.write('%d\t%d\t%d\t%d\n'%(switch[0],switch[1],switch[2],switch[3]))

file_reset.close()
file_switch.close()
