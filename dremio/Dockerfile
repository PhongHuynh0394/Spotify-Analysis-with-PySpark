FROM dremio/dremio-oss

USER root

# add python
RUN apt-get update && \
    apt-get install -y python3 python3-pip

COPY . .

RUN chmod +x ./init.bash

CMD ["bash", "init.bash"]
