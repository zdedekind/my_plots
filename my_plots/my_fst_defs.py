import rpnpy.librmn.all as rmn

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


