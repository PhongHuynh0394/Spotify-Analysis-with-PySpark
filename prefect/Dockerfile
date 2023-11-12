FROM prefecthq/prefect:2-python3.10 

RUN apt update 
RUN apt install -y default-jdk

ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64

# Add our requirements.txt file to the image and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip & pip install -r requirements.txt --trusted-host pypi.python.org --no-cache-dir

COPY flows /opt/prefect/flows

# Run our flow script when the container starts
CMD ["python", "flows/main_flow.py"]
