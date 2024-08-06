import http.client, requests, json, ssl
import credentials

def get_public_ip():
    try:
        resposne = requests.get("http://httpbin.org/ip")
        if resposne.status_code == 200:
            ip_data = resposne.json()
            public_ip = ip_data.get("origin")
            return public_ip
        else:
            return "Unable to fetch public IP"
    except requests.RequestException:
        return "Unable to connect to the Internet"
    
def get_location_id(account_id, location_name):
    conn = http.client.HTTPSConnection(
        "api.cloudflare.com",
        context = ssl._create_unverified_context() #skip SSL check, required due to company proxy
    )

    headers = {
        'Content-Type': "application/json",
        'Authorization': token_id         
    }
    conn.request("GET", "/client/v4/accounts/" + account_id + "/gateway/locations", headers=headers)
    res = conn.getresponse()
    data = res.read()
    data_dict = json.loads(data.decode("utf-8"))
    for location in data_dict["result"]:
        if location_name in location['name']:
            return location["id"]

    
def check_cf_public_ip(account_id, location_id):
    conn = http.client.HTTPSConnection(
        "api.cloudflare.com",
        context = ssl._create_unverified_context() #skip SSL check, required due to company proxy
        )
    headers = {
        'Content-Type': "application/json",
        'Authorization': token_id   
        }
    conn.request("GET", "/client/v4/accounts/" + account_id + "/gateway/locations/" + location_id, headers=headers)
    res = conn.getresponse()
    data = res.read()
    data_dict = json.loads(data.decode("utf-8"))
    cf_public_ip = data_dict["result"]["networks"]

    return cf_public_ip

def update_cf_public_ip(public_ip, account_id, location_name, temporary_location_name):
    conn = http.client.HTTPSConnection(
        "api.cloudflare.com",
        context = ssl._create_unverified_context() #skip SSL check, required due to company proxy
        )

    payload_to_add = {
        "client_default": True,
        "ecs_support": False,
        "name": location_name,
        "networks": [{"network": public_ip + "/32"}]
        }
    
    payload_to_remove = {
        "client_default": True,
        "ecs_support": False,
        "name": location_name,
        "networks": []
        }
    
    payload_for_temp = {
        "client_default": True,
        "ecs_support": False,
        "name": temporary_location_name, 
        "networks": [],
        "endpoints": {"ipv4": {"enabled": False}, 
        "ipv6": {"enabled": True}, 
        "dot": {"enabled": True}, 
        "doh": {"require_token": False, "enabled": True}}
        }

    headers = {
        'Content-Type': "application/json",
        'Authorization':  token_id
        }
    
    conn.request(
        "POST", 
        "/client/v4/accounts/" + account_id + "/gateway/locations", 
        json.dumps(payload_for_temp, indent=2).encode('utf-8'), 
        headers=headers
        ) # temporarly create new default DNS location
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))

    conn.request(
        "DELETE", 
        "/client/v4/accounts/" + account_id + "/gateway/locations/" + get_location_id(account_id, location_name), 
        json.dumps(payload_to_remove, indent=2).encode('utf-8'), 
        headers=headers
        ) # temporarly remove old production DNS location
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))

    conn.request(
        "POST", 
        "/client/v4/accounts/" + account_id + "/gateway/locations/", 
        json.dumps(payload_to_add, indent=2).encode('utf-8'), 
        headers=headers
        ) # create new production DNS location
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))

    conn.request(
        "DELETE", 
        "/client/v4/accounts/" + account_id + "/gateway/locations/" + get_location_id(account_id, temporary_location_name), 
        json.dumps(payload_for_temp, indent=2).encode('utf-8'), 
        headers=headers
        ) # remove temp DNS location
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))
    
if __name__ == "__main__":
    account_id = credentials.account_id
    token_id =   credentials.token_id
    location_name = credentials.location_name
    temporary_location_name = "TMP"
    public_ip = get_public_ip()
    cf_public_ip = check_cf_public_ip(account_id, get_location_id(account_id, location_name))

    print(f"Your Public IP is {public_ip}, CF public: {cf_public_ip}")
    if public_ip not in cf_public_ip[0]["network"] and "Unable to" not in public_ip:
        update_cf_public_ip(
            public_ip, 
            account_id, 
            location_name, 
            temporary_location_name
            )
