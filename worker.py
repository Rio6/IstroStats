import signal

import models
from istroWorker import IstrolidWorker

istro = IstrolidWorker()

def stop(*_):
    print("Stopping worker")
    istro.stop()

def main():
    signal.signal(signal.SIGINT, stop)
    signal.signal(signal.SIGTERM, stop)

    print("Starting worker")
    istro.start()

if __name__ == '__main__':
    main()
