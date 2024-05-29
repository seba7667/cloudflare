import http.client, requests, json


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
    
def check_cf_public_ip(account_id, location_id):
    conn = http.client.HTTPSConnection("api.cloudflare.com")

    headers = {
        'Content-Type': "application/json",
        'Authorization': "Bearer XHb1GZJ5Hoar2n8-KiP76PCJQrWaRQXbJ6HBinLt"    
        }
    conn.request("GET", "/client/v4/accounts/" + account_id + "/gateway/locations/" + location_id , headers=headers)
    res = conn.getresponse()
    data = res.read()
    data_list = json.loads(data.decode("utf-8"))
    cf_public_ip = data_list["result"]["networks"]
    return cf_public_ip

def update_cf_public_ip(public_ip, account_id, location_id, location_name):
    conn = http.client.HTTPSConnection("api.cloudflare.com")

    payload = "{\n  \"client_default\": true,\n  \"ecs_support\": false,\n  \"name\": \""+ location_name +"\",\n  \"networks\": [\n    {\n      \"network\": \""+ public_ip + "/32\"\n    }\n  ]\n}"
    headers = {
        'Content-Type': "application/json",
        'Authorization': "Bearer XHb1GZJ5Hoar2n8-KiP76PCJQrWaRQXbJ6HBinLt"    
        }
    conn.request("PUT", "/client/v4/accounts/" + account_id + "/gateway/locations/" + location_id ,payload , headers=headers)
    res = conn.getresponse()
    data = res.read()

    print(data.decode("utf-8"))
    
if __name__ == "__main__":
    account_id = "a0cc8f105980ac537a70355fc8584dad"
    location_id = "09583314bebb4ed0967d3d27430af062"
    location_name = "Podmiejska"


    public_ip = get_public_ip()
    cf_public_ip = check_cf_public_ip(account_id, location_id)
    print(f"Your Public IP is {public_ip}, CF public: {cf_public_ip}")
    if public_ip not in cf_public_ip[0]["network"]:
        update_cf_public_ip(public_ip, account_id, location_id, location_name)
        


