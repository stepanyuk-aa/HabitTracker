def create_log(time, master, slave, changes):
    string = str(time)[:10] + ';' + str(master) + ';' + str(slave) + ';' + str(changes) + ';\n'

    file = open('track_log.csv', 'a+')
    file.write(string)
    file.close()

def read_log(n = 3):
    file = open('track_log.csv', 'r')
    logs = file.readlines()
    n = len(logs) - n
    logs = logs[n:]
    file.close()

    if type(n) == type([]):
        return logs
    else:
        return [logs]

