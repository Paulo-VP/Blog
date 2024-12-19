FROM ubuntu:24.04
WORKDIR /app
ADD ./app_blog .
ADD ./requirements.txt .
RUN apt update && \
    apt install python3 python3-pip python3-venv -y && \
    apt install supervisor && \
    apt install nginx -y && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*
ADD ./flaskapp /etc/nginx/sites-available/.
RUN ln -s /etc/nginx/sites-available/flaskapp /etc/nginx/sites-enabled/
RUN python3 -m venv .venv
ENV PATH="/app/.venv/bin:$PATH"
RUN pip install -r requirements.txt
ADD supervisord.conf /etc/supervisor/supervisord.conf
EXPOSE 8080
CMD ["/usr/bin/supervisord"]