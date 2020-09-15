import pickle as pk

def init():
    a = {'Андрей': {'Name':'Андрей','Scope': 0, 'Mounth_task': "test1", 'Week_task': "test2", 'Day_task': "test3", 'Rememeber': "test4"}}
    a['Ирина'] = {'Name':'Ирина','Scope': 0, 'Mounth_task': "test1", 'Week_task': "test2", 'Day_task': "test3", 'Rememeber': "test4"}

    file = open("data.dmp", "wb")
    pk.dump(a, file)
    file.close()

def read(user):
    file = open("data.dmp", "rb")
    test = pk.load(file)[user]
    file.close()
    return test

def write(user, param, value):
    file = open("data.dmp", "rb")
    data = pk.load(file)
    file.close()

    data[user][param] = value

    file = open("data.dmp", "wb")
    pk.dump(data, file)
    file.close()


def scope(user, value):
    scope = int(read(user)['Scope']) + int(value)
    write(user, 'Scope', scope)


