# Use the official PostgreSQL image as the base image
FROM postgres:17

# Install PostgreSQL extensions
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-17-pgvector \
        postgresql-17-cron \
        postgresql-17-postgis \
    && rm -rf /var/lib/apt/lists/*

# Optionally, you can include custom initialization scripts
# COPY init.sql /docker-entrypoint-initdb.d/

# Expose the PostgreSQL port
EXPOSE 5432



