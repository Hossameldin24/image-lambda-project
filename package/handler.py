import os
import boto3
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

s3 = boto3.client('s3')
PROCESSED_BUCKET = os.environ.get('PROCESSED_BUCKET', 'hossam-img-processed-1234')
MAX_SIZE = (1024, 1024)

def watermark_image(image: Image.Image, text="? MyApp"):
    draw = ImageDraw.Draw(image)
    try:
        font = ImageFont.load_default()
    except:
        font = None
    text_w, text_h = textbbox(text, font=font)
    x = max(10, image.width - text_w - 10)
    y = max(10, image.height - text_h - 10)
    draw.text((x, y), text, fill=(255,255,255,128), font=font)
    return image

def lambda_handler(event, context):
    for rec in event.get('Records', []):
        src_bucket = rec['s3']['bucket']['name']
        src_key = rec['s3']['object']['key']
        if src_bucket == PROCESSED_BUCKET:
            continue
        obj = s3.get_object(Bucket=src_bucket, Key=src_key)
        body = obj['Body'].read()
        img = Image.open(BytesIO(body)).convert("RGBA")
        img.thumbnail(MAX_SIZE, Image.Resampling.LANCZOS)
        img = watermark_image(img, text="? MyApp")
        out_buffer = BytesIO()
        img_format = 'PNG' if img.mode == 'RGBA' else 'JPEG'
        if img_format == 'JPEG':
            img = img.convert('RGB')
        img.save(out_buffer, format=img_format, optimize=True)
        out_buffer.seek(0)
        dest_key = f"processed/{src_key}"
        s3.put_object(Bucket=PROCESSED_BUCKET, Key=dest_key, Body=out_buffer, ContentType=obj.get('ContentType','image/jpeg'))
    return {"status": "ok"}
