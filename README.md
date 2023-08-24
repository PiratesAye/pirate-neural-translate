# pirate-neural-translate
Пиратский перевод для видео на YouTube

## Использованные модели

1. [PlayVoice/so-vits-svc-5.0](https://github.com/PlayVoice/so-vits-svc-5.0): voice-2-voice style trans
2. [TheBloke/llama2_7b_chat_uncensored-GPTQ](https://huggingface.co/TheBloke/llama2_7b_chat_uncensored-GPTQ) LLM
3. [facebook/seamless-m4t-medium](https://huggingface.co/facebook/seamless-m4t-medium) T2TT translation
4. [suno-ai/bark](https://github.com/suno-ai/bark) text-2-voice

## Установка

1. Склонируйте [PlayVoice/so-vits-svc-5.0](https://github.com/stillonearth/so-vits-svc-5.0/tree/bigvgan-mix-v2) в директорию pirate-neural-translate
2. Скачайте веса [cwiz/volodarsky-so-vits-svc-5.0](https://huggingface.co/cwiz/volodarsky-so-vits-svc-5.0) для so-vits-svc-5.0
3. **TODO** (Установите зависимости из requirements.txt)
4. Запускайте по очереди 01, 02, 03, 04 стадии перевода