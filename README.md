# DuoTalk

## Getting Started

``` shell
# Build image
docker build -t tts .

# Run with GPU
docker run --gpus all -v ./.shared:/app -it tts
```