import os
import logging
import signal
from sqlalchemy import create_engine

from backend import IstrolidWorker, models

DATABASE_URL = 'sqlite:///database.db?check_same_thread=False'

istro = IstrolidWorker()

def stop(*_):
    logging.info("Stopping worker")
    istro.stop()

def main():
    logging.getLogger().setLevel(logging.INFO)

    signal.signal(signal.SIGINT, stop)
    signal.signal(signal.SIGTERM, stop)

    engine = create_engine(os.environ.get('DATABASE_URL', DATABASE_URL))
    models.init_models(engine)

    logging.info("Starting worker")
    istro.start()

if __name__ == '__main__':
    main()
