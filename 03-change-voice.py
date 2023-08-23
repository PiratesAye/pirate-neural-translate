import json
import sys
import subprocess

from scipy.io.wavfile import write as write_wav

json_filename = sys.argv[1]
video_uuid = json_filename.replace("output/", "").replace(".json", "")

f = open(json_filename)
subtitles = json.load(f)

for i, subtitle in enumerate(subtitles):    
    change_voice_command = "cd so-vits-svc-5.0 && python svc_inference.py --config configs/base.yaml --model sovits5.0.pth --spk volodarsky.spk.npy --wave ../output/{video_uuid}/{i}.wav --shift 0".format(
        video_uuid=video_uuid, i=i
    )
    
    subprocess.call(change_voice_command, shell=True)

    cp_command = "cp so-vits-svc-5.0/svc_out.wav output/{video_uuid}/{i}-vol.wav".format(
        video_uuid=video_uuid, i=i
    )

    subprocess.call(cp_command, shell=True)