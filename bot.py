import discord
from discord.ext import commands
import os

from config import TOKEN, PREFIX
from ai import generate_image
from meme import make_meme

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot login sebagai {bot.user}")

@bot.command()
async def meme(ctx, *, args=None):
    try:
        await ctx.send("🧠 Lagi mikir meme...")

        if not args:
            await ctx.send("❌ Format: !meme prompt | teks atas | teks bawah")
            return

        parts = [p.strip() for p in args.split("|")]
        prompt = parts[0]
        top_text = parts[1] if len(parts) > 1 else ""
        bottom_text = parts[2] if len(parts) > 2 else ""

        image_path = generate_image(prompt)
        meme_path = make_meme(image_path, top_text, bottom_text)

        await ctx.send(file=discord.File(meme_path))

    except Exception as e:
        await ctx.send(f"❌ Error: {e}")

@bot.command()
async def start(ctx):
    help_embed = discord.Embed(
        title="🤖 Meme-generator Bot",
        description="Bot AI image generator menggunakan Pollinations API untuk membuat meme.\n\n",
        color=discord.Color.blue()
    )
    help_embed.add_field(
        name="📝 Perintah Yang Tersedia - Available commands:",
        value=(
            "`!start`  - Tampilkan bantuan ini\n"
            "`!meme <prompt> | <teks atas> | <teks bawah>` - Buat meme dari prompt\n"
            "`!meme_random`  - Memberikan meme acak ke user\n"
        ),
        inline=False
    )
    help_embed.add_field(
        name="📖 Cara Menggunakan - How to use:",
        value=(
            "Untuk membuat meme, gunakan `!meme` diikuti dengan prompt dan teks meme.\n\n"
            "**Contoh:**\n"
            "`!meme funny cat | Ketika kamu melihat makanan | Tapi kamu sedang diet`"
        ),
        inline=False
    )
    help_embed.add_field(
        name="⚙️ Fitur - Features:", 
        value=(
            "✅ Generate gambar AI berkualitas tinggi\n"
            "✅ Tambahkan teks meme di atas dan bawah gambar\n"
            "✅ Support prompt bahasa indonesia\n"
        ),
        inline=False
    )
    help_embed.set_footer(text="Gunakan perintah dengan prefix ! untuk mengaktifkan bot")
    await ctx.send(embed=help_embed)

# ---TUGAS FUNGSI TAMBAHAN--- #

import random

RANDOM_MEMES = [
    {
        "prompt": "tired programmer late night",
        "top": "NIAT TIDUR CEPET",
        "bottom": "TAU TAU SUBUH"
    },
    {
        "prompt": "confused cat meme",
        "top": "GUA",
        "bottom": "PAS LIAT SOAL"
    },
    {
        "prompt": "office worker staring at screen",
        "top": "KATANYA KERJA TIM",
        "bottom": "YANG KERJA GUA"
    },
    {
        "prompt": "sad anime boy",
        "top": "BILANG GAPAPA",
        "bottom": "PADAHAL CAPEK"
    },
    {
        "prompt": "dog sitting fire meme",
        "top": "INI",
        "bottom": "BAIK BAIK SAJA"
    }
]

@bot.command()
async def meme_random(ctx):
    try:
        await ctx.send("🎲 Lagi nyari meme random...")

        data = random.choice(RANDOM_MEMES)

        image_path = generate_image(data["prompt"])
        meme_path = make_meme(
            image_path,
            data["top"],
            data["bottom"]
        )

        await ctx.send(file=discord.File(meme_path))

    except Exception as e:
        await ctx.send(f"❌ Error: {e}")


bot.run(TOKEN)
