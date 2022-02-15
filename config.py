from pathlib import Path


base_folder = Path(__file__).parent.resolve()
runTime = 5 # 3 hours in seconds


#SENSE HAT
g = [0,128,0]
o = [0,0,0]
image = [
    g,g,g,g,g,g,g,g,
    o,g,o,o,o,o,g,o,
    o,o,g,o,o,g,o,o,
    o,o,o,g,g,o,o,o,
    o,o,o,g,g,o,o,o,
    o,o,g,g,g,g,o,o,
    o,g,g,g,g,g,g,o,
    g,g,g,g,g,g,g,g,
]
#EN OF SENSEHAT CONFIG