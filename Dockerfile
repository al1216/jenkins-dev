FROM jenkins/jenkins:2.462.3-jdk17

USER root

# Install required system dependencies and Docker CLI
RUN apt-get update && apt-get install -y lsb-release python3-pip curl \
  && curl -fsSLo /usr/share/keyrings/docker-archive-keyring.asc \
     https://download.docker.com/linux/debian/gpg \
  && echo "deb [arch=$(dpkg --print-architecture) \
     signed-by=/usr/share/keyrings/docker-archive-keyring.asc] \
     https://download.docker.com/linux/debian \
     $(lsb_release -cs) stable" > /etc/apt/sources.list.d/docker.list \
  && apt-get update && apt-get install -y docker-ce-cli \
  && apt-get clean && rm -rf /var/lib/apt/lists/*

USER jenkins

# Install plugins (versions verified on Jenkins 2.462.x)
RUN jenkins-plugin-cli --plugins \
  "blueocean docker-workflow workflow-aggregator docker-plugin"