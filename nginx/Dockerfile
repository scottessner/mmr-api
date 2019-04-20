FROM nginx:1.15.3
RUN rm /etc/nginx/nginx.conf
COPY nginx.conf /etc/nginx/
RUN rm /etc/nginx/conf.d/default.conf
COPY ../mmr-api.conf /etc/nginx/conf.d/

RUN mkdir -p /app/build/mmr
COPY build /app/build/mmr