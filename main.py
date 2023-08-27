from share.meroshare import MeroShare, User
from share.utils import file_reader, parse

import termcolor
from tabulate import tabulate

input_file = file_reader('accounts.txt')

accounts = parse(input_file)

try:
    companyShareId = ''
    kitta = ''
    for account in accounts:
        clientId, username, password, crn, pin = [account[i] for i in range(5)]
        
        user = User(clientId=clientId, username=username, password=password, crn=crn, pin=pin)
        m = MeroShare(user=user)
        
        token = m.user_login()

        if companyShareId == '' or kitta == '':
            applicableIPO = m.applicable_ipos(token=token)['object']
            
            termcolor.cprint("\nIPOs available for application:\n", 'green')
            col_names = ['S.N.', 'Company Name', 'Share Type', 'Company ID']

            data = []
            
            for i, company in enumerate(applicableIPO):
                data.append([i+1, company['companyName'], company['shareGroupName'], company['companyShareId']])
            
            termcolor.cprint(tabulate(data, headers=col_names, tablefmt="grid"), 'blue')

            index = int(input("\nWhich company would you like to apply for: "))
            companyShareId = data[index - 1][3]
            
            kitta = str(input("\nEnter the no. of kittas: "))
            
        personalDetails = m.perosnal_details(token=token)
        
        print("\n")
        termcolor.cprint(f'Applying {kitta} units from: {personalDetails["name"]}\n', 'green', attrs=['bold'])
        
        try:
            apply = m.apply_share(user=user, kitta=kitta, companyShareId=companyShareId)
            termcolor.cprint(apply['message'], 'yellow', attrs=['bold'])
        except Exception as e:
            termcolor.cprint(f'\nThere was a problem applying the shares from {personalDetails["name"]}. Please try again later!', 'red', attrs=['bold'])
            print('Error: ', e)
        
except Exception as e:
    print('Error: ', e)