"""
InstaCaption AI — Image → Instagram-style captions
Stage 1 (Vision): BLIP generates a raw description of the image
Stage 2 (NLP):    Llama 3.1 rewrites it into Instagram-style captions,
                  optionally mimicking the user's own caption style.
"""

import os
import gradio as gr
import torch
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
from huggingface_hub import InferenceClient

# ----------------------------
# Stage 1: Vision model (BLIP)
# ----------------------------
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
blip_model = BlipForConditionalGeneration.from_pretrained(
    "Salesforce/blip-image-captioning-base"
).to(DEVICE)


def get_raw_caption(image: Image.Image) -> str:
    """Run BLIP on the image and return a plain factual description."""
    inputs = processor(image.convert("RGB"), return_tensors="pt").to(DEVICE)
    with torch.no_grad():
        output = blip_model.generate(**inputs, max_new_tokens=50)
    return processor.decode(output[0], skip_special_tokens=True)


# ----------------------------
# Stage 2: LLM (Instagram style)
# ----------------------------
LLM_MODEL = "meta-llama/Llama-3.1-8B-Instruct"
client = InferenceClient(token=os.getenv("HF_TOKEN"))

TONES = [
    "Aesthetic / Minimal",
    "Funny / Witty",
    "Motivational",
    "Travel / Wanderlust",
    "Romantic",
    "Casual / Friendly",
    "Professional / Brand",
]


def build_prompt(raw_caption, tone, past_captions, num_captions, include_hashtags):
    style_block = ""
    if past_captions and past_captions.strip():
        style_block = (
            "\nThe user pasted some of their past Instagram captions below. "
            "Study their voice (emoji usage, length, punctuation, vibe) and "
            "write the new captions in the SAME personal style:\n"
            f"---\n{past_captions.strip()}\n---\n"
        )

    hashtag_rule = (
        "End each caption with 4-6 relevant, popular hashtags."
        if include_hashtags
        else "Do NOT include any hashtags."
    )

    return f"""You are an expert Instagram caption writer.

An AI vision model described the uploaded photo as: "{raw_caption}"

Write {num_captions} different Instagram captions for this photo.
Tone: {tone}
{style_block}
Rules:
- Each caption must feel native to Instagram (emojis welcome where natural).
- Keep each caption under 2 short sentences unless the tone demands more.
- {hashtag_rule}
- Number the captions 1., 2., 3. ...
- Return ONLY the captions, no preamble or explanation."""


def generate(image, tone, past_captions, num_captions, include_hashtags):
    if image is None:
        return "", "⚠️ Please upload an image first."

    raw_caption = get_raw_caption(image)

    prompt = build_prompt(raw_caption, tone, past_captions, num_captions, include_hashtags)

    try:
        response = client.chat_completion(
            model=LLM_MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0.9,
        )
        captions = response.choices[0].message.content.strip()
    except Exception as e:
        captions = (
            "❌ LLM call failed. Make sure the HF_TOKEN secret is set in your "
            f"Space settings.\n\nError: {e}"
        )

    return raw_caption, captions


# ----------------------------
# UI
# ----------------------------
with gr.Blocks(title="InstaCaption AI") as demo:
    gr.Markdown(
        """
        # 📸 InstaCaption AI
        Upload a photo → get Instagram-ready captions.
        **Computer Vision (BLIP)** describes your image, then an **LLM (Llama 3.1)**
        turns it into captions in your chosen tone — or in *your own voice* if you
        paste a few of your past captions.
        """
    )

    with gr.Row():
        with gr.Column():
            image_input = gr.Image(type="pil", label="Upload your photo")
            tone = gr.Dropdown(TONES, value=TONES[0], label="Caption tone")
            past_captions = gr.Textbox(
                label="Your past Instagram captions (optional — for personalization)",
                placeholder="Paste 2-5 of your own captions here, one per line...",
                lines=4,
            )
            num_captions = gr.Slider(1, 5, value=3, step=1, label="Number of captions")
            include_hashtags = gr.Checkbox(value=True, label="Include hashtags")
            btn = gr.Button("✨ Generate Captions", variant="primary")

        with gr.Column():
            raw_out = gr.Textbox(label="🔍 What the vision model sees (BLIP)")
            captions_out = gr.Textbox(label="📝 Your Instagram captions", lines=12)

    btn.click(
        generate,
        inputs=[image_input, tone, past_captions, num_captions, include_hashtags],
        outputs=[raw_out, captions_out],
    )

    gr.Markdown("Built by **Aarij** · BLIP + Llama 3.1 · [GitHub](https://github.com/YOUR_USERNAME/insta-caption-ai)")

if __name__ == "__main__":
    demo.launch()
