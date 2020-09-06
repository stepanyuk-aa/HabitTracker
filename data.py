import pandas as pd

def read(user):
    df = pd.read_csv('data.csv', sep=',')
    tmp = df.loc[df['Name'] == user].to_numpy()[0]
    return {'Name':tmp[0],'Scope':tmp[1],'Mounth_task':tmp[2],'Week_task':tmp[3],'Day_task':tmp[4],'Rememeber':tmp[5]}

def write(user, param, value):
    arr = {'Name':0,'Scope':1,'Mounth_task':2,'Week_task':3,'Day_task':4,'Rememeber':5}
    df = pd.read_csv('data.csv', sep=',')
    tmp = df.loc[df['Name'] == user]
    index = tmp.index[0]
    tmp = tmp.to_numpy()[0]

    tmp[arr[param]] = value
    df.loc[index] = tmp

    df.to_csv('data.csv', sep=',')