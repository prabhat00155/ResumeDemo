import urllib.request
import json

def resume_predict(profile_data):
    data = {
        "Inputs": {
                "input1":
                [
                   profile_data
                ],
        },
    "GlobalParameters":  {}
    }

    body = str.encode(json.dumps(data))

    url = 'https://ussouthcentral.services.azureml.net/subscriptions/a148ec5553064f8f907e0fc6415333ae/services/20a66283a7884d5481bf78d91c72aca1/execute?api-version=2.0&format=swagger'
    api_key = 'nyOppUQx5VKT9P1t1+TGLp+UJpS9uEm2yHCP5bGlmsLPBxttvL1sDYwlRZM6jaFgSCOYFmstpmeuInAZuzFZjQ=='
    headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

    req = urllib.request.Request(url, body, headers)
    result = ""
    try:
        response = urllib.request.urlopen(req)
        result = response.read().decode('utf-8')
        #print(result)
    except urllib.error.HTTPError as error:
        print("The request failed with status code: " + str(error.code))

        # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
        print(error.info())
        print(json.loads(error.read().decode("utf8", "ignore")))
    return result