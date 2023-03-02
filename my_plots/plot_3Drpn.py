import os
import numpy as np
from read_3Drpn_defs import get_array, svpw, svpi
import matplotlib.pyplot as plt
import fnmatch
from matplotlib.colors import LogNorm

def masking(var,var2,var2_lim,var3,miss):
    x = np.zeros((var.shape[0],var.shape[1],var.shape[2],var.shape[3]))
    x[:] = var
    x[((var2 < var2_lim - 5) | (var2 >= var2_lim) | (var3 > 400))] = miss
    x = np.ma.masked_equal(x,-999)
    print(var2_lim)
    #x = x[~x.mask]
    return x


def histo(var,bi):
    if var[~var.mask].size == 0:
        norm_n = 1
        weight = np.zeros(np.shape(var[~var.mask]))
        weight[:] = 1./norm_n
        var_n, edges = np.histogram(var[~var.mask],bins=bi,weights=weight)
        bincenter = 0.5*(edges[1:]+edges[:-1])
        binsize = 1
    else:
        norm_n = len(var[~var.mask])
        weight = np.zeros(np.shape(var[~var.mask]))
        weight[:] = 1./norm_n
        var_n, edges = np.histogram(var[~var.mask],bins=bi,weights=weight)
        bincenter = 0.5*(edges[1:]+edges[:-1])
        binsize = ((np.max(var[~var.mask]) - np.min(var[~var.mask]))/bi)
    return var_n, bincenter, binsize

def mplot(axis,var,name):
    #xx = axis.bar(var[1],var[0],var[2],alpha=0.3,color='red')
    xx = axis.bar(var[1],var[0],var[2],alpha=0.7,color='red')
    yy = axis.grid()
    axis.set_title(name)
    axis.set_yscale('log')
    axis.set_ylabel('Norm. Probability')
    axis.set_xlabel('RHice (%)')
    axis.set_ylim(10e-6,10e-1)
    return xx, yy


def main():
    
    #--------------------------------------------
    #SWITCHES FOR GENERATING FIGURES
    f_2dhist = False
    f_temp_pres = True
    f_temp_rhi = False

    #---------------------------------------------
    #FILE DIRECTORIES
    dirc = '/home/zde001/data/ppp5/output_demo_gridpt_data/model/'
    #dirc = '/space/hall5/sitestore/eccc/prod/hubs/gridpt/dbase/prog/lam/nat.model/'
    infile = '2023020900_???'
    #infile = '2023020500_00?'
    #var = 'TT'
    var_name = ['HRLI','TT','PX']
    
    #-----------------------------------------------
    #GET VARIABLES FROM FILES
    i=0
    for var in var_name:
        v = []
        b = []
        for filename in sorted(os.listdir(dirc)):
            if fnmatch.fnmatch(filename, infile):
                print(dirc+filename)
                var3d = get_array(dirc+filename,var)
                b.append(var3d)
        v = np.stack(b,axis=0)
        if i == 0:
            w = np.zeros((len(var_name),v.shape[0],v.shape[1],v.shape[2],v.shape[3]))
        w[i,:] = v
        i+=1
    
    rhli = w[0,:,:]*100
    tt = w[1,:]
    pp = w[2,:]

    #------------------------------
    #GENERATE VARIABLES FOR 2D-HIST
    tt_rhli = tt[np.where(rhli > 90)]
    pp_rhli = pp[np.where(rhli > 90)]
    tt_pres = tt[np.where(pp < 400)]
    rhli_pres = rhli[np.where(pp < 400)]

    #----------------------------------------
    #MASK RHI IN SPECIFIC TEMP AND PRES RANGE
    if f_2dhist == True:
        rhli_20 = masking(rhli,tt,-20,pp,-999)
        rhli_25 = masking(rhli,tt,-25,pp,-999)
        rhli_30 = masking(rhli,tt,-30,pp,-999)
        rhli_35 = masking(rhli,tt,-35,pp,-999)
        rhli_40 = masking(rhli,tt,-40,pp,-999)
        rhli_45 = masking(rhli,tt,-45,pp,-999)
        rhli_50 = masking(rhli,tt,-50,pp,-999)
        rhli_55 = masking(rhli,tt,-55,pp,-999)
        rhli_60 = masking(rhli,tt,-60,pp,-999)



    #---------------------------------------------------------
    #IF ONLY RH IS AVAILABLE THEN THESE CONVERSIONS CAN BE USED
    #INCLUDE HR AS ONE OF THE OUTPUT VARIABLES
    #ew = svpw(tt+273.15)
    #ei = svpi(tt+273.15)
    #rhi = rh*ew/ei


    #---------------------------------------------------------
    #GENERATE FIGURES
    hbin=20
    if f_2dhist == True:
        f, ((ax7,ax8,ax9),(ax1,ax2,ax3),(ax4,ax5,ax6)) = plt.subplots(3,3,figsize=(16,12))#,sharex=True,sharey=True)
        f.suptitle('RHi distribution over Temperature for Pressure < 400 mb')
        mplot(ax7,histo(rhli_20,hbin),'-20 >= T (degC) > -25')
        mplot(ax8,histo(rhli_25,hbin),'-25 >= T (degC) > -30')
        mplot(ax9,histo(rhli_30,hbin),'-30 >= T (degC) > -35')
        mplot(ax1,histo(rhli_35,hbin),'-35 >= T (degC) > -40')
        mplot(ax2,histo(rhli_40,hbin),'-40 >= T (degC) > -45')
        mplot(ax3,histo(rhli_45,hbin),'-45 >= T (degC) > -50')
        mplot(ax4,histo(rhli_50,hbin),'-50 >= T (degC) > -55')
        mplot(ax5,histo(rhli_55,hbin),'-55 >= T (degC) > -60')
        mplot(ax6,histo(rhli_60,20),'-60 >= T (degC) > -65')
        plt.grid()
        f.tight_layout()
        f.savefig('RHi_diffTemp.pdf')
        f.savefig('RHi_diffTemp.png')        
        plt.show()
    
    if f_temp_pres == True:
        f, ax = plt.subplots(1,1)
        ac = plt.hist2d(tt_rhli[~np.isnan(tt_rhli)].flatten(),pp_rhli[~np.isnan(tt_rhli)].flatten(),hbin,cmap='YlOrBr',norm=LogNorm(vmin=10**(-5.4),vmax=10**(-2.1)),density=True)
        cbar = plt.colorbar(ac[3])
        cbar.set_label('Density')
        plt.xlabel('Temperature (degC)')
        plt.ylabel('Pressure (mb)')
        plt.title('RHi > 90%')
        plt.grid()
        f.tight_layout()
        f.savefig('Temp_Pressure_constrain_RHi.pdf')
        f.savefig('Temp_Pressure_constrain_RHi.png')
        plt.show()

    if f_temp_rhi == True:
        f, (ax1,ax2) = plt.subplots(1,2,figsize=(12,6),sharey=True)
        ac = ax1.hist2d(tt.flatten(),rhli.flatten(),hbin,cmap='RdYlBu_r',norm=LogNorm(vmin=10**(-5.4),vmax=10**(-2.1)),density=True)
        cbar = plt.colorbar(ac[3], ax=ax1)
        cbar.set_label('Density')
        ax1.set_xlabel('Temperature (degC)')
        ax1.set_ylabel('RHi (%)')
        ax1.set_ylim(0,150)
        ax1.grid()
        ac2 = ax2.hist2d(tt_pres[~np.isnan(tt_pres)].flatten(),rhli_pres[~np.isnan(tt_pres)].flatten(),hbin,cmap='RdYlBu_r',\
                norm=LogNorm(vmin=10**(-5.4),vmax=10**(-2.1)),density=True)
        cbar2 = plt.colorbar(ac2[3], ax=ax2)
        cbar2.set_label('Density')
        ax2.set_title('Pressure < 400 mb')
        ax2.set_xlabel('Temperature (degC)')
        ax2.set_ylabel('RHi (%)')
        ax2.set_ylim(0,150)
        ax2.grid()
        f.tight_layout()
        f.savefig('Temp_RHi_contrain_pressure.pdf')
        f.savefig('Temp_RHi_contrain_pressure.png')
        
        plt.show()
        
if __name__ == '__main__':
    main()

