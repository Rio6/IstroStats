#!/bin/sh
export PORT=8000
source env/bin/activate
python worker.py &
pid=$!
python web.py
kill $pid
wait $pid
