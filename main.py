import subprocess
import shlex
from io import StringIO
import json
from ftplib import FTP

def decode_json(command) -> str:
    """[summary]

        Return Azure data in json decoded version
        
    Args:
        command (str): Command argument given

    Returns:
        [json]: JSON encoded
    """
    # Converto command to popen format
    args = shlex.split(command)
    
    ## Get app service list
    #  Open process
    p = subprocess.Popen(args, stdout=subprocess.PIPE)
    
    # Create IO data reader
    io = StringIO(p.stdout.read().decode())
    
    # Formato io data reader in JSON
    return json.load(io)

def init_ftp(url) -> FTP:
    """[summary]

    Generate FTP Connection
    
    Args:
        url (str): Url to connect

    Returns:
        FTP: FTP Connection
    """
    url = url.replace("ftp://", "")
    url = url.replace("/site/wwwroot", "")
    print(url)
    return FTP(url)

def main() -> None:
    """[summary]
    Main function
    """
    
    # Set command to execute
    command = "az appservice plan list --query [].name"

    j = decode_json(command)
    j_appsrv = decode_json('az webapp list --query "[].name"')
    
    #TEST 
    print("App service plan {j}".format(j=j))
    
    for app in j_appsrv:
        
        url = decode_json(
                'az webapp deployment list-publishing-profiles --resource-group U87-PM-AppServices-pci-uat --name {0} --query "[1].publishUrl"'
                .format(app)
            )
        user = decode_json(
                'az webapp deployment list-publishing-profiles --resource-group U87-PM-AppServices-pci-uat --name {0} --query "[1].userName"'
                .format(app)
            )
        passwd = decode_json(
                'az webapp deployment list-publishing-profiles --resource-group U87-PM-AppServices-pci-uat --name {0} --query "[1].userPWD"'
                .format(app)
            )
        
        print("App service [{app}] connection url [{conn}] : \n{user}\n{passwd}\n".format(
                app=app,
                conn=url,
                user=user,
                passwd=passwd,
            )
        )
        
    ftp = init_ftp(url)
    ftp.login(user=user, passwd=passwd)
    print(ftp.retrlines("LIST"))
    
    

if __name__ == "__main__":
    main()