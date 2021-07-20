FROM alpine:3.14

# Update and install postgresql-client (include psql)
RUN apk update \
    && apk upgrade \
    && apk add --no-cache postgresql-client

# Copy entry.sh and add permmision of execute
COPY entry.sh entry.sh
RUN chmod 755 ./entry.sh

CMD ["./entry.sh"]
