FROM docker.io/library/postgres:16.2
COPY init/* /docker-entrypoint-initdb.d
ENV POSTGRES_PASSWORD=mysecretpassword
EXPOSE 5432

# I made an attempt to store the data inside the image, that is, run the
# initialization scripts on image creation, since all the data really is
# "static" in that it never changes. But this turned out to be a futile
# attempt, and so this image is now just a wrapper around postgres, that
# contains the database schema creation files in the initialization directory.

# Old comments from this attempt is below, but they probably aren't worth
# keeping

# -----------------------

# Initialize the database folder, then run startup which runs our
# initialization scripts (which fills the database with our data)
# and stop the running server, to prevent the image creation process
# to complete
# Now, when we run the server, it already has all the data loaded
#     trap '' SIGTERM && \
#STOPSIGNAL SIGTERM

# this runs the SQL COPY commands, and afterwards, /var/lib/postgresql/data
# is ~140 MB (default clean is 39MB) - but when COPYing the folder below,
# nothing seems to be copied

# /var/lib/postgresql/data is a VOLUME (!)
# this has implications - meaning nothing will be stored there, it seems!
#RUN set -eux && \
#    (timeout 8s /usr/local/bin/docker-entrypoint.sh postgres || exit 0) && \
#    du -sh /var/lib/postgresql

#RUN du -sh /var/lib/postgresql
# du -sh /var/lib/postgresql/data
#     gosu postgres pg_ctl start -w && \
# RUN set -eux && \
#     chmod +x /wait_for_creation.sh && \
#     /wait_for_creation.sh
#RUN set -eux && \
#    /usr/local/bin/docker-entrypoint.sh
#RUN gosu postgres pg_ctl status

#FROM docker.io/library/postgres:16.2
#COPY --from=builder /var/lib/postgresql /var/lib/postgresql

# this is 4k
#RUN du -sh /var/lib/postgresql

#ENV POSTGRES_PASSWORD=mysecretpassword
# this may or may not be secure. On the one hand, the container app will
# not allow external access (public internet), but only connections that
# come from within the same VNET or the same container app environment,
# so exposing a dummy password here may in fact be totally ok.
# On the other hand, you never know, you know..
#ENV PGDATA=/var/lib/postgresql/data
#RUN /usr/local/bin/docker-ensure-initdb.sh
#ENTRYPOINT [ "/usr/local/bin/docker-entrypoint.sh" ]
#CMD [ "postgres" ]
