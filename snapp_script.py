# 1. GET to /service-worker.js for client ID and client secret
# 2. POST to /api/api-passenger-oauth/v2/otp for sneding mobile number to the server
# 3. POST to /api/api-passenger-oauth/v2/auth with client ID and client secret and sms code to get access token
# 4. POST to /api/api-base/v2/passenger/config with access token to get some user's info like favorite places and their addresses
import requests, re, sys, json

base_url = "https://app.snapp.taxi"
session = requests.session() #all the requests will be made in this session

# 1:
js_res = session.get(base_url + "/service-worker.js") # this js file contains client ID and secrect

if js_res.status_code == 200:
    # Define regular expressions to match the client ID and client secret
    client_id_pattern = r'PWA_CLIENT_ID:"(.*?)"'
    client_secret_pattern = r'PWA_CLIENT_SECRET:"(.*?)"'

    # Use re.search to find the values in js_res
    client_id_match = re.search(client_id_pattern, js_res.text) #index 1 of the matched regex object gives us the part in the double qoutes meaning "(.*?)" 
    client_secret_match = re.search(client_secret_pattern, js_res.text)

    if client_id_match and client_secret_match:
        client_id = client_id_match[1]
        client_secret = client_secret_match[1]
    else:
        sys.exit("Client_id and Client_secret is missing from the JS file!")
else:
    sys.exit("The JS file containing client_id and client_secret can't be fetched!")    

         
# 2:
user_number = input("Enter your mobile number starting with +98: ")
otp_res = session.post(base_url + "/api/api-passenger-oauth/v2/otp", data={"cellphone" : user_number}) # we should check this res to see if the otp operation is OK
if json.loads(otp_res.text)["status"] != "OK": #first we should turn the res string into json object and then access it's elements which here is only status
    sys.exit("OTP operation failed!")
otp_code = input("Enter the SMS code sent to you: ")

# 3:
otp_validation_res = session.post(base_url + "/api/api-passenger-oauth/v2/auth", data={"grant_type":"sms_v2","client_id":client_id,"client_secret":client_secret,"cellphone":"+989013078187","token":otp_code,"referrer":"pwa"})
if otp_validation_res.status_code != 200:
    sys.exit("OTP validation operation failed!")
access_token = json.loads(otp_validation_res.text)["access_token"] #extracting access_tojen from response  

# 4:
#this below temp data is just provided whithin the request so that the server can handle the req and we do not run into bad request
temp_unimportant_data = {"locale":"fa-IR","device_type":1,"version_code":4,"os_version":"msvfdibacOSS","device_name":"ovisosv","referrer":0}
user_info_res = session.post(base_url + "/api/api-base/v2/passenger/config", headers={"Authorization" : "Bearer " + access_token}, json=temp_unimportant_data)
if user_info_res.status_code != 200:
    sys.exit("Fetching user's info failed:\n" + user_info_res.text)
#extracting user's favorite places:    
user_favorite_places = json.loads(user_info_res.text)["data"]["favorite_places"]
print("-----------------------------------")
for place, i in zip(user_favorite_places, range(len(user_favorite_places))): 
    print("{}:".format(i+1))
        
    print("User's chosen name for this place: " + place["name"])

    print("Formatted address of this place:\n" + place["location"]["formatted_address"] + "\n") 
