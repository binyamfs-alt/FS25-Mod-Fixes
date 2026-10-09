"""Build the original standalone add-on; no third-party mod is packaged."""
from pathlib import Path
import zipfile
from PIL import Image, ImageDraw
ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / 'source'
im = Image.new('RGB', (512, 512), '#151c16')
d = ImageDraw.Draw(im)
d.rounded_rectangle((40, 100, 470, 360), radius=24, fill='#839f35')
d.rectangle((70, 125, 430, 285), fill='#263329')
for x in (105, 205, 305):
    d.ellipse((x, 170, x+80, 230), fill='#eeeece')
    d.ellipse((x+60, 150, x+95, 195), fill='#eeeece')
    d.line((x+15, 220, x+15, 250), fill='#eeeece', width=10)
    d.line((x+65, 220, x+65, 250), fill='#eeeece', width=10)
for x in (125, 370):
    d.ellipse((x-35, 330, x+35, 400), fill='#101210', outline='#eeeece', width=8)
d.rectangle((60, 430, 452, 455), fill='#39423b')
d.rectangle((60, 430, 320, 455), fill='#b7d642')
im.save(SOURCE / 'icon_livestockCapacityHUD.dds', pixel_format='DXT1')
out = ROOT / 'builds' / 'FS25_z_LivestockCapacityHUD.zip'
out.parent.mkdir(exist_ok=True)
with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
    for p in sorted(SOURCE.rglob('*')):
        if p.is_file():
            info = zipfile.ZipInfo(p.relative_to(SOURCE).as_posix(), (2026,10,8,0,0,0))
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, p.read_bytes())
print(out)
