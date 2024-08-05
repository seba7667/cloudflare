Update Location Dns script
Script used to dynamicaly check the public IP address and in case of the change it will replace it on the CloudFlare DNS Gateway.
Usefull for Dynamic IP assigment and dual-home sites.

To run Update Location Dns script you need to have a dedicated python file called: credentials.py.
This file needs to have:
account_id = ""
token_id = ""
location_name = ""
