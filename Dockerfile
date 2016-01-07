FROM python:2.7

# libmemcached-dev is required by pip package, but libmemcache doesn't work for
# me, using regular memcached
# kobocat needs java, otherwise "Survey Publishing failed: pyxform odk validate dependency: java not found"
RUN apt-get update && apt-get install -y unzip python-gdal memcached libmemcached-dev default-jre-headless

ADD https://github.com/kimetrica/kobocat/archive/master.zip /master.zip

RUN unzip master.zip && mv kobocat-master kobocat

WORKDIR /kobocat

RUN pip install -r requirements/base.pip -r requirements/dev.pip python-memcached

RUN useradd --create-home kobocat
RUN chown -R kobocat.kobocat /kobocat
USER kobocat

# ADDing modified production_example settings to use dockerized mongo & PSQL
ADD kimetrica_settings.py /kobocat/onadata/settings/kimetrica_settings.py
ENV DJANGO_SETTINGS_MODULE onadata.settings.kimetrica_settings

CMD python manage.py runserver 0.0.0.0:9000
