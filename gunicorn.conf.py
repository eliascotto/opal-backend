# -*- coding: utf-8 -*-
bind = "0.0.0.0:5000"
workers = 2
# Uvicorn's Gunicorn worker class
worker_class = "uvicorn.workers.UvicornWorker"
