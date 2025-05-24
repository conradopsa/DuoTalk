# DuoTalk

## Getting Started

``` shell
conda create --name duotalk python=3.11

conda activate duotalk

# Build image
docker build -t tts .

# Run with GPU
docker run --gpus all -v ./.shared:/app -it tts
```