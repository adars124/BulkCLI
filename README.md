
# BulkCLI

BulkCLI is a CLI application built on top of python which enables user to apply IPOs in bulk from multiple different accounts. In order to get started, consider the following steps:

## Step 1: Clone the repo
First clone the repository into your system by using the following command:
```
git clone https://github.com/adars124/BulkCLI.git
```

## Step 2: Install the requirements
Then, navigate to the folder where you have cloned this repo and install all the requirements using:
```
pip install -r requirements.txt
# or
python3 -m pip install -r requirements.txt
```
This will install all the required libraries/modules into your system that will make the program work.


## Step 3: Modify the accounts.txt file
The **accounts.txt** file contails dummy information in following format:

```
clientId, username, password, crn, pin
clientId, username, password, crn, pin
clientId, username, password, crn, pin
clientId, username, password, crn, pin
```
Change the information according to the respective name. You can follow the following approach:

**Note**: You can find the clientId in **capitals.json** file

```
# Should not contain spaces after comma
130,01234458,password@123,XYZ0231412,1234
```

## Step 4: Run the **main.py** file
After all the aforementioned steps are successfully completed, you can run the **main.py** file using `python main.py` command. And you are good to go. Enjoy using BulkCLI application. 😊
