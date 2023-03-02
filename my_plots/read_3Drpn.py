import numpy as np
import rpnpy.librmn.all as rmn
import rpnpy.vgd.all as vgd
import matplotlib.pyplot as plt
#---------- NOTES ------------

def masking(x,y,miss):
    x[x < 0.0001] = miss
    x = np.ma.masked_equal(x,-999)
    return x

#-- To convert from hybrid level to IP1 (e.g.):
hyb_lev = 0.997497022152
ip1 = rmn.ip1_val(hyb_lev, rmn.LEVEL_KIND_HYB)
print(hyb_lev,ip1)

#-- convert ip1 to hybrid level (hyb_lev), lkind (e.g.):
ip1 = 95336683
(hyb_lev, lkind) = rmn.convertIp(rmn.CONVIP_DECODE, ip1)
print(hyb_lev,ip1)

#-----------------------------


fileIn = '/home/zde001/data/ppp5/output_demo_gridpt_data/model/2022120812_001'

# Open file
fileId = rmn.fstopenall(fileIn, rmn.FST_RO)

#---- Get the vgrid definition (!!) present in the file
v = vgd.vgd_read(fileId)

#---- Get the list of ip1 number on thermo levels in this file
tlvl = vgd.vgd_get(v, 'VIPT')

#---- Get the list of ip1 on dyn levels in this file
mlvl = vgd.vgd_get(v, 'VIPM')


#------------------
# Trim the list of thermo ip1 to actual levels in files for VAR,
# since the vgrid in the file is a super set of all levels, and get their "key"

VAR = 'SHR2'
tlvlkeys = []  # elements of tlvl for which VAR is present in file
rshape = None

for ip1 in tlvl:
    key = rmn.fstinf(fileId, nomvar=VAR, ip1=ip1)
    print('A: ',ip1,key)
    if key is not None:
        tlvlkeys.append((ip1, key['key']))
        if rshape is None:
           rshape = key['shape']
rshape = (rshape[0], rshape[1], len(tlvlkeys))


#------------------
# Read every level for VAR at ip2=(?), re-use 2d array while reading and
# store the data in a 3d array with lower level at nk, top at 0 as in the model
# Note that for efficiency reasons, if only a profile was needed,
# only that profile would be saved instead of the whole 3d field


r2d = {'d' : None}
r3d = None
k   = 0

for ip1, key in tlvlkeys:
    print('B: ',ip1,key)
    r2d = rmn.fstluk(key, dataArray=r2d['d'])
    if r3d is None:
        r3d = r2d.copy()
        r3d['d'] = np.empty(rshape, dtype=r2d['d'].dtype, order='F')
    r3d['d'][:,:,k] = r2d['d'][:,:]
    k = k + 1

# Add the vgrid and the actual ip1 list in the r3d dict, update shape and nk
r3d['vgd']     = v
r3d['ip1list'] = [x[0] for x in tlvlkeys]
r3d['shape']   = rshape
r3d['nk']      = rshape[2]

var3d = r3d['d'][:,:,:]  # store value of 3D field (VAR) in 'var3d'
var3d_ma = masking(var3d,var3d,-999)

rmn.fstcloseall(fileId)

result, edges = np.histogram(var3d_ma[~var3d_ma.mask],normed=True,bins=200)
binw = edges[1] - edges[0]
plt.bar(edges[:-1], result*binw,binw)
plt.show()
