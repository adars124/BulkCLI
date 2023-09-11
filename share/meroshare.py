import requests as req

from typing import Optional
import logging

logging.basicConfig(level=logging.INFO)

from .utils import token_error, status_error

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
    def user_login(self) -> Optional[str]:
        url = f'{URL}/meroShare/auth/'
        
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        
        payload: dict = {
            'clientId': self.user.clientId,
            'username': self.user.username,
            'password': self.user.password
        }
        
        r = req.post(url=url, json=payload, headers=headers)
        
        if r.status_code == 200:
            res = r.headers
            token = res['Authorization'].strip()
            return token
        else:
            logging.error(r.json()['message'])
            return None

    # Personal Details of the Client
    def perosnal_details(self, token: str) -> Optional[dict]:
        if token is None:
            token_error()
        else:
            url = f'{URL}/meroShare/ownDetail/'
            
            headers = {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Authorization': token
            }
                        
            r = req.get(url=url, headers=headers)
            
            if r.status_code == 200:
                return r.json()
            else:
                status_error(r.json())

    # BOID Details of the Client
    def client_boid_details(self, token: str, demat: str) -> Optional[dict]:
        if token is None:
            token_error()
        else:
            url = f'{URL}/meroShareView/myDetail/{demat}'
            
            headers = {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Authorization': token
            }

            r = req.get(url=url, headers=headers)
            
            if r.status_code == 200:
                return r.json()
            else:
                status_error(r.json())

    # Get details of the Applicable IPOs                
    def applicable_ipos(self, token: str) -> Optional[dict]:
        if token is None:
            token_error()
        else:
            url = f'{URL}/meroShare/companyShare/applicableIssue/'
            
            headers = {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Authorization': token
            }

            payload = {
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
                        
            r = req.post(url=url, json=payload, headers=headers)
            
            if r.status_code == 200:
                return r.json()
            else:
                status_error(r.json())
 
    # Bank details of the Client       
    def bank_details(self, token: str, bankCode: str) -> Optional[dict]:
        if token is None:
            token_error()
        else:
            url = f'{URL}/bankRequest/{bankCode}/'
            
            headers = {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Authorization': token
            }
            
            r = req.get(url=url, headers=headers)

            if r.status_code == 200:
                return r.json()
            else:
                logging.info(r.json()['message'])
                return None
    
    # Get the customer's code
    def get_customer_code(self, token: str, bankId: str) -> Optional[dict]:
        if token is None:
            token_error()
        else:
            url = f'{URL}/meroShare/bank/{bankId}/'
            
            headers = {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Authorization': token
            }
            
            r = req.get(url=url, headers=headers)
            
            if r.status_code == 200:
                return r.json()
            else:
                status_error(r.json())
    
    def select_bank(self, token: str, bankId: str) -> Optional[dict]:
        if token is None:
            token_error()
        else:
            url = f'{URL}/meroShare/bank/{bankId}'
            
            headers = {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Authorization': token
            }

            res = req.get(url=url, headers=headers)

            if res.status_code == 200:
                return res.json()
            else:
                status_error(res.json())
    
    # For applying IPO
    def apply_ipo(self, data) ->  Optional[dict]:
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
            status_error(r.json())
     
    # In order to apply from multiple accounts 
    def apply_share(self, user: User, kitta: str, companyShareId: int) -> Optional[dict]:
        if user:
            token = self.user_login()
            
            if token:
                personalDetails = self.perosnal_details(token=token)
                
                clientBoid = self.client_boid_details(token=token, demat=personalDetails['demat'])
                
                bankDetails = self.bank_details(token=token, bankCode=clientBoid['bankCode'])

                applicableIPO = self.applicable_ipos(token=token)['object']
                
                shareCriteriaId = ''
                
                for listed in applicableIPO:
                    if 'shareTypeName' in listed.keys():
                        url = f'{URL}/shareCriteria/boid/{personalDetails["demat"]}/{listed["companyShareId"]}'
                    
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
                        
                        if shareCriteriaId != '':
                            data['shareCriteriaId'] = shareCriteriaId
                        
                        apply = self.apply_ipo(data=data)
                        
                        if apply:
                            return apply
                else:
                    customerCode = self.get_customer_code(token=token, bankId=bankDetails['bank']['id'])['id']
                    
                    data = {
                        "accountBranchId": bankDetails['branch']['id'],
                        "accountNumber": bankDetails['accountNumber'],
                        "appliedKitta": kitta,
                        "bankId": bankDetails['bank']['id'],
                        "boid": personalDetails['boid'],
                        "companyShareId": companyShareId,
                        "crnNumber": user.crn,
                        "customerId": customerCode,
                        "demat": clientBoid['boid'],
                        "transactionPIN": user.pin,
                        "token": token
                    }

                    if shareCriteriaId != '':
                        data['shareCriteriaId'] = shareCriteriaId
                        
                    apply = self.apply_ipo(data=data)
                    
                    if apply:
                        return apply
                   