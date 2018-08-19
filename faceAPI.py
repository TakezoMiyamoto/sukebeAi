import requests
import json
import logging
BASE_URL = "https://japaneast.api.cognitive.microsoft.com/face/v1.0/"
SUBSCRIPTION_KEY = ${92455ee48ae64f43b528dc41a0506280}
GROUP_NAME = ${avactress} 

def makeGroup():
  end_point = BASE_URL + "persongroups/" + GROUP_NAME
  payload = {
    "name": GROUP_NAME
  }
  headers = {
  "Ocp_Apim-Subscription-Key" :SUBSCRIPTION_KEY
  }
  r = requests.put(
      end_point,
      headers = headers,
      json = payload
  )
  print(r.text)

  def makePerson(personName):
    # makeGroupで作為性したgroupにpersonを追加する
    end_point = BASE_URL + "persongroups" + GROUP_NAME + "/persons"
    headers = {
      "Ocp_Apim-Subscription-Key" :SUBSCRIPTION_KEY
    }
    payload = {
      "name": name
    }
    r = requests.post(
        end_point,
        headers = headers,
        json = payload
    )
    try:
      personId = r.json()["personId"]
    except Exception as e:
      personId = None
      print(r.json()["error"])
    return personId
