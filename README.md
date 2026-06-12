---
title: InstaCaption AI
emoji: 📸
colorFrom: pink
colorTo: purple
sdk: gradio
sdk_version: "6.17.3"
app_file: app.py
pinned: false
---

# 📸 InstaCaption AI — Instagram Caption Generator

Upload a photo and get Instagram-ready captions in seconds. Combines **Computer Vision** and **NLP** in a two-stage AI pipeline — and it can even mimic *your* personal caption style.

**🔴 Live Demo:** https://huggingface.co/spaces/aarij2026/insta-caption-ai

## How it works

```
 ┌─────────────┐     ┌──────────────────┐     ┌─────────────────────┐
 │  Your photo │ ──▶ │  BLIP (Vision)   │ ──▶ │  Llama 3.1 (NLP)    │ ──▶ 📝 Captions
 └─────────────┘     │  "a dog running  │     │  Instagram-style    │
                     │   on a beach"    │     │  rewrite + hashtags │
                     └──────────────────┘     └─────────────────────┘
```

1. **Vision stage** — [BLIP](https://huggingface.co/Salesforce/blip-image-captioning-base) (Salesforce) generates a raw factual description of the uploaded image.
2. **NLP stage** — Llama 3.1 8B (via Hugging Face Inference API) rewrites the description into Instagram-style captions based on:
   - **Tone** (Aesthetic, Funny, Motivational, Travel, Romantic, Casual, Brand)
   - **Your personal voice** — paste a few of your past captions and the model mimics your emoji usage, length, and vibe
   - **Hashtag preference** and number of variants

## Features

- 🖼️ Drag-and-drop image upload
- 🎭 7 caption tones
- 🪞 Personalization from your own past captions (few-shot style transfer)
- #️⃣ Optional hashtag generation
- 📋 One-click copy

## Tech Stack

| Layer | Tech |
|---|---|
| Computer Vision | BLIP (`Salesforce/blip-image-captioning-base`) |
| LLM | Llama 3.1 8B Instruct (HF Inference API) |
| UI | Gradio |
| Deployment | Hugging Face Spaces (free CPU tier) |

## Run locally

```bash
git clone https://github.com/syedaarijali/insta-caption-ai.git
cd insta-caption-ai
pip install -r requirements.txt
set HF_TOKEN=your_huggingface_token
python app.py
```

Open http://127.0.0.1:7860

## Deploy your own (free)

1. Create a Space at https://huggingface.co/new-space → SDK: **Gradio**
2. Push this repo to the Space
3. In Space **Settings → Variables and secrets**, add a secret `HF_TOKEN` with a token from https://huggingface.co/settings/tokens (enable "Make calls to Inference Providers")

## Author

**Syed Aarij Ali Hasan** — Data Scientist & ML Engineer, Berlin
[GitHub](https://github.com/syedaarijali) · [Hugging Face](https://huggingface.co/aarij2026)
