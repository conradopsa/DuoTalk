FROM nvidia/cuda:12.2.0-base-ubuntu22.04

RUN apt-get update && \
    apt-get install -y --allow-unauthenticated --no-install-recommends \
    wget \
    git \
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

ENV HOME="/root"
ENV CONDA_DIR="${HOME}/miniconda"
ENV PATH="$CONDA_DIR/bin":$PATH
ENV CONDA_AUTO_UPDATE_CONDA=false
ENV PIP_DOWNLOAD_CACHE="$HOME/.pip/cache"
ENV TORTOISE_MODELS_DIR="$HOME/tortoise-tts/build/lib/tortoise/models"

RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /tmp/miniconda3.sh \
    && bash /tmp/miniconda3.sh -b -p "${CONDA_DIR}" -f -u \
    && "${CONDA_DIR}/bin/conda" init bash \
    && rm -f /tmp/miniconda3.sh \
    && echo ". '${CONDA_DIR}/etc/profile.d/conda.sh'" >> "${HOME}/.profile"

# --login option used to source bashrc (thus activating conda env) at every RUN statement
SHELL ["/bin/bash", "--login", "-c"]

RUN conda create --name tortoise python=3.9 numba inflect -y \
    && conda activate tortoise \
    && conda install --yes pytorch==2.2.2 torchvision==0.17.2 torchaudio==2.2.2 pytorch-cuda=12.1 -c pytorch -c nvidia \
    && conda install --yes transformers=4.31.0 

RUN git clone https://github.com/neonbjb/tortoise-tts.git

# RUN conda activate tortoise \
#     && pip install --progress-bar=raw -v https://files.pythonhosted.org/packages/35/f5/d0ad1a96f80962ba65e2ce1de6a1e59edecd1f0a7b55990ed208848012e0/scipy-1.13.1-cp39-cp39-manylinux_2_17_x86_64.manylinux2014_x86_64.whl

# RUN conda activate tortoise \
#     && conda install --yes scipy==1.13.1 

RUN conda activate tortoise \
    && pip install --progress-bar=raw -v scipy==1.13.1 -i https://pypi.tuna.tsinghua.edu.cn/simple
    
# COPY ./scipy-1.13.1-cp39-cp39-manylinux_2_17_x86_64.manylinux2014_x86_64.whl scipy-1.13.1-cp39-cp39-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
# RUN pip install ./scipy-1.13.1-cp39-cp39-manylinux_2_17_x86_64.manylinux2014_x86_64.whl

RUN cd ./tortoise-tts \
    && conda activate tortoise \
    && sed -i 's/tokenizers[^*]*/tokenizers==0.13.3/' requirements.txt \
    # && sed -i '/^tokenizers*/d' requirements.txt \
    # && echo "tokenizers==0.13.3" >> requirements.txt \
    && sed -i 's/tokenizers[^'"'"'"]*/tokenizers==0.13.3/' setup.py \
    && pip install .


RUN pip config set global.timeout 120 \
    && pip config set global.retries 5 \
    && pip config set global.extra-index-url "https://pypi.tuna.tsinghua.edu.cn/simple/" \
    && pip config set global.trusted-host "pypi.org pypi.tuna.tsinghua.edu.cn"

RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    python3-dev \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Install PyTorch with CUDA 12.2 support
RUN conda activate tortoise && \
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

COPY . /app

RUN cd ./app \
    && conda activate tortoise \
    && pip install -r requirements.txt --only-binary=:all:
    # && python run main.py

# RUN cd ./app \
#      && conda activate tortoise \
#      && python main.py || true

     