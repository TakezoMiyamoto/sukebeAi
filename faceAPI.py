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

# Person と Person Faceを一致させるために画像を学習させる
def trainGroup(groupId):
  end_point = BASE_URL + "persongroups/" + GROUP_NAME + "/train"
  headers = {
    "Ocp_Apim-Subscription-Key" :SUBSCRIPTION_KEY
  }
  r = requests.post(
      end_point,
      headers = headers,
  )
  print(r.text)

# 画像のURLを送信すると、その中の顔を検知してFaceIdを返す
def detectFace(imageUrl):
  """
  学習済みのpersonGroupの中で、送信する画像のURLから似ている候補を取得できる
  """
  end_point = BASE_URL + "detect"
  headers = {
    "Ocp_Apim-Subscription-Key" :SUBSCRIPTION_KEY
  }
  payload = {
    "url": imageUrl
  }
  r = requests.post(
      end_point,
      json = payload,
      headers = headers
  )
  try:
    faceId = r.json()[0]["faceId"]
    print("faceId Found:{}".format(faceId))
    return r.json()[0]
  except Exception as e:
    print("faceId no found:{}".format(e))
    return None

#Fade IDをもとに、学習された画像を特定する。一致する女優がJSON形式で帰ってくる。

def identifyPerson(faceId):
  end_point = BASE_URL + "identify"
  headers = {
    "Ocp_Apim-Subscription-Key" :SUBSCRIPTION_KEY
  }
  faceIds = [faceId]
  payload = {
    "faceIds" :faceIds,
    "personGroupId" :GROUP_NAME,

  }
  r = requests.post(
      end_point,
      json = payload,
      headers = headers
  )
  print(r.text)


if __name__ = '__main__':
  #pandasでcsvからAV女優を学習させます
  #AV女優のリストを取得する
  df = pd.read_csv("romaned.csv",index_col=0)
  df2 = pd.read_csv("learning-default.csv", index_col=0)

  for i, row in df.iterrows(): #,name,kana,image,dmmimage,roman
    name = row["name"]
    kana = row["kana"]
    image = row["image"]
    dmmimage = row["dmmimage"]
    #personを登録し、personIdを返す
    personId = makePerson(name)
    #personIdをもとに、そのpersonにスクレイピングした画像とDMMの画像を追加する。
    addFaceToPerson(personId, dmmimage)
    addFaceToPerson(personId, image)
    se = pd.Series([name,kana,image,dmmimage,personId],["name","kana","image","dmmimage","personId"])
    df2 = df2.append(se,ignore_index=True)
    print(df2)  

  #画像からpersonを特定するときのサンプルコード
  image = "https://cdn.mainichi.jp/vol1/2016/09/02/20160902ddm001010041000p/9.jpg?1"
  faceId = detectFace(image)
  person = identifyPerson(faceId["faceId"])
  if person["candidates"]: #学習データに候補があれば
      personId = person["candidates"][0]["personId"]
      personInfo = getPersonInfoByPersonId(personId)
      print(personInfo["name"])
  else:
      print("No candidates found")
      











