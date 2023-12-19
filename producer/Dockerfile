FROM python:3.11


#Labels as key value pair
LABEL Maintainer="jfp"


# Any working directory can be chosen as per choice like '/' or '/home' etc
# i have chosen /usr/app/src
WORKDIR /usr/app/src

#to COPY the remote file at working directory in container
COPY entities.py ./
COPY trade_feed.py ./
COPY requirements.txt ./

# Now the structure looks like this '/usr/app/src/test.py'

RUN pip install pip install -r requirements.txt 
#CMD instruction should be used to run the software
#contained by your image, along with any arguments.

CMD [ "python", "./trade_feed.py"]