FROM node:16.17.0-slim

ENV workdir /app

RUN mkdir ${workdir}
WORKDIR ${workdir}

ENV PATH="${workdir}/node_modules/.bin:${PATH}"

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git

RUN git clone https://github.com/karrioapi/quicktype.git /quicktype && \
    cd /quicktype && \
    yarn; \
    echo "done"
