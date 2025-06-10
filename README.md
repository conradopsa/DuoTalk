# DuoTalk

## Best Usage on Android

After generated your audios, transfer files to your phone and activate the lyrics.

Its recommended to use Musicolet App for Android, see below:

https://github.com/user-attachments/assets/115ae197-0d21-470b-a5b5-6bfafe26f80f

Obs.: Some USBC to P3 adapter with DAC can cut 2s in each audio start, so prefer other alternatives like direct USB phone, bluetooth or native phone audio. On PC Linux, this  isn't a problem.

## Best Usage on Linux

Use [Lollypop](https://wiki.gnome.org/Apps/Lollypop) Player and activate Lyrics.


## Getting Started
``` shell
# 1. Create and/or activate env with python 3.11
conda create --name duotalk python=3.11
conda activate duotalk

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run (needs CUDA GPU)
python src input/halflife.txt --speaker atlas

# 4. Check 'audios' folder
```

## List speakers

``` shell
ls samples
# atlas.wav  gaia.wav  uranos.wav
```

## Run with Docker
``` shell
# Build image
docker build -t tts .

# Run with GPU
docker run --gpus all -v ./.shared:/app -it tts
```

## Start tests
``` shell
# Start test with makefile
make test
```
