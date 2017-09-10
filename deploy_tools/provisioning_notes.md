Provisioning a new site
======================

## Required packages:

- nginx
- Python 3.6
- virutalenv + pip
- Git

## Nginx Virtual Host config:

- see nginx.template.conf
- replace SITENAME with staging.my-domain.com

##Systemd service

- see gunicorn-systemd.template.service
- replace SITENAME with staging.my-domain.com

