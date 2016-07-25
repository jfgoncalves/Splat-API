#!/bin/env python3

import requests
import json

#based on https://gist.github.com/anonymous/9c790980b4955a35187a

NINTENDO_LOGIN_PAGE = "https://id.nintendo.net/oauth/authorize"

SPLATNET_CALLBACK_URL = "https://splatoon.nintendo.net/users/auth/nintendo/callback"
SPLATNET_CLIENT_ID = "12af3d0a3a1f441eb900411bb50a835a"

SPLATNET_SCHEDULE_URL = "https://splatoon.nintendo.net/schedule/index.json?utf8=✓"

#Set this with your credentials

username_eu = ''
password_eu = ''
username_na = ''
password_na = ''
username_jp = ''
password_jp = ''

def get_english_name(name):
    jp_dict = {
    "アンチョビットゲームズ": "Ancho-V Games",
    "アロワナモール": "Arowana Mall",
    "Ｂバスパーク": "Blackbelly Skatepark",
    "ネギトロ炭鉱": "Bluefin Depot",
    "モンガラキャンプ場": "Camp Triggerfish",
    "ヒラメが丘団地": "Flounder Heights",
    "マサバ海峡大橋": "Hammerhead Bridge",
    "モズク農園": "Kelp Dome",
    "マヒマヒリゾート＆スパ": "Mahi-Mahi Resort",
    "タチウオパーキング": "Moray Towers",
    "キンメダイ美術館": "Museum d'Alfonsino",
    "ショッツル鉱山": "Piranha Pit",
    "ホッケふ頭": "Port Mackerel",
    "シオノメ油田": "Saltspray Rig",
    "デカライン高架下": "Urchin Underpass",
    "ハコフグ倉庫": "Walleye Warehouse",
    "ガチエリア": "Splat Zones",
    "ガチホコ": "Rainmaker",
    "ガチヤグラ": "Tower Control"
    }

    return jp_dict[name]

#based on https://github.com/Wiwiweb/SakuraiBot/blob/master/src/sakuraibot.py

def get_new_splatnet_cookie(u, pwd):
    parameters = {'client_id': SPLATNET_CLIENT_ID,
                  'response_type': 'code',
                  'redirect_uri': SPLATNET_CALLBACK_URL,
                  'username': u,
                  'password': pwd}

    #Nintendo being slow at updating their SSL cert on the backend, trying to fetch their json might fail once on a year. add verify=False to the request parameters to ignore the SSL cert and force the fetch regardless...

    #Comment this if the SSL cert on Nintendo's AWS has expired.
    response = requests.post(NINTENDO_LOGIN_PAGE, data=parameters)

    #UNcomment this if the SSL cert on Nintendo's AWS has expired.
    #response = requests.post(NINTENDO_LOGIN_PAGE, data=parameters, verify=False)

    cookie = response.history[-1].cookies.get('_wag_session')
    if cookie is None:
        raise Exception("Couldn't retrieve cookie")
    return cookie

def get_splatnet_schedule(splatnet_cookie):
    cookies = {'_wag_session': splatnet_cookie}

    response = requests.get(SPLATNET_SCHEDULE_URL, cookies=cookies, data={'locale':"ja"})
    status = response.status_code

    #Check if splatoon.nintendo.net is ready

    if status == 200:
        data = response.json()

        schedule = data["schedule"]
        festival = data["festival"]

        for rotation in schedule:

            #Clean names
            rotation["begin"] = rotation["datetime_begin"]
            del rotation["datetime_begin"]
            rotation["end"] = rotation["datetime_end"]
            del rotation["datetime_end"]

            if festival == False:
                rotation["ranked_mode"] = rotation["gachi_rule"]
                del rotation["gachi_rule"]
                rotation["ranked_modeEN"] = get_english_name(rotation["ranked_mode"])
                rotation["stages"]["ranked"] = rotation["stages"]["gachi"]
                del rotation["stages"]["gachi"]

                regular = rotation["stages"]["regular"]
                ranked = rotation["stages"]["ranked"]

                for map in regular:
                    del map["asset_path"]
                    map["nameEN"] = get_english_name(map["name"])
                for map in ranked:
                    del map["asset_path"]
                    map["nameEN"] = get_english_name(map["name"])
            else:
                for map in rotation["stages"]:
                    del map["asset_path"]
                    map["nameEN"] = get_english_name(map["name"])
    else:
        data = None

    return (status, data)

def write_schedule(u, pwd, region):
    splatnet_cookie = get_new_splatnet_cookie(u, pwd)
    statusI, dataI = get_splatnet_schedule(splatnet_cookie)

    if statusI == 200:
        with open('/YOUR/PATH/TO/schedule_'+region+'.json', 'w', encoding='utf-8') as outfile:
            json.dump(dataI, outfile, ensure_ascii=False)
    else:
        pass


if __name__ == "__main__":

    write_schedule(username_eu, password_eu, "eu")
    write_schedule(username_na, password_na, "na")
    write_schedule(username_jp, password_jp, "jp")
