# -*- coding: utf-8 -*-
from import_library import *

path = 'data/'
save_path = 'results/'
date = input('date (sample 16-2 ) \n')


def convert_object_2_int(input):
    '''    
    Convert objects value to float ones , using in DataFrame transformation
    ----------
    Attributes:
    input: input data
    ----------
    Example:
    data['OCB_pct'] = data['OCB_pct'].apply(convert_object_2_int)
    '''    
    return int(str(input).replace(',',''))

def data_wrangling(path,file,date,save=False):
    '''    
    Get data from excel file and sum of the same date_time
    ----------
    Attributes:
    path: input data path
    file: file name
    date: 
    save: bool, default:False
    ----------
    Example:
    data['OCB_pct'] = data['OCB_pct'].apply(convert_object_2_int)
    '''    
    columns = ['date_time','volume','price','pct']
    data = pd.read_excel(path+file, sheet_name = date,header = None, names=columns)
    data['volume'] = data['volume'].apply(convert_object_2_int)
    data_group=data.groupby('date_time')
    data_list = []
    total_volume = 0
    for idx,row in data_group:
        data_tmp = row
        total_volume = data_tmp['volume'].sum()
        data_list.append([data_tmp['date_time'].unique()[0],total_volume,data_tmp['price'].unique()[0],data_tmp['pct'].unique()[0]])
    new_data = pd.DataFrame(data_list, columns=columns)
    if save:
        title = f'{file[0:-3]}-{date}.csv'
        if not os.path.exists(f'{save_path}/'):
            os.makedirs( f'{save_path}/')  
        new_data.to_csv(f'{save_path}/{title}')  
    return new_data

def abnormal_trading_filtering(data,threshold=1000):
    '''
    Filter abnormal trading 
    ----------
    Attributes:
    data: data
    threshold: trading volume considered as abnormal ones
        default: 1000    
    ----------
    Example:
    Ex: abnormal = abnormal_trading_filtering(data,threshold=1000)
    '''
    condition = data['volume']>threshold
    abnormal = data[condition]
    return abnormal 

def price_trading_chart(data,abnormal,file,save=False):
    '''
    Line chart of price trading
    ----------
    Attributes:
    data: data
    threshold: trading volume considered as abnormal ones
        default: 1000    
    ----------
    Example:
    price_trading_chart(data,abnormal,save=False)
    '''
    plt.close('all')
    data['date_time'] = pd.to_datetime(data['date_time'],format='%H:%M:%S')
    data['date_time'] = data['date_time'].dt.strftime('%H:%M:%S')
    ax = data['price'].plot(figsize = (25,6), lw =2 , c='black')
    plt.plot(ax=ax)
    plt.grid()
    for i in abnormal.index:
        plt.axvline(x = i, c='r', lw=2, linestyle='dashed')
    if save:
        title = f'trading_price of {file[:-3]}-{date}.jpg'
        if not os.path.exists(f'{save_path}/'):
            os.makedirs( f'{save_path}/')  
        plt.savefig(f'{save_path}/{title}', bbox_inches="tight") 
    
def volume_trading_chart(data,abnormal,file,save=False):
    '''
    Line chart of price trading
    ----------
    Attributes:  
    ----------
    Example:
    Ex: abnormal = abnormal_trading_filtering(data,threshold=1000)
    '''
    plt.close('all')
    ax = data['volume'].plot(figsize = (25,6))
    plt.plot(ax=ax)
    plt.grid()    
    if save:
        title = f'volume_price of {file[:-3]}-{date}.jpg'
        if not os.path.exists(f'{save_path}/'):
            os.makedirs( f'{save_path}/')  
        plt.savefig(f'{save_path}/{title}', bbox_inches="tight") 

def main():
    all_names = os.listdir(path) # list all name in a folder
    for file in all_names:
        data = data_wrangling(path,file,date,save=False)
        abnormal = abnormal_trading_filtering(data,threshold=1000)
        price_trading_chart(data,abnormal,file,save=True)
        volume_trading_chart(data,abnormal,file,save=True)


main()