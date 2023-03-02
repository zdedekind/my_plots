#import rpnstd
import rpnpy.librmn.all as rmn
import rpnpy.vgd.all as vgd

import numpy as np
import matplotlib as mpl
from pylab import *
import array
from mpl_toolkits.basemap import Basemap, cm
import matplotlib.pyplot as plt
import csv
from matplotlib import colors
import my_fst_defs

#dname   = '/users/dor/armn/gr8/data2/output/hrdps_tests/'
#fname00 = '2011060812_000-hyb'
#fname   = '2016070700_006'

dname = '/home/zde001/data/ppp5/output_demo_gridpt_data/model/'
fname = '2022120812_001'


#fname00 = dname + fname00
fname0x = dname + fname

var= 'ZEC'
#model_level = 0.950274    # correspond to 1051.4m from find_vert_prof_rpn.py script

model_level = 95336683    # obtained from 'rread3D_rpn.py' script

# Open FST file
file1 = rmn.fstopenall(fname0x,rmn.FST_RO)



#-----------------------------------------------------
def get_latlon(file_obj):
    """
    Get 2D lat,lon (LA,LO) records.
    Arguments:
      file_obj (file object)
    Output:
      lat,lon (2D lists of latitude,longitude))
    """
    var = 'TT'
    key  = rmn.fstinf(file_obj, nomvar=var)['key']
    meta = rmn.fstprm(key)
    meta['iunit'] = file_obj
    grid0 = rmn.ezqkdef(meta)
    gridLatLon = rmn.gdll(grid0)
    lat = gridLatLon['lat']
    lon = gridLatLon['lon']
   #lon = np.mod((lon + 180), 360) - 180
    return lat,lon

#-----------------------------------------------------
def get_rec2D(file_obj,var2D):
    """
    Reads a record from a FST file.
    Arguments:
      file_obj
    Output:
      2D array containing record
    """
    var_key = rmn.fstinf(file_obj, nomvar=var2D)
    var_rec = rmn.fstluk(var_key)
    rec2D   = var_rec['d']
    return rec2D


(lat,lon) = get_latlon(file1)

zet = get_rec2D(file1, 'ZEC')
me  = get_rec2D(file1, 'ME')


# zet = np.fmax(zet,-5)  # clip data

# create figure and axes instances
fig = plt.subplots(num=None, figsize=(14,10), dpi=80, facecolor='w', edgecolor='k')
ax1 = plt.subplot(1,1,1)
#ax1.m = Basemap(resolution='l',projection='stere',lat_0=46,lon_0=-95,width=3000000,height=2000000,no_rot=True)
ax1.m = Basemap(resolution='l',projection='stere',lat_0=48,lon_0=-95,width=6000000,height=3000000,no_rot=True)
x, y = ax1.m(lon, lat)
myLineColor = 'grey'
ax1.m.drawcoastlines(color=myLineColor)
ax1.m.drawstates(color=myLineColor, linewidth=0.6)
ax1.m.drawcountries(color=myLineColor)

parallels = np.arange(0.,90,5.)
ax1.m.drawparallels(parallels,labels=[1,0,0,0],fontsize=10, linewidth = 0.25)
meridians = np.arange(180.,360.,5.)
ax1.m.drawmeridians(meridians,labels=[0,0,0,1],fontsize=10, linewidth = 0.25)

# plot terrain:
#lev = np.linspace(0,3000,3000/200+1)
lev = np.linspace(0,3000,16)
#cs = ax1.m.contourf(x, y, me-1., cmap='terrain', levels=lev)
cs = ax1.m.contourf(x, y, me-1., cmap='gray', levels=lev)
#cs = ax1.m.contourf(x, y, me-1., cmap='terrain') #, vmin=0, vmax=3000.)

# plot ZE:
#col =['white',[0.2,0.2,0.2],'midnightblue',[0.1,0.2,0.6],[0.1,0.2,0.1],[0.15,0.25,0.15],[0.15,0.35,0.15],'forestgreen',[0.,0.65,0.],'limegreen','lime','greenyellow','yellow','goldenrod','red','maroon','darkviolet','magenta','white']
#lev=[-100,-25,-10,-5,0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75]
col =[[0.2,0.2,0.2],'midnightblue',[0.1,0.2,0.6],[0.1,0.2,0.1],[0.15,0.25,0.15],[0.15,0.35,0.15],'forestgreen',[0.,0.65,0.],'limegreen','lime','greenyellow','yellow','goldenrod','red','maroon','darkviolet','magenta','white']
lev=[-25,-10,-5,0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75]
cbar = ax1.m.colorbar(cs,location='bottom',pad="10%")

cs = ax1.m.contourf(x, y, zet ,levels=lev,colors=col)
cbar = ax1.m.colorbar(cs,location='right',pad="5%")

plt.title('My test')


# plt.savefig('./fig.png', format='png')

plt.show()

