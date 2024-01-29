ARG FROM_SRC=amd64/ubuntu:22.04

FROM ${FROM_SRC}

ENV MINICONDA_SRC https://repo.anaconda.com/miniconda/Miniconda3-py310_23.9.0-0-Linux-x86_64.sh
ENV USER exp_user
ENV CONDA_DIR /home/$USER/apps/miniconda
ENV ROOT_PWD root
ENV PATH=$CONDA_DIR/bin:$PATH

# # -- Layer: OS 
RUN apt update && \
    apt install -y wget && \
    apt install -y curl && \
    apt install -y gcc && \
    apt install -y cmake && \
    apt install -y make && \
    apt install -y bzip2 && \
    apt install -y vim && \
    apt install -y unzip

# -- Layer : User
RUN echo "root:$ROOT_PWD" | chpasswd && \
    useradd -ms /bin/bash $USER

# -- Switch to $USER user
USER $USER

WORKDIR /home/$USER

# -- Layer : Conda
RUN mkdir /home/$USER/apps && \
    wget --quiet $MINICONDA_SRC -O miniconda.sh && \
    chmod +x miniconda.sh && \
    bash miniconda.sh -b -p $CONDA_DIR && \
    rm miniconda.sh && \
    conda init bash && \
    echo ". $CONDA_DIR/etc/profile.d/conda.sh" >> ~/.profile && \
    echo "export PATH=$CONDA_DIR/bin:$PATH" >> $HOME/.bashrc && \
    echo "conda activate base" >> $HOME/.bashrc

# -- Layer : Python Packages
RUN conda update --name base --channel defaults conda && \
    conda install -y python=3.10 && \
    conda install -y scikit-learn=1.3.0 && \
    conda install -y matplotlib=3.7.2 && \
    conda install -y pandas=2.0.3 && \
    conda install -y conda-build=3.27.0 && \
    conda install -y pip && \
    pip install --upgrade pip && \
    pip install river==0.18.0 && \
    pip install numpy==1.25.2 && \
    pip install paho-mqtt==1.6.1

# -- Layer : src and data files
RUN mkdir -p /home/$USER/src/python

COPY ./src/python /home/$USER/src/python
RUN conda develop /home/$USER/src/python/mqtt_client_decode_temp
RUN cd /home/$USER/src/python/mqtt_client_decode_temp

# -- Runtime
CMD ["bash"]
