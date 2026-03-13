# Gunicorn configuration file for Render
# https://docs.gunicorn.org/en/stable/configure.html

import multiprocessing

# Server socket
bind = "0.0.0.0:8000"

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 120
keepalive = 5

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"

# Process naming
proc_name = "smartgalpon-api"

# Server mechanics
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

# SSL (not needed for Render, handled by their proxy)
certfile = None
keyfile = None
ca_certs = None

# Graceful timeout
graceful_timeout = 30
