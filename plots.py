import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import random
import os
import pandas as pd
import fnmatch


path='/directory/'

coord_lat = [[np.arange(89.75, -90,-0.5)], [np.arange(1,361)]] #it should be inverte because th latitude is in this way according to ISIMIP protocol
coord_lon = [[np.arange(-179.75, 180,0.5)], [np.arange(1,721)]]

nc_files = [file for file in fnmatch.filter(os.listdir(path), '*.nc')]

for fname in nc_files:

    variables=['surftemp', 'bottemp','icetemp', 'icethick', 'latentheatf', 'sensheatf','watertemp']
    for var in variables:
        if var in fname:
            var_plot=var
    
        ds=xr.open_dataset(path+fname)

    if var_plot!='watertemp':
        #plot a random day of the chunk
        random_day=random.choice(range(1,ds.dims['time'],1))
        ds[var_plot].isel(time=random_day).plot()
        plt.savefig('output/'+fname+'_randomday_'+str(random_day)+'.png')
        plt.close()

        #plot average map
        ds_mean=ds[var_plot].mean(dim='time')
        ds_mean.plot()
        plt.savefig('output/'+fname+'_mean.png')
        plt.close()
        #plot watertemp corresponing to the pixels of the local lakes
    if var_plot=='watertemp':
        #local_lakes=pd.read_csv('overlapLocalLakes.csv')
        for index, lake in local_lakes.iterrows():
            lat_pos_values = coord_lat[1][0][np.where(coord_lat[0][0]==lake[1])]
            lon_pos_values = coord_lon[1][0][np.where(coord_lon[0][0]==lake[2])]

            time_plot=range(0,366,1)
            temp_level=ds[var_plot][time_plot,:,lat_pos_values-1,lon_pos_values-1].values.squeeze()
            plt.plot(temp_level)
            plt.savefig('output/'+fname+'_'+lake[0]+'HL'+str(lake[5])+'.png')
            plt.close()
