FROM cloudhelper/python3:latest
MAINTAINER Sun <wenhaijie@cloudhelper.xyz>

WORKDIR /opt/cloudhelper
RUN useradd cloudhelper

COPY . /opt/cloudhelper

RUN cd /opt/cloudhelper/requirements && yum -y install $(cat rpm_requirements.txt)

RUN cd /opt/cloudhelper/requirements && pip3 --default-timeout=1000 install --upgrade pip setuptools \
    && pip3 install -r requirements.txt \
    || pip3 install -i https://mirrors.aliyun.com/pypi/simple/ -r requirements.txt

# 安装gunicorn
RUN pip3 install gunicorn || pip3 install -i https://mirrors.aliyun.com/pypi/simple/ gunicorn
RUN ln -s /usr/local/python3/bin/gunicorn /usr/bin/gunicorn
RUN ln -s /usr/local/python3/bin/celery /usr/bin/celery

VOLUME /opt/cloudhelper/data
VOLUME /opt/cloudhelper/logs

EXPOSE 80
EXPOSE 8080
ENTRYPOINT ["./entrypoint.sh"]