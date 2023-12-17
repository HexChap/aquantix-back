FROM nginx/unit:1.29.0-python3.11

COPY ./config/config.json /docker-entrypoint.d/config.json
COPY ./config/application_default_credentials.json /gcp/creds.json
ENV GOOGLE_APPLICATION_CREDENTIALS=/gcp/creds.json
ENV GOOGLE_CLOUD_PROJECT=root-opus-408218

RUN mkdir build
COPY . ./build
RUN cd ./build
RUN ls
RUN apt update && apt install -y python3-pip                                  \
    && pip3 install -r /build/requirements.txt                               \
    && apt remove -y python3-pip                                              \
    && apt autoremove --purge -y                                              \
    && rm -rf /var/lib/apt/lists/* /etc/apt/sources.list.d/*.list

EXPOSE 8000
