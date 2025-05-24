FROM nvidia/cuda:12.2.0-base-ubuntu22.04

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y --no-install-recommends gcc g++ make python3 python3-dev python3-pip python3-venv python3-wheel espeak-ng libsndfile1-dev && rm -rf /var/lib/apt/lists/*
RUN pip3 install llvmlite --ignore-installed

# Install Dependencies:
RUN pip3 install torch torchaudio --extra-index-url https://download.pytorch.org/whl/cu118
RUN rm -rf /root/.cache/pip

ENV CONDA_DIR="/root/miniconda"
ENV PATH="$CONDA_DIR/bin":$PATH
ENV CONDA_AUTO_UPDATE_CONDA=false

RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /tmp/miniconda3.sh \
    && bash /tmp/miniconda3.sh -b -p "${CONDA_DIR}" -f -u \
    && "${CONDA_DIR}/bin/conda" init bash \
    && rm -f /tmp/miniconda3.sh \
    && echo ". '${CONDA_DIR}/etc/profile.d/conda.sh'" >> "/root/.profile"

# --login option used to source bashrc (thus activating conda env) at every RUN statement
SHELL ["/bin/bash", "--login", "-c"]

# adding extra mirrors
RUN pip config set global.timeout 120 \
    && pip config set global.retries 5 \
    && pip config set global.extra-index-url "https://pypi.tuna.tsinghua.edu.cn/simple/" \
    && pip config set global.trusted-host "pypi.org pypi.tuna.tsinghua.edu.cn"

RUN conda create --name duotalk python=3.12 -y \
    && conda activate tortoise \
    && git clone https://github.com/archwesome/XTTS-v2.git XTTS-v2 \
    && RUN make install

RUN cd ./XTTS-v2 \
    && conda activate duotalk

ENTRYPOINT ["tts"]
CMD ["--help"]
   
