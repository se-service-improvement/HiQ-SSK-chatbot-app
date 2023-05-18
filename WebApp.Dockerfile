FROM node:20-alpine AS frontend  
RUN mkdir -p /home/node/app/node_modules && chown -R node:node /home/node/app

WORKDIR /home/node/app 
COPY ./frontend/package*.json ./  
USER node
RUN npm ci  
COPY --chown=node:node ./frontend/ .  
RUN npm run build
  
FROM python:3.9.7-alpine3.14  
RUN apk add --no-cache --virtual .build-deps \  
***REMOVED***build-base \  
***REMOVED***libffi-dev \  
***REMOVED***openssl-dev \  
***REMOVED***curl \  
***REMOVED***&& apk add --no-cache \  
***REMOVED***libpq \  
***REMOVED***&& pip install --no-cache-dir uwsgi  
  
COPY requirements.txt /usr/src/app/  
RUN pip install --no-cache-dir -r /usr/src/app/requirements.txt \  
***REMOVED***&& rm -rf /root/.cache  
  
COPY . /usr/src/app/  
COPY --from=frontend /home/node/app/  /usr/src/app/frontend/  
WORKDIR /usr/src/app  
EXPOSE 5000  
CMD ["uwsgi", "--http", ":5000", "--wsgi-file", "app.py", "--callable", "app", "--processes", "4", "--threads", "2", "--uid", "guest"]  
