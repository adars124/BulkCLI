import requests as req

URL = 'https://webbackend.cdsc.com.np/api'
    
class User:
    def __init__(self, clientId: int, username: str, password: str, crn: str, pin: int):
        self.clientId = clientId
        self.username = username
        self.password = password
        self.crn = crn
        self.pin = pin
        
class MeroShare:
    def __init__(self, user: User):
        self.user = user

    # Login user
    def user_login(self) -> str:
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        
        client_data: dict = {
            'clientId': self.user.clientId,
            'username': self.user.username,
            'password': self.user.password
        }
        
        url = f'{URL}/meroShare/auth/'
        
        r = req.post(url=url, json=client_data, headers=headers)
        
        if r.status_code == 200:
            res = r.headers
            token: str = res['Authorization'].strip()
            return token
        else:
            res = r.json()['documentation']
            print(res)
            return

    # Personal Details of the Client
    def perosnal_details(self, token: str) -> dict:
        if token is None:
            print('Invalid Token! User Not Authenticated.')
            return
        else:
            headers = {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Authorization': token
            }
            
            url = f'{URL}/meroShare/ownDetail/'
            
            r = req.get(url=url, headers=headers)
            
            if r.status_code == 200:
                return r.json()

    # BOID Details of the Client
    def client_boid_details(self, token: str, demat: str) -> dict:
        if token is None:
            print('Invalid Token! User Not Authenticated.')
            return
        else:
            headers = {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Authorization': token
            }

            url = f'{URL}/meroShareView/myDetail/{demat}'
            
            r = req.get(url=url, headers=headers)
            
            if r.status_code == 200:
                return r.json()

    # Get details of the Applicable IPOs                
    def applicable_ipos(self, token: str) -> dict:
        if token is None:
            print('Invalid Token! User Not Authenticated.')
            return
        else:
            headers = {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Authorization': f'{token}'
            }

            json_data = {
                'filterFieldParams': [
                    {
                        'key': 'companyIssue.companyISIN.script',
                        'alias': 'Scrip',
                    },
                    {
                        'key': 'companyIssue.companyISIN.company.name',
                        'alias': 'Company Name',
                    },
                    {
                        'key': 'companyIssue.assignedToClient.name',
                        'value': '',
                        'alias': 'Issue Manager',
                    },
                ],
                'page': 1,
                'size': 10,
                'searchRoleViewConstants': 'VIEW_APPLICABLE_SHARE',
                'filterDateParams': [
                    {
                        'key': 'minIssueOpenDate',
                        'condition': '',
                        'alias': '',
                        'value': '',
                    },
                    {
                        'key': 'maxIssueCloseDate',
                        'condition': '',
                        'alias': '',
                        'value': '',
                    },
                ],
            }       
            
            url = f'{URL}/meroShare/companyShare/applicableIssue/'
            
            r = req.post(url=url, json=json_data, headers=headers)
            
            if r.status_code == 200:
                return r.json()
 
    # Bank details of the Client       
    def bank_details(self, token: str, bankCode: str) -> dict:
        if token is None:
            print('Invalid Token! User Not Authenticated.')
            return
        else:
            headers = {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Authorization': f'{token}'
            }

            url = f'{URL}/bankRequest/{bankCode}/'
            r = req.get(url=url, headers=headers)

            if r.status_code == 200:
                return r.json()
    
    # Get the customer's code
    def get_customer_code(self, token: str, bankId: str) -> dict:
        if token is None:
            print("Invalid Token! User Not Authenticated.")
            return
        else:
            headers = {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Authorization': f'{token}'
            }
            
            url = f'{URL}/meroShare/bank/{bankId}/'
            
            r = req.get(url=url, headers=headers)
            
            if r.status_code == 200:
                return r.json()
    
    def select_bank(self, token: str, bankId: str) -> dict:
        if token is None:
            print('Invalid Token! User Not Authenticated.')
            return
        else:
            headers = {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Authorization': token
            }

            url = f'{URL}/meroShare/bank/{bankId}'

            res = req.get(url=url, headers=headers)

            if res.status_code == 200:
                return res.json()
    
    # For applying IPO
    def apply_ipo(self, data) ->  dict:
        url = f'{URL}/meroShare/applicantForm/share/apply/'
        
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': data['token']
        }
        
        r = req.post(url=url, json=data, headers=headers)
        
        if r.status_code == 200 or r.status_code == 201 or r.status_code == 409:
            return r.json()
        else:
            return
     
    # In order to apply from multiple accounts 
    def apply_share(self, user: User, kitta: str, companyShareId: int) -> dict:
        if user:
            token = self.user_login()
            
            personalDetails = self.perosnal_details(token=token)
            
            clientBoid = self.client_boid_details(token=token, demat=personalDetails['demat'])
            
            bankDetails = self.bank_details(token=token, bankCode=clientBoid['bankCode'])

            applicableIPO = self.applicable_ipos(token=token)['object']
            
            shareCriteriaId = ''
            
            if applicableIPO[0]['shareTypeName'] == 'RESERVED':
                
                url = f'{URL}/shareCriteria/boid/{personalDetails["demat"]}/{applicableIPO[0]["companyShareId"]}'
                
                res = req.get(url=url, headers={
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                    'Authorization': token
                })
                
                if res.status_code == 200:
                    shareCriteriaId = res.json()['id']
            
            if bankDetails is None:
                url = f'{URL}/meroShare/bank/'

                headers = {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                    'Authorization': token
                }

                res = req.get(url=url, headers=headers)

                if res.status_code == 200:
                    resp = res.json()
                    
                    bank = self.select_bank(token, resp[0]['id'])
                    
                    if shareCriteriaId != '':
                    
                        data = {
                            "accountBranchId": bank['accountBranchId'],
                            "accountNumber": bank['accountNumber'],
                            "appliedKitta": kitta,
                            "shareCriteriaId": shareCriteriaId,
                            "bankId": bank['bankId'],
                            "boid": personalDetails['boid'],
                            "companyShareId": companyShareId,
                            "crnNumber": user.crn,
                            "customerId": bank['id'],
                            "demat": clientBoid['boid'],
                            "transactionPIN": user.pin,
                            "token": token
                        }
                    else:
                        
                        data = {
                            "accountBranchId": bank['accountBranchId'],
                            "accountNumber": bank['accountNumber'],
                            "appliedKitta": kitta,
                            "bankId": bank['bankId'],
                            "boid": personalDetails['boid'],
                            "companyShareId": companyShareId,
                            "crnNumber": user.crn,
                            "customerId": bank['id'],
                            "demat": clientBoid['boid'],
                            "transactionPIN": user.pin,
                            "token": token
                        }
                    
                    apply = self.apply_ipo(data=data)
                    
                    if apply:
                        return apply
            else:
                customerCode = self.get_customer_code(token=token, bankId=bankDetails['bank']['id'])['id']
                
                if shareCriteriaId != '':
                    
                    data = {
                        "accountBranchId": bankDetails['branch']['id'],
                        "accountNumber": bankDetails['accountNumber'],
                        "appliedKitta": kitta,
                        "bankId": bankDetails['bank']['id'],
                        # "shareCriteriaId": shareCriteriaId,
                        "boid": personalDetails['boid'],
                        "companyShareId": companyShareId,
                        "crnNumber": user.crn,
                        "customerId": customerCode,
                        "demat": clientBoid['boid'],
                        "transactionPIN": user.pin,
                        "token": token
                    }
                else:

                    data = {
                        "accountBranchId": bankDetails['branch']['id'],
                        "accountNumber": bankDetails['accountNumber'],
                        "appliedKitta": kitta,
                        "bankId": bankDetails['bank']['id'],
                        # "shareCriteriaId": shareCriteriaId,
                        "boid": personalDetails['boid'],
                        "companyShareId": companyShareId,
                        "crnNumber": user.crn,
                        "customerId": customerCode,
                        "demat": clientBoid['boid'],
                        "transactionPIN": user.pin,
                        "token": token
                    }
                    
                apply = self.apply_ipo(data=data)
                
                if apply:
                    return apply
                else:
                    print('Some error occured!')
                    return
                   