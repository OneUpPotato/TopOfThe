from time import sleep
from threading import Thread
from datetime import timedelta

from settings import load_configs
load_configs()

from helpers import current_time
from post_handler import post_totd

def handle_totd():
    while True:
        time = current_time()
        time_remaining = (timedelta(hours=24) - (time - time.replace(hour=0, minute=0, second=0, microsecond=0))).total_seconds() % (24 * 3600)
        sleep(time_remaining)
        post_totd()

# Start the threads.
Thread(target=handle_totd).start()
post_totd()
