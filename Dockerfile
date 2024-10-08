FROM python:3.10.12

WORKDIR /var/www/html/monitorZKH

COPY . /var/www/html/monitorZKH

RUN ls -la /var/www/html/monitorZKH/*

RUN ls -la /var/www/html/monitorZKH/utils/*

RUN pip install -r requirements.txt

RUN apt-get update && apt-get install -y libodbc1

EXPOSE 8503

HEALTHCHECK CMD curl -f http://localhost:8503/_stcore/health || exit 1

ENTRYPOINT ["streamlit", "run", "Монитор_ЖКХ.py", "--server.port=8503", "--server.address=0.0.0.0"]

ENV  PYTHONPATH="/var/www/html/monitorZKH:/var/www/html/monitorZKH/utils"