import uuid
import subprocess
import torch
import json
import sys

from pytube import YouTube
from faster_whisper import WhisperModel
from transformers import AutoTokenizer, pipeline
from auto_gptq import AutoGPTQForCausalLM
from tqdm import tqdm
from seamless_communication.models.inference import Translator


def download_yt_video(link, filename):
    yt = YouTube(link)
    yt.streams.filter(progressive=True, file_extension="mp4").order_by(
        "resolution"
    ).desc().first().download(output_path="./output/", filename=filename)


yt_link = sys.argv[1]

video_uuid = uuid.uuid4().hex
video_filename = video_uuid + ".mp4"
audio_filename = video_uuid + ".wav"

mkdir_command = "mkdir output/{video_uuid}".format(video_uuid=video_uuid)
subprocess.call(mkdir_command, shell=True)

download_yt_video(yt_link, video_filename)

ffmpeg_command = "ffmpeg -i ./output/{video_filename} -acodec pcm_s16le -ac 1 -ar 16000 ./output/{audio_filename}".format(
    video_filename=video_filename, audio_filename=audio_filename
)

subprocess.call(ffmpeg_command, shell=True)

model = WhisperModel("large-v2", device="cuda", compute_type="float16")
segments, info = model.transcribe(
    "output/" + audio_filename, beam_size=5, language="en"
)

subtitles = []

for segment in segments:
    print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
    subtitle = {
        "original_text": segment.text,
        "start": segment.start,
        "end": segment.end,
    }
    subtitles.append(subtitle)

del model


model_name_or_path = "TheBloke/llama2_7b_chat_uncensored-GPTQ"
model_basename = "model"
use_triton = False
tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, use_fast=True)

model = AutoGPTQForCausalLM.from_quantized(
    model_name_or_path,
    model_basename=model_basename,
    use_safetensors=True,
    trust_remote_code=True,
    device="cuda:0",
    use_triton=use_triton,
    quantize_config=None,
)


def change_meaning(text):
    prompt = "Change meaning of this sentence to opposite by changing some words, reply only new text, no explanation. `{text}`".format(
        text=text
    )

    prompt_template = f"""### HUMAN:
    {prompt}

    ### RESPONSE:
    """

    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=64,
        temperature=0.7,
        top_p=0.95,
        repetition_penalty=1.15,
    )

    reply = pipe(prompt_template)[0]["generated_text"]
    reply = reply[len(prompt_template) :]

    end_index = reply.find("### HUMAN")
    if end_index != -1:
        return reply[:end_index]

    return reply


for subtitle in tqdm(subtitles):
    changed_sentence = change_meaning(subtitle["original_text"])
    subtitle["changed_text"] = changed_sentence

del model
del tokenizer

torch.cuda.empty_cache()

translator = Translator(
    "seamlessM4T_medium",
    vocoder_name_or_card="vocoder_36langs",
    device=torch.device("cuda:0"),
)

for subtitle in tqdm(subtitles):
    translated_text, _, _ = translator.predict(
        subtitle["changed_text"], "t2tt", "rus", src_lang="eng"
    )
    subtitle["translated_changed_text"] = str(translated_text)

with open("output/" + video_uuid + ".json", "w", encoding="utf-8") as outfile:
    json.dump(subtitles, outfile, ensure_ascii=False)

print(video_uuid)
