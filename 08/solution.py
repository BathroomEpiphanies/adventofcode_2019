#!/usr/bin/python3

import sys
import json

image = sys.stdin.readline().strip()
xsize,ysize = [ int(x) for x in sys.argv[1:3] ]
lsize = xsize*ysize
lcount = len(image)//lsize

counts = [{n: sum([p==n for p in image[l*(lsize):(l+1)*(lsize)]]) for n in ['0','1','2']} for l in range(0,lcount)]
#print(json.dumps(counts,indent=2))
counts.sort( key=(lambda x: x['0']) )
print( counts[0]['1']*counts[0]['2'] )


flat = ['0' for x in range(lsize)]
for p in range(0,ysize*xsize):
    for l in range(0,lcount):
        if image[l*lsize+p] != '2':
            flat[p] = '#' if image[l*lsize+p] == '1' else ' '
            break
flat = [ flat[r*xsize:(r+1)*xsize] for r in range(0,ysize) ]
for row in flat:
    print( ''.join(row) )


###  #     ##  #  # #### 
#  # #    #  # # #  #    
#  # #    #  # ##   ###  
###  #    #### # #  #    
# #  #    #  # # #  #    
#  # #### #  # #  # #    
