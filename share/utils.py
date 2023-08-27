def file_reader(file):
    '''Reads file and splits the information into a list.'''
    with open(file, 'r') as f:
        return [line.split(',') for line in f.readlines()]
    
    
def parse(file):
    users = []
    for account in file:
        clientId, username, password, crn, pin = [account[i].strip() for i in range(5)]
        users.append([clientId, username, password, crn, pin])
        
    return users