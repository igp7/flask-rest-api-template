###########
#   BASE  #
###########
FROM python:3.8-alpine as base

RUN apk update && \
    apk upgrade

###########
# BUILDER #
###########
# Pull official base image
FROM base as builder

# Set work directory
WORKDIR /usr/src/app

# Install system dependencies
RUN apk add --no-cache build-base postgresql-dev gcc musl-dev

# Install python dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN python -OO -m pip wheel --no-cache-dir --wheel-dir=/usr/src/app/wheels -r requirements.txt

#########
# FINAL #
#########
# Pull official base image
FROM base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create directory for the app user
RUN mkdir -p /home/app

# Create the app user
RUN addgroup -g 1000 app && adduser -u 1000 -G app -h /home/app -D app

# Create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/api
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

# Install dependencies
RUN apk add --no-cache libpq
COPY --from=builder /usr/src/app/wheels /wheels
RUN pip install --upgrade pip
RUN python -m pip install --no-cache --no-index /wheels/*
RUN rm -rf /wheels

# Copy project
COPY . $APP_HOME

# Chown all the files to the app user
RUN chown -R app:app $APP_HOME

# Change to the app user
USER app

# Chmod to entrypoint.sh
RUN chmod +x ./entrypoint.sh

# Run entrypoint.sh
ENTRYPOINT ["/home/app/api/entrypoint.sh"]