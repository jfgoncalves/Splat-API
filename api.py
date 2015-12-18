#!/bin/env python3

import requests
import json

SPLATNET_SCHEDULE_URL = "https://splatoon.nintendo.net/schedule/index.json?utf8=✓"

#Set this with the _wag_session value of your cookie, by logging with your credentials before.

wagEU = ''
wagNA = ''
wagJP = ''

#based on https://github.com/Wiwiweb/SakuraiBot/blob/master/src/sakuraibot.py

def get_splatnet_schedule(splatnet_cookie):
    cookies = {'_wag_session': splatnet_cookie}

    response = requests.get(SPLATNET_SCHEDULE_URL, cookies=cookies, data={'locale':"ja"})
    status = response.status_code

    #Check if splatoon.nintendo.net is under maintenance

    if status == 503:
        data = status
    else:
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
                rotation["stages"]["ranked"] = rotation["stages"]["gachi"]
                del rotation["stages"]["gachi"]

                regular = rotation["stages"]["regular"]
                ranked = rotation["stages"]["ranked"]

                for map in regular:
                    del map["asset_path"]
                for map in ranked:
                    del map["asset_path"]
            else:
                for map in rotation["stages"]:
                    del map["asset_path"]

    return data

def write_schedule(splatnet_cookie, region):
    dataI = get_splatnet_schedule(splatnet_cookie)
    if dataI == 503:
        pass
    else:
        with open('/YOUR/PATH/TO/schedule_'+region+'.json', 'w', encoding='utf-8') as outfile:
            json.dump(dataI, outfile, ensure_ascii=False)


if __name__ == "__main__":

    write_schedule(wagEU, "eu")
    write_schedule(wagEU, "na")
    write_schedule(wagEU, "jp")
