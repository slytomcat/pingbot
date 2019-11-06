from telegram import Bot
from pythonping import ping
import time
import yaml
from libs.host import address  

def init():
    global bot, userid

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

        except yaml.YAMLError as exc:
            print(exc)

def set_hosts(hosts):

    global hosts_list
    hosts_list = []

    for item in hosts:
        ac = item.split(":")
        hosts_list.append(address(ac[0], ac[1]))

def send_message(message):
    bot.send_message(userid, message, parse_mode='HTML', disable_web_page_preview=True)

def ping_host(address):
   
    status = ping_url(address.address)
    if status != address.status:
        send_message(address.comment + ( " is unresolwed" if status is none elseif status " is up" else " is down"))
        address.status = staus
            

def ping_url(url):

    try:
        response_list = ping(url)
    except:
        return None

    return 4 == sum(1 for x in response_list if x == response.success)

def main():

    init()

    while True:

        for host in hosts_list:
            ping_host(host)

        time.sleep(30)

if __name__ == '__main__':
    main()
