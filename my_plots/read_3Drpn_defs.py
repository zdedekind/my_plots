import numpy as np
import rpnpy.librmn.all as rmn
import rpnpy.vgd.all as vgd



def svpw(t):
#   Murphy and Koop 2005
#    x = np.exp(54.842763 - 6763.22/t - 4.210*np.log(t) + 0.000367*(t) +
#               np.tanh(0.0415*(t - 218.8))*(53.878 - 1331.22/t - 9.44523*np.log(t) + 0.014025*t))
#   Goff-Gratch
    x = 100*np.exp(-6096.9385/t + 16.635794 - 0.02711193*t +(1.673952e-5)*t**2 + 2.433502*np.log(t))
    return x

def svpi(t):
#   Murphy and Koop 2005
#    x = np.exp(9.550426 - 5723.265/t + 3.53068*np.log(t) - 0.00728332*t)
#   Goff-Gratch
    x = 100*np.exp(-6024.5282/t + 24.7219 + 0.010613868*t - (1.3198825e-5)*t**2 - 0.49382577*np.log(t))
    return x


def get_array(fileN,var):
    #---------- NOTES ------------
    
    
    #-- To convert from hybrid level to IP1 (e.g.):
    hyb_lev = 0.997497022152
    ip1 = rmn.ip1_val(hyb_lev, rmn.LEVEL_KIND_HYB)
    #print(hyb_lev,ip1)
        
    #-- convert ip1 to hybrid level (hyb_lev), lkind (e.g.):
    ip1 = 95336683
    (hyb_lev, lkind) = rmn.convertIp(rmn.CONVIP_DECODE, ip1)
    #print(hyb_lev,ip1)
    
    #-----------------------------
    
        
    fileIn = fileN #'/home/zde001/data/ppp5/output_demo_gridpt_data/model/2022120812_001'
    
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
    
    VAR = var
    
    tlvlkeys = []  # elements of tlvl for which VAR is present in file
    rshape = None
    
    for ip1 in tlvl:
        key = rmn.fstinf(fileId, nomvar=VAR, ip1=ip1)
        #print('A: ',ip1,key)
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
        #print('B: ',ip1,key)
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
    ar = var3d
    return ar

    rmn.fstcloseall(fileId)


