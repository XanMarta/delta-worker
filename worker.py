delta_url = "https://delta.xanmarta.workers.dev/0:/"

import os, time, threading
from google.colab import output
import os
FROM = ""
TO = ""
PARA = ""
run = False


def read_file(WORKER_NAME, WORKER_STATE):
    global FROM, TO, PARA, delta_url
    print('----- Downloading necessary files -----')
    try:
        if not os.path.isfile('/content/rclone.conf'):
            link = delta_url + WORKER_NAME + '/' + WORKER_STATE + '/rclone.conf'
            print('Downloading', link)
            !curl -O $link
        if not os.path.isfile('/content/path.txt'):
            link = delta_url + WORKER_NAME + '/' + WORKER_STATE + '/path.txt'
            print('Downloading', link)
            !curl -O $link
        print('----- Completed -----')
    except:
        print('Downloading error')
        return False
    with open('/content/path.txt', 'r') as f:
        try:
            content = f.read().split('\n')
            FROM = content[0]
            TO = content[1]
            PARA = content[2]
        except:
            print('Path file corrupted')
            !rm "/content/path.txt"
            return False
    return True


def running():
    global FROM, TO, PARA
    if not os.path.isfile('/usr/bin/rclone'):
        print('----- Installing rclone -----')
        !curl https://rclone.org/install.sh | sudo bash
    output.clear()
    os.environ['fromC'] = FROM
    os.environ['toC'] = TO
    os.environ['paraC'] = PARA
    print('FROM: ', FROM)
    print('TO:   ', TO)
    print('PARA: ', PARA)
    print('----- Syncing -----')
    !rclone sync --config=/content/rclone.conf "$fromC" "$toC" $paraC -v --drive-acknowledge-abuse


def clear_output():
    global run
    while True:
        output.clear()
        time.sleep(200)
        if not run:
            break


def worker(WORKER_NAME, WORKER_STATE):
    if os.path.isdir('/content/sample_data'):
        !rm -r '/content/sample_data'
    if read_file(WORKER_NAME, WORKER_STATE):
        run = True
        threading.Thread(target=clear_output).start()
        running()
        run = False

