import getpass
import os
import subprocess
from os import system, name


### ==================
###   JWT Generation
### ==================


def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear') 

def disclaimer():
   print("""
=============================================================================
  NEO Unbinding a database from an application for a particular data source
                                 Win/MacOS
=============================================================================

         
1. Generate JWT token.
      """)

def action():
    username = input("Enter your SAP email: ")
    password = getpass.getpass("Enter your global password: ")
    MFA = input("MFA for accounts.sap.com: ")
    cmd = [
        "curl",
        "--request", "POST",
        "https://oauthasservices.eu1.hana.ondemand.com/oauth2/api/v1/token?grant_type=password",
        "--header", "Content-Type: application/x-www-form-urlencoded",
        "--data-urlencode", f"username={username}",
        "--data-urlencode", f"password={password}{MFA}"
    ]   

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        token = subprocess.run(["jq", "-r", ".access_token"], input=result.stdout, capture_output=True, text=True, check=True).stdout.strip()

        if token != "null":
            print("\n*** JWT generated successfully! ***")
            return token
        else:
            print("\n\nFailed to extract access token. Please check your credentials and MFA code.")
            option()

    except subprocess.CalledProcessError as e:
        print(f"\n\nAn error occurred: {e}")
        print(f"\n\nCommand output: {e.output}")
        print(f"\n\nCommand stderr: {e.stderr}")
        option()       

def option():
    key = input("\n\nTo Try again please type 1: ")
    if key == "1":
        clear()
        disclaimer()
        action()
    else:
       exit()  

disclaimer()
jwt = action()


### ==============
###   Unbinding
### ==============


print("\n\n2. Unbind the database from the application.\n")

technical_name = input("Technical name of the of the target java service (not the system): ")
java_application = input("Java application(ex. c4paservices): ")
landscape = input("Landscape: ")
binding = input("Binding to be removed (Data Source): ")

if landscape.lower() == "ae1":
    host_name = "ae1.hana.ondemand.com"
elif landscape.lower() == "ap1":
    host_name = "ap1.hana.ondemand.com"
elif landscape.lower() == "br1":
    host_name = "br1.hana.ondemand.com"
elif landscape.lower() == "ca1":
    host_name = "ca1.hana.ondemand.com"
elif landscape.lower() == "cn1":
    host_name = "cn1.platform.sapcloud.cn"
elif landscape.lower() == "eu1":
    host_name = "eu1.hana.ondemand.com"
elif landscape.lower() == "eu2":
    host_name = "eu2.hana.ondemand.com"
elif landscape.lower() == "jp1":
    host_name = "jp1.hana.ondemand.com"
elif landscape.lower() == "sa1":
    host_name = "sa1.hana.ondemand.com"
elif landscape.lower() == "us1":
    host_name = "us1.hana.ondemand.com"
elif landscape.lower() == "us3":
    host_name = "us3.hana.ondemand.com"
elif landscape.lower() == "eudp":
    host_name = "hana.ondemand.com"

if name == 'nt':
    unbind = f"neo.bat unbind-db -a {technical_name} -b {java_application} -h {host_name} -s {binding} -u JWT -p {jwt}"
else:
    unbind = f"neo.sh unbind-db -a {technical_name} -b {java_application} -h {host_name} -s {binding} -u JWT -p {jwt}"

try:
    result = subprocess.run(unbind, shell=True, capture_output=True, text=True, check=True)
    lines = result.stdout.splitlines()
    for line in lines:
        if "Database" in line:
            print("\n*** Unbinding successful! ***\n\nResult:\n", line)
    print(f"\nErrors:\n{result.stderr}" if result.stderr else "")
except subprocess.CalledProcessError as e:
    print(f"An error occurred: {e}")
    print("Standard Output:\n", e.stdout)
    print("Standard Error:\n", e.stderr)