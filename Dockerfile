FROM alpine:3.20.0

ENV TZ=Europe/Paris

RUN apk update && apk add --no-cache tzdata curl wget python3 py3-pip
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN mkdir -m 0777 -p /root/.config/pip && echo "[global]" > /root/.config/pip/pip.conf && echo "break-system-packages = true" >> /root/.config/pip/pip.conf
RUN pip install requests pyyaml

COPY ./root /
RUN chmod a+x /start/*.sh

VOLUME /config

CMD ["/start/start.sh"]