import logging
import os
import aiofiles
import aiohttp
from PIL import Image

import config

logging.basicConfig(level=logging.INFO)


def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    newImage = image.resize((newWidth, newHeight), Image.Resampling.LANCZOS)
    return newImage


async def gen_thumb(videoid: str):
    try:
        cache_path = f"cache/{videoid}_v4.png"
        if os.path.isfile(cache_path):
            return cache_path

        os.makedirs("cache", exist_ok=True)

        custom_image_url = getattr(
            config, "CUSTOM_THUMB_URL", "https://files.catbox.moe/wser72.jpg"
        )
        image_path = f"cache/thumb{videoid}.png"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        timeout = aiohttp.ClientTimeout(total=15)

        async with aiohttp.ClientSession(headers=headers, timeout=timeout) as session:
            async with session.get(custom_image_url) as resp:
                if resp.status == 200:
                    async with aiofiles.open(image_path, mode="wb") as f:
                        await f.write(await resp.read())
                else:
                    logging.error(
                        f"Config Image URL မှ ပုံကို ဒေါင်းလုဒ်ဆွဲ၍ မရပါ။ Status: {resp.status}"
                    )
                    return None

        if not os.path.exists(image_path):
            return None

        custom_img = Image.open(image_path).convert("RGB")

        # ပုံအသေးနှင့် ဘောင်များကို ဖြုတ်လိုက်ပြီး ပုံတစ်ပုံတည်းကို 1280x720 ဘောင်အပြည့် ညှိယူခြင်း
        target_w, target_h = 1280, 720
        orig_w, orig_h = custom_img.size

        if orig_w / orig_h > target_w / target_h:
            w_crop = int(orig_h * (target_w / target_h))
            img_cropped = custom_img.crop(
                ((orig_w - w_crop) // 2, 0, (orig_w + w_crop) // 2, orig_h)
            )
        else:
            h_crop = int(orig_w * (target_h / target_w))
            img_cropped = custom_img.crop(
                (0, (orig_h - h_crop) // 2, orig_w, (orig_h + h_crop) // 2)
            )

        final_image = img_cropped.resize(
            (target_w, target_h), Image.Resampling.LANCZOS
        )

        if os.path.exists(image_path):
            os.remove(image_path)

        background_path = f"cache/{videoid}_v4.png"
        final_image.save(background_path, quality=95)

        return background_path

    except Exception as e:
        logging.error(f"Error generating thumbnail for video {videoid}: {e}")
        return None
