FROM 8675309/ffmpy

RUN apt-get -y update && apt-get install -y python3

ADD fridaysborbot /usr/src/app/fridaysborbot
WORKDIR /usr/src/app/fridaysborbot

RUN pip install -r requirements.txt

CMD ["python", "./SborBot.py"]