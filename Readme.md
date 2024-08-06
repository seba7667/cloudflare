###Update Location DNS
https://developers.cloudflare.com/cloudflare-one/connections/connect-devices/agentless/dns/
The script developed to dynamicaly check the public IP address and in case of the change it will replace it on the CloudFlare DNS Gateway.
Usefull for Dynamic IP assigment and dual-home sites.

To run Update Location Dns script you need to have a dedicated python file called: credentials.py.
This file needs to have:
account_id = "" # you can collect it from the CF Zero Trust URL https://one.dash.cloudflare.com/ACCOUNT_ID/home?tab=24h
token_id = "" # you can create it on the main CF page > right top corner > My Profile > API Tokens > Create Token, you need to assign all Zero Trust permissions
location_name = "" # your DNS location name from CF Zero Trust > Gateway > DNS Location
