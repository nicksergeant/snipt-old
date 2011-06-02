bind = "unix:/tmp/gunicorn.snipt.sock"
daemon = True                    # Whether work in the background
debug = False                    # Some extra logging
logfile = ".gunicorn.log"        # Name of the log file
loglevel = "info"                # The level at which to log
pidfile = ".gunicorn.pid"        # Path to a PID file
workers = 1                      # Number of workers to initialize
umask = 0                        # Umask to set when daemonizing
user = None                      # Change process owner to user
group = None                     # Change process group to group
proc_name = "gunicorn-snipt"    # Change the process name
tmp_upload_dir = None            # Set path used to store temporary uploads


def post_fork(server, worker):
    server.log.info("Worker spawned (pid: %s)" % worker.pid)
    
    import local_settings, monitor
    if local_settings.DEBUG:
        server.log.info("Starting change monitor.")
        monitor.start(interval=1.0)

