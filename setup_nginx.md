Nginx compatible

Example uses the following:

* Mayannah app for framework
* nginx to serve app
* postgresql for database

1. Setup Nginx docker

```script
# Create a Docker Network
$ docker network create --driver bridge mayannah
# Pull nginx image
$ docker pull nginx:latest
# Create nginx with volume to place configuration files
$ docker run --name nginx \
             --network mayannah \
             -p 80:80 \
             -p 8000:8000 \
             # Volume to place configurations
             -v $PWD:/etc/nginx/conf.d \
             -d nginx:latest
```

2. Create NGINX conf file

Add `mayannah.example.com` in `/etc/hosts`

```script
server {
    listen 80;
    server_name mayannah.example.com;

    location / {
        proxy_pass http://mayannah:8000;
        proxy_http_version 1.1;
        proxy_set_header Host $http_host;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

1. Setup Database

```script
$ docker run --name mayannah_db \
             -e POSTGRES_PASSWORD=postgres \
             --network mayannah \
             -d postgres:latest
# Create database
$ docker exec -it mayannah_db psql -U postgres
postgres=# CREATE DATABASE mayannah;
postgres=# \q
```

1. Setup Application

```script
$ docker --name mayannah \
         --network mayannah \
         -d mayannah
# Run database migration
$ docker exec -it mayannah python manage.py migrate
```

1. Update nginx

```script
$ docker exec -it nginx bash
# Test if mayannah conf is working
$ nginx -t
# reload nginx
$ nginx -s reload
```

1. Open browser `mayannah.example.com`
