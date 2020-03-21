import logging
import signal

import models
from istroWorker import IstrolidWorker

istro = IstrolidWorker()

def stop(*_):
    logging.info("Stopping worker")
    istro.stop()

def main():
    logging.getLogger().setLevel(logging.INFO)

    signal.signal(signal.SIGINT, stop)
    signal.signal(signal.SIGTERM, stop)

    logging.info("Starting worker")
    istro.start()

if __name__ == '__main__':
    main()
