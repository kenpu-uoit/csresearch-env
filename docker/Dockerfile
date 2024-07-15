FROM nvidia/cuda:12.2.2-devel-ubuntu22.04
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
SHELL ["/bin/bash", "-ec"]
ENV DEBIAN_FRONTEND=noninteractive

#
# Core UNIX
#
RUN apt-get update && \
    apt-get upgrade --yes && \
    apt-get install --yes --no-install-recommends \
    build-essential \
    curl \
    git \
    htop \
    less \
    ack \
    locales \
    openssh-client \
    openssh-server \
    sudo \
    tmux \
    tree \
    tzdata \
    unzip \
    wget \
    ffmpeg \
    openjdk-21-jdk-headless \
    postgresql-client-14 \
    vim && \
    echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen && \
    rm -f /etc/localtime && \
    ln -s /usr/share/zoneinfo/America/Toronto /etc/localtime

# Latex
# https://github.com/mingchen/docker-latex/

RUN apt-get update -q && \
    apt-get install -y -qq --no-install-recommends \
        ca-certificates  \
        curl \
        ghostscript \
        git \
        gnuplot \
        imagemagick \
        make \
        jq \
        qpdf \
        python3-pygments \
        wget \
        vim-tiny && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /texlive

COPY install-texlive.sh .
COPY texlive.profile .
RUN chmod +x install-texlive.sh && \
    ./install-texlive.sh

#
# Core Python
#

ARG MINICONDA_DOWNLOAD=Miniconda3-py312_24.4.0-0-Linux-x86_64.sh
ENV PATH=/opt/miniconda3/bin:$PATH
RUN wget https://repo.anaconda.com/miniconda/$MINICONDA_DOWNLOAD && \
    bash ./$MINICONDA_DOWNLOAD -p /opt/miniconda3 -s -b && \
    rm -f ./$MINICONDA_DOWNLOAD

#
# Quarto
#
ENV QUARTO_VERSION=1.5.40
RUN cd /tmp \
    && wget https://github.com/quarto-dev/quarto-cli/releases/download/v${QUARTO_VERSION}/quarto-${QUARTO_VERSION}-linux-amd64.tar.gz \
    && tar -C /opt -xzf quarto-${QUARTO_VERSION}-linux-amd64.tar.gz \
    && ln -s /opt/quarto-${QUARTO_VERSION}/bin/quarto /bin/quarto \
    && rm -f quarto-${QUARTO_VERSION}-linux-amd64.tar.gz

RUN pip install --upgrade \
    nbconvert==7.16.4 \
    mistune==2.0.4
RUN quarto install tinytex
RUN quarto install chrome

#
# Github integration
RUN conda install -y --channel conda-forge git-lfs=3.4.0 gh=2.37.0

#
# Data Science
#
RUN pip install \
    altair==5.3.0 \
    beautifulsoup4==4.12.3 \
    bokeh==3.4.1 \
    Bottleneck==1.3.8 \
    cloudpickle==3.0.0 \
    Cython==3.0.10 \
    dask==2024.5.2 \
    dill==0.3.8 \
    h5py==3.11.0 \
    ipympl==0.9.4 \
    ipywidgets==8.1.3 \
    matplotlib==3.9.0 \
    numba==0.59.1 \
    numexpr==2.10.0 \
    pandas==2.2.2 \
    scikit-image==0.23.2 \
    scikit-learn==1.5.0 \
    scipy==1.13.1 \
    seaborn==0.13.2 \
    SQLAlchemy==2.0.30 \
    statsmodels==0.14.2 \
    sympy==1.12.1 \
    tqdm==4.66.4 \
    widgetsnbextension==4.0.11 \
    xlrd==2.0.1 \
    pydantic==2.7.3

#
# PyTorch
#
RUN pip install \
    torch==2.3.0 \
    torchaudio==2.3.0 \
    torchmetrics==1.4.0 \
    torchtext==0.18.0 \
    torchvision==0.18.0

RUN pip install lightning==2.2.5

#
# Huggingface
#
RUN pip install \
    transformers==4.41.2 \
    accelerate==0.30.1 \
    bitsandbytes==0.43.1 \
    datasets==2.19.2 \
    evaluate==0.4.2 \
    peft==0.11.1 \
    safetensors==0.4.3 \
    tensorboard==2.16.2 \
    trl==0.8.6 \
    wandb==0.17.0 \
    xformers==0.0.26.post1

RUN pip install flash-attn==2.5.9.post1 --no-build-isolation

# NLP tools
RUN pip install \
    sentencepiece==0.2.0 \
    tiktoken==0.7.0 \
    py7zr==0.21.0 \
    nltk==3.8.1 \
    rouge-score==0.1.2 \
    textual==0.64.0 \
    PyMuPDF==1.24.5 \
    InstructorEmbedding==1.0.1 \
    colbert-ai==0.2.19

# embedding models
#RUN conda install -c conda-forge faiss-gpu
RUN conda install -c pytorch/label/nightly -c nvidia faiss-gpu=1.7.4

#
# Audio related
#
RUN pip install soundfile==0.12.1

# VSCode Jupyter support
RUN pip install ipykernel ipywidgets

# Postgres
RUN pip install psycopg2-binary==2.9.9

# LLM
RUN pip install \
    ollama==0.2.1 \
    openai==1.35.13 \
    llama-index==0.10.55 \
    langchain==0.2.7

#
# Post installation configuration
#
WORKDIR /
COPY ./start.sh ./createuser.sh ./createusers /bin/
COPY ./users.default /etc
COPY ./bash.bashrc /etc/bash.bashrc
CMD /bin/start.sh
