import os
import json
import requests
import subprocess
import sys
import xmltodict
import dicttoxml
import json
import asyncio

async def bouyomi(request, port=50081):
    res = requests.get(
        "http://localhost:" + str(port) + "/Talk",
        params=request)
    return res.status_code
"""
requestの種類
            'text':ゆっくりしていってね
            'voice':0
            'volume':-1
            'speed':-1
            'tone':-1
"""

def bouyomi_douki(text='ゆっくりしていってね', voice=0, volume=-1, speed=-1, tone=-1, port=50080):
    res = requests.get(
        "http://localhost:" + str(port) + "/Talk",
        params={
            'text': text,
            'voice': voice,
            'volume': volume,
            'speed': speed,
            'tone': tone})
    return res.status_code

if __name__ == "__main__":
    path = './config.json'
    print("設定ファイルを探します(./config.json)")
    if os.path.isfile(path):
        print("設定ファイルが見つかりました")
        f = open(path, 'r')
        config = json.load(f)
        f.close()
        print("設定ファイルをロードしました")
    else:
        print("設定ファイルが見つかりませんでした")
        print("デフォルト設定ファイルを新たに作成します")
        config = {}
        config["kosuu"] = 5
        config["port"] = 50080
        for i in range(5):
            config[str(i)] = {"folder":i,"port":50080 + i}
        f = open(path, 'w')
        json.dump(config, f)
        f.close()
        print("デフォルト設定ファイルを新たに作成しました")
    print(config)
    miss_bouyomi = []
    mitukatta = []
    bouyomi_port_list = []
    bouyomi_true_port_list = []
    for i in range(config["kosuu"]):
        if os.path.isfile("./" + str(config[str(i)]["folder"]) + "/BouyomiChan.exe"):
            pass
            print(str(i + 1) + "番目の棒読みちゃんが見つかりました")
            print("設定ファイルを読み込みます")
            bouyomi_setting_f = open("./" + str(config[str(i)]["folder"]) + "/BouyomiChan.setting", 'r',encoding="utf-8")
            bouyomi_setting = bouyomi_setting_f.read()
            bouyomi_setting = xmltodict.parse(bouyomi_setting)
            bouyomi_setting_f.close()
            bouyomi_port = int(bouyomi_setting["Settings"]["PortNumberHttp"])
            if(bouyomi_port != config[str(i)]["port"]):
                print("configファイルに記述されているポート番号(" + str(config[str(i)]["port"]) + ")と棒読みちゃんの設定に記述されているポート番号(" + str(bouyomi_port) + ")が異なります")
            bouyomi_port_list += [config[str(i)]["port"]]
            bouyomi_true_port_list += [bouyomi_port]
            print("起動します")
            proc = subprocess.Popen("./" + str(config[str(i)]["folder"]) + "/BouyomiChan.exe")
            mitukatta += [i]
        else:
            print(str(i + 1) + "番目の棒読みちゃん(" + "./" + str(config[str(i)]["folder"]) + "/BouyomiChan.exe" +")が見つかりません")
            miss_bouyomi += [i]
    
    if(miss_bouyomi != []):
        print("見つからなかった棒読みちゃんが" + str(len(miss_bouyomi)) + "個ありますが、実行を続けますか?y/n(見つからなかった棒読みちゃんは無視されます)")
        hentou = input()
        while not(hentou == "y" or hentou == "n"):
            print("yとn以外の返答がされました")
            print("見つからなかった棒読みちゃんが" + str(len(miss_bouyomi)) + "個ありますが、実行を続けますか?y/n(見つからなかった棒読みちゃんは無視されます)")
            hentou = input()
        if (hentou == "n"):
            print("終了します")
            os.system('PAUSE')
            sys.exit()
    if(miss_bouyomi != [] or bouyomi_true_port_list != bouyomi_port_list):
        new_config = {}
        new_config["kosuu"] = len(mitukatta)
        new_config["port"] = config["port"]
        for i in range(len(mitukatta)):
            new_config[str(i)] = {"folder":config[str(mitukatta[i])]["folder"],"port":bouyomi_true_port_list[i]}
        config = new_config
        print("configを一時的に以下のように変更しました")
        print(config)
        print("configをファイルに反映しますか?(y/n)(そうしないと次回起動時に反映されません)")
        hentou = input()
        while not(hentou == "y" or hentou == "n"):
            print("yとn以外の返答がされました")
            print("configをファイルに反映しますか?(y/n)(そうしないと次回起動時に反映されません)")
            hentou = input()
        if (hentou == "y"):
            print("ファイルに反映します")
            f = open(path, 'w')
            json.dump(config, f)
            f.close()
            print("ファイルに反映させました")
    print("棒読みちゃんへの同時送信テストを行います")
    print("すべての棒読みちゃんが起動するまで待っててください")
    os.system('PAUSE')
    loop = asyncio.get_event_loop()
    for i in range(config["kosuu"]):
       loop.run_until_complete(bouyomi({"text":"これは" + str(i + 1) + "番目の棒読みちゃんです"},port=config[str(i)]["port"]))
#   非同期のほうがよかったのでそっちを標準にするが、一応同期するほうも残しておく
#   同期処理用↓
#    input()
#    for i in range(config["kosuu"]):
#        bouyomi_douki(text="これは" + str(i) + "番目の棒読みちゃんです",port=config[str(i)]["port"])
    print("棒読みちゃんへの同時送信テストを行いました")
    print("棒読みちゃんapiの受信サーバーを起動します")


from flask import Flask, render_template,request

app = Flask(__name__)

@app.route('/Talk', methods=["GET"])
def result_get1():
    req = request.args
    shorityuu = []
    for i in range(config["kosuu"]):
        res = requests.get("http://localhost:" + str(config[str(i)]["port"]) + "/gettalktaskcount")
        #gettalktaskcount
        shorityuu += [res.json()["talkTaskCount"]]
    print(shorityuu)
    loop.run_until_complete(bouyomi(req,port=config[str([i for i, x in enumerate(shorityuu) if x == min(shorityuu)][0])]["port"]))
    print(req)
    return "success"

@app.route('/test', methods=["GET"])
def result_get2():
    print("受信")
    print("リクエスト送信テストを実行します")
    res = requests.get("http://localhost:" + str(config["port"]) + "/Talk",params={"text":"これはテスト送信です"})
    print(res)
    return "success"

if __name__ == '__main__':
    app.debug = False
    app.run(host='localhost',port=config["port"])