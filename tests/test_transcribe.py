import os

import pytest

import pywhisper


@pytest.mark.parametrize('model_name', ["tiny.en", "tiny", "base.en", "base"])
def test_transcribe(model_name: str):
    model = pywhisper.load_model(model_name)
    audio_path = os.path.join(os.path.dirname(__file__), "jfk.flac")

    language = "en" if model_name.endswith(".en") else None
    result = model.transcribe(audio_path, language=language, temperature=0.0)
    assert result["language"] == "en"

    transcription = result["text"].lower()
    assert "my fellow americans" in transcription
    assert "your country" in transcription
    assert "do for you" in transcription
