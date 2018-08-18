import pandas as pd
import requests

# DMMアフェリエイトIDとAPI IDの指定
DMM_AFFILIATE_ID = ""
DMM_API_ID = ""
API_END_POINT = "https://api.dmm.com/affiliate/v3/ActressSearch?api_id=" + DMM_API_ID + "&affiliate_id" + DMM_AFFILIATE_ID + "&keyword={}" + "&output=json"

# カウンター で何件取得できたか数える
count = 0
skipped_count = 0

df1 = pd.read_csv("output.csv") # スクレイピングで取得したCSVファイル
df = pd.read_csv('default.csv', index_col=0) #DMMから撮ってきた結果を保存したいCSVをdfに設定

# for でdf1からname , image を行ごとに一個ずつ取り出す
for i, rows in df1.iterrows():
  name = rows["name"]
  image = rows["image"]
  try:
      end_point = API_END_POINT.format(name)
      r = requests.get(end_point)
      data = r.json()
      actress = data["result"]["actress"][0]["name"]
      if name == actress: #csvの女優名とDMMの女優名が一致した場合
          dmmimage = data["result"]["actress"][0]["imageURL"]["large"]
          birthday = data["result"]["actress"][0]["birthday"]
          height = data["result"]["actress"][0]["height"]
          B = data["result"]["actress"][0]["bust"]
          C = data["result"]["actress"][0]["cup"]
          W = data["result"]["actress"][0]["waist"]
          H = data["result"]["actress"][0]["hip"]
          print("name={}".format(name))
          print("image={}".format(image))
          print("dmmimage={}".format(dmmimage))
          print("height={}".format(height))
          print("birthday={}".format(birthday))
          print("bust={}".format(B))
          print("cup={}".format(C))
          print("hip={}".format(H))
          print("waist={}".format(W))
    # なにも取得できなかったり、エラーがでたら、何も値を入れないでおきます。
    except Exception as e:
      print(e)
      skipped_count += 1
      print("{}をスキップしました:スキップ数:{}".format(name,skipped_count))
      dmmimage = ""
      birthday = ""
      height = ""
      B = ""
      C = ""
      H = ""
      W = ""
    # 取得した値seをdf(データフレームオブジェクト)にぶち込みます。
    se = pd.Series([name,image,dmmimage,height,birthday,B,C,W,H],["name","image","height","birthday","B","C","W","H"])
    df = df.append(se,ignore_index=True)
    print(df)
# 取得した結果を, final.csvとしてデータを保存します。
df.to_csv("final.csv")
print("DONE")

