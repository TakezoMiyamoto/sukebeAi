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

  # 画像をpersonにセットする
  def addFaceToPerson(personId, imageUrl):
    """
    PersonにFaceを追加
    params:
        - personId:
        - imageUrl: personに追加したい画像URL
    return:
    """
    if personId != None:
      end_point = BASE_URL + "persongroups/" + GROUP_NAME + "/persons" + personId + "/persistedFaces"
      print(end_point)
      headers = {"Ocp_Apim-Subscription-Key" :SUBSCRIPTION_KEY}
      payload = {
        "url" = imageUrl
      }
      r = requests.post(
          end_point,
          headers = headers,
          json = payload
      )
      try:
        print("Successfuly added face to person")
        persistedFaceId = r.json()
      except Exception as e:
        print("Failed to add a face to person")
        print(e)
        persistedFaceId = None
      return persistedFaceId

    else:
      print("personId is not set.")
      return None













