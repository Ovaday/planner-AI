# base image
# sudo sudo yum update -y
#  sudo yum install git python docker pip
#sudo curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose

#sudo chmod +x /usr/local/bin/docker-compose

#docker-compose version
#sudo service docker start
#sudo systemctl enable docker
#sudo usermod -a -G docker ec2-user
# reload the concole
#docker info
FROM python:3.8
# setup environment variable
ENV DockerHOME=/home/ec2-user/planner-AI/docker

# set work directory
RUN mkdir -p $DockerHOME

# where your code lives
WORKDIR $DockerHOME

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip

# copy whole project to your docker home directory.
COPY . $DockerHOME
# run this command to install all dependencies
RUN pip install -r requirements.txt
# port where the Django app runs
EXPOSE 8000
# start server
CMD python manage.py qcluster