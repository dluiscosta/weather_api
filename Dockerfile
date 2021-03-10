FROM python:3.9

# initiate virtualenv with dependencies
COPY Pipfile .
COPY Pipfile.lock .
RUN pip install pipenv
ARG PIPENV_INSTALL_PARAMS=""
RUN pipenv install \
    --deploy --ignore-pipfile ${PIPENV_INSTALL_PARAMS}

# bring source code to container
RUN mkdir /app/
COPY /app/ /app/
WORKDIR /app/
