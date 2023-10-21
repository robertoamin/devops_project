#!/bin/bash
sudo su
source /var/app/venv/staging-LQM1lest/bin/activate
cd /var/app/current
python -m blacklist.manage create_db