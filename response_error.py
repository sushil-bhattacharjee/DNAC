import requests

from requests.exceptions import Timeout

dnac_url = "https://sandboxdnac.cisco.com/api/v1/network-device"

sess = requests.session()

try:
    rc = sess.request('GET', dnac_url, timeout=1)
    
except Timeout:
    print('Timeout ERROR: Unable to access DNA Centre!')
    exit(-1)
if rc.status_code == requests.code.ok :
    print('The request was successful')
    
else:
    print(f'Error Code: {rc.status_code}: {rc.reason}')
