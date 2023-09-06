# Python-script-to-extract-user's-snapp.ir-data
This Python script logs into user's snapp application using user's cellphone number and OTP code and then extracts user's favorite places in snapp(iranian uber) application.

> **Usage :**
> 
> 
>     Just use the command <b>"python3 snapp_script.py"</b> to run the program 
> 
>     and follow the instructions in the terminal :)   
> 

> **BE AWARE :**
> 
> - I extracted the snapp APIs that I make requests to in the script by redirecting my network traffic into the Burp Suite application so that I can monitor the requests that [https://app.snapp.taxi](https://app.snapp.taxi/) makes and learn the APIs I should send requests to and how snapp servers handle those requests so that I can write this script.
> 
> - So if you want to extract any other data instead of user’s favorite places you can use Burp Suite to study to which APIs the requests are sent and how, when you click on different things or access different parts of the snapp web application and then you can update the code to your desire.

> **Libraries Used :**
> 
> - requests
> - json
> - re
> - sys
