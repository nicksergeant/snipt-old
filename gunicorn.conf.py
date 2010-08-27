import os

bind = "localhost:1337"
daemon = True                     # Whether work in the background
debug = False                     # Some extra logging
logfile = "./logs/gunicorn.log"                     # Name of the log file
loglevel = "info"                 # The level at which to log
pidfile = ".gunicorn.pid"     # Path to a PID file
workers = 1                       # Number of workers to initialize
umask = 0                         # Umask to set when daemonizing
user = None                       # Change process owner to user
group = None                      # Change process group to group
proc_name = "gunicorn-snipt"    # Change the process name
tmp_upload_dir = None             # Set path used to store temporary uploads

def after_fork(server, worker):
    server.log.info("Worker spawned (pid: %s)" % worker.pid)

before_fork=lambda server, worker: server.log.debug("Worker ready to fork!")
before_exec=lambda server: server.log.debug("Forked child, reexecuting")
