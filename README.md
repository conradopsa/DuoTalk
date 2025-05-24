# DuoTalk

## Getting Started

``` shell
conda create --name duotalk python=3.11

conda activate duotalk

pip install -r requirements.txt

python ./src

# Build image
docker build -t tts .

# Run with GPU
docker run --gpus all -v ./.shared:/app -it tts
```