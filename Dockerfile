FROM python:3.6.1

ADD ./mayannah /mayannah
COPY ./entrypoint.sh /mayannah/
WORKDIR /mayannah
RUN pip install -r requirements.txt
EXPOSE 8000
ENV DJANGO_SETTINGS_MODULE config.settings.prod
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
#CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config:wsgi:application"]
#CMD "gunicorn --bind 0.0.0.0:8000 config.wsgi:application"
RUN ["chmod", "+x", "/mayannah/entrypoint.sh"]
ENTRYPOINT ["sh","/mayannah/entrypoint.sh"]
