# Dockerfile for Apache Spark
FROM openjdk:8-jre-alpine

# Install dependencies
RUN apk add --no-cache \
    bash \
    curl \
    tar \
    && curl -O https://downloads.apache.org/spark/spark-3.4.0/spark-3.4.0-bin-hadoop3.2.tgz \
    && tar -xzf spark-3.4.0-bin-hadoop3.2.tgz \
    && mv spark-3.4.0-bin-hadoop3.2 /opt/spark \
    && rm spark-3.4.0-bin-hadoop3.2.tgz

# Set environment variables
ENV SPARK_HOME=/opt/spark
ENV PATH=$SPARK_HOME/bin:$PATH

# Expose Spark ports
EXPOSE 7077 8080

# Start Spark master (this can be replaced by a custom entrypoint if necessary)
CMD ["spark-class", "org.apache.spark.deploy.master.Master"]
