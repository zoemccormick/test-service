FROM centos:7

ARG PYTHON_VERSION=3

RUN yum install -y epel-release && \
    yum update -y && \
    yum install -y python-pip wget bzip2 gcc-c++

RUN echo 'export PATH=/opt/conda/bin:$PATH' > /etc/profile.d/conda.sh && \
    wget --quiet -O conda.sh https://repo.continuum.io/miniconda/Miniconda$PYTHON_VERSION-latest-Linux-x86_64.sh && \
    bash conda.sh -b -p /opt/conda

ENV PATH="/opt/conda/bin:${PATH}"

WORKDIR /opt/services/test/

RUN pip install flask kazoo pyyaml msgpack==0.5.4 msgpack-python==0.5.4

COPY ./test_service /opt/services/test/test_service
COPY ./setup.py /opt/services/test/

RUN cd /opt/services/test/ && \
    python setup.py install

EXPOSE 3000

CMD cd && test-start
