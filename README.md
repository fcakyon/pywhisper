<div align="center">
<h1>
  pywhisper
</h1>

<h4>
  <a href="https://github.com/openai/whisper/tree/5d8d3e75a4826fe5f01205d81c3017a805fc2bf9">openai/whisper</a> + extra features
</h4>

<div>
    <a href="https://badge.fury.io/py/pywhisper"><img src="https://badge.fury.io/py/pywhisper.svg" alt="pypi version"></a>
    <a href="https://pepy.tech/project/pywhisper"><img src="https://pepy.tech/badge/pywhisper" alt="downloads"></a>
    <a href="https://github.com/fcakyon/pywhisper/actions/workflows/ci.yml"><img src="https://github.com/fcakyon/yolov5-pip/actions/workflows/ci.yml/badge.svg" alt="ci testing"></a>
    <a href="https://github.com/fcakyon/pywhisper/actions/workflows/package_testing.yml"><img src="https://github.com/fcakyon/yolov5-pip/actions/workflows/package_testing.yml/badge.svg" alt="package testing"></a>
    <br>
    <br>
    
</div>
</div>

## extra features

- no need for ffmpeg cli installation, pip install is enough
- srt export
- progress bar for `transcribe`
- continious integration and package testing via github actions

## setup

```bash
pip install pywhisper
```

You may need [`rust`](http://rust-lang.org) installed as well, in case [tokenizers](https://pypi.org/project/tokenizers/) does not provide a pre-built wheel for your platform. If you see installation errors during the `pip install` command above, please follow the [Getting started page](https://www.rust-lang.org/learn/get-started) to install Rust development environment.

## command-line usage

The following command will transcribe speech in audio files, using the `medium` model:

    pywhisper audio.flac audio.mp3 audio.wav --model medium

The default setting (which selects the `small` model) works well for transcribing English. To transcribe an audio file containing non-English speech, you can specify the language using the `--language` option:

    pywhisper japanese.wav --language Japanese

Adding `--task translate` will translate the speech into English:

    pywhisper japanese.wav --language Japanese --task translate

Run the following to view all available options:

    pywhisper --help

See [tokenizer.py](pywhisper/tokenizer.py) for the list of all available languages.


## python usage

Transcription can also be performed within Python: 

```python
import pywhisper

model = pywhisper.load_model("base")
result = model.transcribe("audio.mp3")
print(result["text"])
```

Internally, the `transcribe()` method reads the entire file and processes the audio with a sliding 30-second window, performing autoregressive sequence-to-sequence predictions on each window.

Below is an example usage of `pywhisper.detect_language()` and `pywhisper.decode()` which provide lower-level access to the model.

```python
import pywhisper

model = pywhisper.load_model("base")

# load audio and pad/trim it to fit 30 seconds
audio = pywhisper.load_audio("audio.mp3")
audio = pywhisper.pad_or_trim(audio)

# make log-Mel spectrogram and move to the same device as the model
mel = pywhisper.log_mel_spectrogram(audio).to(model.device)

# detect the spoken language
_, probs = model.detect_language(mel)
print(f"Detected language: {max(probs, key=probs.get)}")

# decode the audio
options = pywhisper.DecodingOptions()
result = pywhisper.decode(model, mel, options)

# print the recognized text
print(result.text)
```
