import json
import sys
import subprocess
import librosa

from pydub import AudioSegment
from scipy.io.wavfile import write as write_wav


json_filename = sys.argv[1]
video_uuid = json_filename.replace("output/", "").replace(".json", "")

f = open(json_filename)
subtitles = json.load(f)

orig_sound = AudioSegment.from_file(
    "output/{video_uuid}.wav".format(video_uuid=video_uuid), format="wav"
)
quiter_orig = orig_sound - 17

for i, subtitle in enumerate(subtitles):
    original_segment_length = int((subtitle["end"] - subtitle["start"]) * 1000)

    translation_fragment = AudioSegment.from_file(
        "output/{video_uuid}/{i}.wav".format(video_uuid=video_uuid, i=str(i)),
        format="wav",
    )
    translation_fragment + 20

    if len(translation_fragment) > original_segment_length:
        translation_fragment = translation_fragment[:original_segment_length]

    accumulated_length = 0
    quiter_orig = quiter_orig.overlay(
        translation_fragment, position=int(1000 * subtitle["start"])
    )

ffmpeg_command = """ffmpeg -i output/{video_uuid}.mp4 -vf "tinterlace=4, curves=m='0/0 0.5/0.9':r='0/0 0.5/0.5 1/1':g='0/0 0.5/0.5 1/1':b='0/0 0.5/0.5 1/1':, eq=saturation=1.2, scale=480:360, smartblur=lr=2:ls=-1, noise=c0s=13:c0f=t+u, gblur=sigma=3:steps=1, unsharp=luma_msize_x=15:luma_msize_y=9:luma_amount=5.0:chroma_msize_x=7:chroma_msize_y=3:chroma_amount=-2, format=yuv422p" -af "highpass=f=50, lowpass=f=5000" output/{video_uuid}-vhs.mp4""".format(video_uuid=video_uuid)
subprocess.call(ffmpeg_command, shell=True)

file_handle = quiter_orig.export(
    "output/{video_uuid}-vol.wav".format(video_uuid=video_uuid), format="wav"
)

ffmpeg_command = "ffmpeg -i output/{video_uuid}-vhs.mp4 -i output/{video_uuid}-vol.wav -c:v copy -map 0:v:0 -map 1:a:0 output/{video_uuid}-new.mp4".format(
    video_uuid=video_uuid
)

subprocess.call(ffmpeg_command, shell=True)
