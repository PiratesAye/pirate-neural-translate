import json
import sys

from bark import SAMPLE_RATE, generate_audio, preload_models
from scipy.io.wavfile import write as write_wav

json_filename = sys.argv[1]
video_uuid = json_filename.replace("output/", "").replace(".json", "")

f = open(json_filename)
subtitles = json.load(f)

print(subtitles)

preload_models()

for i, subtitle in enumerate(subtitles):
    audio_array = generate_audio(
        subtitle["translated_changed_text"], history_prompt="v2/ru_speaker_2"
    )
    write_wav("output/" + video_uuid + "/" + str(i) + ".wav", SAMPLE_RATE, audio_array)
