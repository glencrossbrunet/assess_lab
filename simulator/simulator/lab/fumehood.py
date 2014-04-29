class Fumehood:
    kind
    height
    width
    minflowrate
    maxflowrate
    facevelocityoccupied
    facevelocityunoccupied
    maxsash
    maxcfm
    mincfm
    occupied
    bac
    tag
    building
    room
    hoodnumber
    department
    uselevel

    def __init__(self, kind, height, width, minflowrate, maxflowrate, facevelocityoccupied, facevelocityunoccupied, maxsash, maxcfm, mincfm):
	    self.kind = kind
	    self.height = height
	    self.width = width
	    self.minflowrate = minflowrate
	    self.maxflowrate = maxflowrate
	    self.facevelocityoccupied = facevelocityoccupied
	    self.facevelocityunoccupied = facevelocityunoccupied
	    self.maxsash = maxsash
	    self.maxcfm = maxcfm
	    self.mincfm = mincfm

