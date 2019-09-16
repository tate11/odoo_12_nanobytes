FROM registry2.nanobytes.es/odoo_12_ee:latest
MAINTAINER Nanobytes Informática y Telecomunicaciones <soporte@nanobytes.es>

RUN set -x; \
        apt-get update \
        && apt-get install -y --no-install-recommends \
            python3-dev \
            build-essential \
            libssl-dev \
            libffi-dev \
            libxml2-dev \
            libxslt1-dev \
            zlib1g-dev \
        && rm -rf /var/lib/apt/lists/*

COPY . /mnt/extra-addons/

RUN pip3 install -r /mnt/extra-addons/requirements.txt