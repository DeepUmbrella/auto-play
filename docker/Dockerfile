FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \ 
  build-essential \
  libpcre3 \
  libpcre3-dev \
  libssl-dev \
  zlib1g-dev \
  wget \
  git \
  && rm -rf /var/lib/apt/lists/*
# download and install nginx-rtmp-module
RUN wget http://nginx.org/download/nginx-1.24.0.tar.gz -O /tmp/nginx.tar.gz \
  && tar -zxvf /tmp/nginx.tar.gz -C /tmp \
  && git clone https://github.com/arut/nginx-rtmp-module.git /tmp/nginx-rtmp-module \
  && cd /tmp/nginx-1.24.0 \
  && ./configure --add-module=/tmp/nginx-rtmp-module --with-http_ssl_module \
  && make \
  && make install \
  && mkdir -p /usr/local/nginx/conf \
  && mv /usr/local/nginx/sbin/nginx /usr/sbin/nginx \
  && rm -rf /tmp/*

COPY nginx.conf /usr/local/nginx/conf/nginx.conf

EXPOSE 1935
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]