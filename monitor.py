import multiprocessing
import threading
import time

import requests
import json
from urllib.parse import *

from playsound import playsound

headers = {
    "accept": "application/json",
    "accept-language": "zh-CN,zh;q=0.9,en-CN;q=0.8,en;q=0.7",
    "content-type": "application/x-www-form-urlencoded",
    "sec-ch-ua": "\"Not/A)Brand\";v=\"99\", \"Google Chrome\";v=\"115\", \"Chromium\";v=\"115\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"macOS\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "x-channel": "pc",
    "x-fpt": "bIdentify(main.pc.pc.c)",
    "cookie": "",
    "Referer": "https://market.m.taobao.com/",
    "Referrer-Policy": "strict-origin-when-cross-origin"
}

success_process = None
error_process = None


def create_playsound_process(path: str):
    return multiprocessing.Process(target=playsound, args=(path,))


def get_rooms_data(room_type: [str], rooms: [object]):
    if room_type:
        rooms = list(filter(lambda t: t["name"] in room_type, rooms))
    rooms = list(map(lambda t: {"name": t["name"], "sellers": t["sellers"]}, rooms))
    for room in rooms:
        room["sellers"] = list(map(lambda t: list(map(lambda v: {
            "title": v["title"],
            "bedDesc": v["bedDesc"],
            "breakfastInfos": v["breakfastInfos"],
            "inventoryDesc": v["inventoryDesc"],
            "dinamicPriceWithTax": v["dinamicPriceWithTax"],
            "dinamicBreakfastDescTitle": v["dinamicBreakfastDesc"]["title"],
            "dinamicCancelDescTitle": v["dinamicCancelDesc"]["title"],
            "businessPay": v["businessPay"]
        }, t["items"])), room["sellers"]))
        room["prices"] = sorted(
            [float(m["dinamicPriceWithTax"]) for v in room["sellers"] for m in v])
    return rooms


def print_info(rooms: [object]):
    print("\n\n房型信息(可拷贝到json格式化工具中查看):")
    print(rooms)
    print()
    for room in rooms:
        print(room)

    print("\n房型价格列表(已做排序处理):")
    for room in rooms:
        print({room["name"]: room["prices"]})


def monitor(url, cookie=None, body=None, room_type=[]):
    global success_process
    global error_process
    headers["cookie"] = cookie
    session = requests.session()
    session.headers = headers
    count = 0
    while True:
        res = session.post(url, data=body)
        data = json.loads(res.text)
        if data["data"] == {}:
            if not error_process:
                error_process = create_playsound_process("张靓颖 - 如果这就是爱情.mp3")
                error_process.start()
                input("press ENTER to stop playback")
            if error_process and error_process.is_alive():
                error_process.terminate()
                error_process = None
            url = input("请输入新的url: ")
            cookie = input("请输入新的cookie: ")
            body = input("请输入新的body: ")
            headers["cookie"] = cookie
            session = requests.session()
            session.headers = headers
            continue
        count = count + 1
        rooms = data["data"]["roomTypes"]
        print("第" + str(count) + "次获取房间信息, 房间数量为" + str(len(rooms)))
        if len(rooms):
            rooms = get_rooms_data(room_type, rooms)
            print_info(rooms)
            if not success_process:
                success_process = create_playsound_process("宋祖儿 - 约定 (Live).mp3")
                success_process.start()
                time.sleep(180)
            if success_process and success_process.is_alive():
                success_process.terminate()
                success_process = None
            continue
        time.sleep(30)
