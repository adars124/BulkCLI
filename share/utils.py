import logging
import requests

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

def token_error():
    logging.error('Token is invalid.')
    return None

def status_error(response):
    logging.error(response['documentation'])
    return None