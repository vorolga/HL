FROM python:3

COPY httptest /var/www/html/httptest
COPY . .

EXPOSE 80

CMD python3 main.py