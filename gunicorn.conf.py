bind = "127.0.0.1:8888"
accesslog = "/home/cagani/log/gunicorn_access.log"
errorlog = "/home/cagani/log/gunicorn_error.log"
pidfile = "/tmp/gunicorn.pid"
user = 'cagani'
group = 'cagani'
workers = 3
