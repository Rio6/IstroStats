#!/bin/sh
export PORT=8000
source venv/bin/activate
python worker.py &
pid=$!
python web.py
kill $pid
wait $pid
