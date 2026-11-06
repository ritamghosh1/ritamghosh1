#!/usr/bin/env python3
"""Render deterministic share artwork from the approved portrait and site identity.
Requires Pillow only when regenerating images; runtime site has no dependencies.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps
root = Path(__file__).resolve().parents[1]
folder = root / 'docs/assets/images'
regular = '/System/Library/Fonts/Supplemental/Arial.ttf'
bold = '/System/Library/Fonts/Supplemental/Arial Bold.ttf'
# DejaVu Sans paths make this usable on Linux as well.
if not Path(regular).exists():
    regular = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
    bold = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
font = lambda size, strong=False: ImageFont.truetype(bold if strong else regular, size)
im = Image.new('RGB', (1200,630), '#f8f9f5')
draw = ImageDraw.Draw(im)
draw.text((64,48), 'rg.', font=font(48,True), fill='#3158cf')
draw.text((64,165), 'Ritam', font=font(88,True), fill='#172c38')
draw.text((64,261), 'Ghosh.', font=font(88,True), fill='#172c38')
draw.text((68,392), 'Developer. Problem solver.', font=font(26), fill='#52636b')
draw.text((68,433), 'Web / AI / Algorithms', font=font(23), fill='#52636b')
draw.line((68,534,640,534), fill='#d7dedb', width=2)
draw.text((68,557), 'ritamghosh1.github.io/ritamghosh1', font=font(19), fill='#52636b')
photo = Image.open(folder/'ritam-ghosh.jpg')
photo = ImageOps.fit(photo, (440,550), method=Image.Resampling.LANCZOS, centering=(.52,.36))
mask = Image.new('L',photo.size,0); md = ImageDraw.Draw(mask)
md.rounded_rectangle((0,0,440,550),radius=150,fill=255)
im.paste(photo,(710,40),mask)
im.save(folder/'social-preview.jpg',quality=91,optimize=True)
icon = Image.new('RGB',(180,180),'#3158cf'); d = ImageDraw.Draw(icon)
d.text((24,38),'rg.',font=font(94,True),fill='white')
icon.save(folder/'apple-touch-icon.png',optimize=True)
print('Generated 1200×630 share card and 180×180 touch icon.')
