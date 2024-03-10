# finalProject1
python for the finalProject for graduation from BYUI


NOTES on building and running the docker:

fire up shell somewhere to do this

from the directory with the Dockerfile (this directory) run:

docker build . -t finalproject
 
and then run the container in interactive mode:

docker run -it -p 5000:5000 finalproject

For that to work the build command must have succeeded, otherwise you are running an old version of the container.  So make sure you save your docker file and that the build command runs first

To update and push to ECR for the deployed service:

 aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 211125642163.dkr.ecr.us-east-2.amazonaws.com

 docker build -t wreckage-webservice . 

 docker tag wreckage-webservice:latest 211125642163.dkr.ecr.us-east-2.amazonaws.com/wreckage-webservice:latest

 docker push 211125642163.dkr.ecr.us-east-2.amazonaws.com/wreckage-webservice:latest 

To run locally you must run:

docker run -it -p 5000:5000 -e AWS_ACCESS_KEY_ID="<access_key_id_for_user>" -e AWS_SECRET_ACCESS_KEY="<access_key_for_user>"

Get these from your local .aws credentials file or from the iam console in aws

Reminder to myself Local db userpwcombo on my dev host is serviceaccount/test1234
