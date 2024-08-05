FROM public.ecr.aws/unocha/python:3.12-stable

WORKDIR /srv/hapi

COPY . .

RUN apk add \
    postgresql-dev && \
    apk --virtual .build-deps add \
    git \
    build-base \
    python3-dev && \
    mkdir -p \
    /var/log/hwa && \
    pip3 install --upgrade -r requirements.txt && \
    apk del .build-deps && \
    rm -rf /var/lib/apk/* && rm -r /root/.cache

ENTRYPOINT /usr/bin/python

CMD []
