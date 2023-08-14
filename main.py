import monitor

url = "https://h5api.m.taobao.com/h5/mtop.btrip.hotel.hoteldetailv2/1.0?jsv=xxxx"

cookie = "xxxx"

body = "data=xxxx"

room_type = ["高级大床房"]


if __name__ == '__main__':
    monitor.monitor(url=url, cookie=cookie, body=body, room_type=room_type)

