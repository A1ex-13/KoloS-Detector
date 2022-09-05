FROM tiangolo/uwsgi-nginx-flask:python3.8

COPY ./requirements.txt /app/
RUN python3 -m pip install --upgrade -r /app/requirements.txt

COPY . /app/

EXPOSE 5000

CMD [ "python3", "-m", "flask", "run" ]
