import json
import sys
import subprocess

from pydub import AudioSegment


json_filename = sys.argv[1]
video_uuid = json_filename.replace("output/", "").replace(".json", "")

f = open(json_filename)
subtitles = json.load(f)

orig_sound = AudioSegment.from_file(
    "output/{video_uuid}.wav".format(video_uuid=video_uuid), format="wav"
)
quiter_orig = orig_sound - 15


for i, subtitle in enumerate(subtitles):
    translation_fragment = AudioSegment.from_file(
        "output/{video_uuid}/{i}.wav".format(video_uuid=video_uuid, i=str(i)),
        format="wav",
    )
    translation_fragment + 20
    original_segment_length = int(1000 * subtitle["end"] - 1000 * subtitle["start"])
    
    if len(translation_fragment) > original_segment_length:
        translation_fragment = translation_fragment[:original_segment_length]
    accumulated_length = 0
    quiter_orig = quiter_orig.overlay(
        translation_fragment, position=int(1000 * subtitle["start"])
    )

file_handle = quiter_orig.export(
    "output/{video_uuid}-vol.wav".format(video_uuid=video_uuid), format="wav"
)

ffmpeg_command = "ffmpeg -i output/{video_uuid}.mp4 -i output/{video_uuid}-vol.wav -c:v copy -map 0:v:0 -map 1:a:0 output/{video_uuid}-new.mp4".format(video_uuid=video_uuid)

subprocess.call(ffmpeg_command, shell=True)
