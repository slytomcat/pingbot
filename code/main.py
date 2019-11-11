from telegram import Bot
from pythonping import ping
import time
import yaml
from libs.host import address

def init():
    global bot, userid, interval

    interval = 30

    with open('/usr/src/app/config.yaml') as f:
        try:
            docs = yaml.load_all(f, Loader=yaml.FullLoader)

            for doc in docs:
                for k, v in doc.items():
                    if k == "botkey":
                        bot = Bot(v)
                    elif k == "userid":
                        userid = v
                    elif k == "hosts":
                        set_hosts(v)
                    elif k == "interval":
                        interval = int(v)

        except yaml.YAMLError as exc:
            print(exc)

def set_hosts(hosts):

    global hosts_list
    hosts_list = [address(ip, desc) for desc, ip in hosts.items()]

def send_message(message):
    bot.send_message(userid, message, parse_mode='HTML', disable_web_page_preview=True)

def ping_host(address):

    status = ping_url(address.address)
    if status != address.status:
        send_message(address.comment + ( " is unresolwed" if status is None else " is up" if status else " is down"))
        address.status = status

def ping_url(url):

    try:
        response_list = ping(url)
    except:
        return None

    return sum(1 for x in response_list if x.success) > 0

def main():

    init()

    while True:

        for host in hosts_list:
            ping_host(host)

        time.sleep(interval)

if __name__ == '__main__':
    main()
