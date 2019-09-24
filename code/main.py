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
                    if k == "botid":
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
   
    if ping_url(address.address):
        if not address.status:
            address.status = True
            send_message(address.comment + " is up again")
    else:
        if (address.status):
            address.status = False
            send_message(address.comment + " is down")
            

def ping_url(url):

    i = 0;

    try:
        response_list = ping(url)

        for response in response_list:
            if (not response.success):
                i += 1

        if (i == 4):
            return False
        else:
            return True
            
    except Exception as e:
        send_message(str(e))

def main():

    init()

    while True:

        for host in hosts_list:
            ping_host(host)

        time.sleep(30)

if __name__ == '__main__':
    main()