ARG IMAGE_VARIANT=slim-buster
ARG OPENJDK_VERSION=11
ARG PYTHON_VERSION=3.11.0

FROM python:${PYTHON_VERSION}-${IMAGE_VARIANT} AS py3
FROM openjdk:${OPENJDK_VERSION}-${IMAGE_VARIANT}

COPY --from=py3 / /

WORKDIR /opt/prefect
COPY requirements.txt .
RUN pip install -r requirements.txt --trusted-host pypi.python.org --no-cache-dir

COPY flows /opt/prefect/flows

# Run our flow script when the container starts
CMD ["python", "flows/main_flow.py"]
