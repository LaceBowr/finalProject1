# finalProject1
python for the finalProject for graduation from BYUI


NOTES on building and running the docker:

fire up shell somewhere to do this

from the directory with the Dockerfile (this directory) run:

docker build . -t finalProject
 
and then run the container in interactive mode:

docker run -it -p 5000:5000 finalproject

For that to work the build command must have succeeded, otherwise you are running an old version of the container.  So make sure you save your docker file and that the build command runs first
