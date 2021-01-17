# rspoc

#### In AWS console:
- ec2 launch: free t3.micro server, ubuntu 2004
- add 8080 access to incoming traffic in SG
- create bucket "rsdemo1" in eu-west-1, public access

#### Set up docker & add sudo to jenkins and run:
```apt update && apt install docker.io
docker pull jenkins/jenkins
docker build . -t jenkins:sudo -f Dockerfile
docker run -d -v /var/run/docker.sock:/var/run/docker.sock -v $(which docker):/usr/bin/docker -v jenkins_home:/var/jenkins_home -p 8080:8080 -p 50000:50000 jenkins:sudo
```

##### optional: use Dockerfile,plugins.txt to install standard set of plugins
- Pipeline Utility, Pipeline Steps for AWS plugin, Blue Ocean

#### Add deploy key to Github repo - for jenkins ssh:
```
$ ssh-keygen -t ed25519 -C "your_email@example.com"
```

#### Add creds to Jenkins: ssh, aws ...

