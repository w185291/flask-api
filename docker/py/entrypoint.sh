#!/bin/sh

cd /usr/src/app || exit
cp .env.local .env

if [ ! -f "/app/initialized" ]; then

    # exec command
    pip install -r requirements.txt
    export FLASK_APP=app.py
    # FLASK_APP=app.py flask db upgrade
    # FLASK_APP=app.py flask seed run
    # FLASK_APP=cli.py flask job create_master -n 'master' -p 'Test1234'

    # save flag
    touch /app/initialized
fi

# start app in background
# python app.py --host 0.0.0.0 --debugger --reload &

# keep docker running
tail -f  /dev/null



