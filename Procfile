web: gunicorn --worker-tmp-dir /dev/shm --config gunicorn.conf.py app:app --host=0.0.0.0 --port=${PORT:-5000}
