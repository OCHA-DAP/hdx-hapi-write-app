FROM public.ecr.aws/unocha/python:3-base

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
    pip3 --no-cache-dir install --upgrade \
        pip \
        wheel && \
    pip3 install --upgrade -r requirements.txt && \
    apk del .build-deps && \
    rm -rf /var/lib/apk/* && rm -r /root/.cache

RUN ln -sf /usr/bin/python3 /usr/bin/python

ENTRYPOINT /usr/bin/python

CMD []
