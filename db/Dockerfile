FROM docker.io/library/postgres:16.2

COPY init/* /docker-entrypoint-initdb.d

# Initialize the database folder, then run startup which runs our
# initialization scripts (which fills the database with our data)
# and stop the running server, to prevent the image creation process
# to complete
# Now, when we run the server, it already has all the data loaded
RUN set -eux && \
    gosu postgres pg_ctl init && \
    gosu postgres pg_ctl start && \
    gosu postgres pg_ctl stop


# TODO the step above can be a builder layer, to prevent storing the files
# in the image twice (1 copy in our files, 1 copy in the database)
