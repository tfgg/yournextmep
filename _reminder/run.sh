uwsgi --socket server.sock --wsgi-file reminder_server.py --callable app --chmod-socket=666 --daemonize server-yournextmep-reminder.log

