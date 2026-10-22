"""Generate per-page Open Graph images (1200x630) with the RoboRide logo and pin. Run with a Python that has Pillow + cairosvg."""
import io, cairosvg, pathlib
from PIL import Image, ImageDraw, ImageFont, ImageFilter
R = pathlib.Path(__file__).resolve().parent.parent
SYNE, DM = "/tmp/fonts/Syne.ttf", "/tmp/fonts/DMSans.ttf"
def font(path, size, w):
    f = ImageFont.truetype(path, size)
    try: f.set_variation_by_axes([w] if path == SYNE else [14, w])
    except Exception: pass
    return f
def svg(path, h):
    return Image.open(io.BytesIO(cairosvg.svg2png(url=str(R / path), output_height=h))).convert("RGBA")
PAGES = {
  "businesses":   ("FOR BUSINESSES", ["Autonomous delivery", "for NWA businesses."], "Register interest in driverless goods delivery."),
  "service-area": ("PLANNED SERVICE AREA", ["Seven cities,", "one region."], "Bentonville · Rogers · Springdale · Fayetteville and more"),
  "safety":       ("SAFETY & REGULATION", ["Safety first,", "and by the rules."], "How driverless vehicles are regulated in Arkansas."),
  "privacy":      ("PRIVACY POLICY", ["Your data,", "kept simple."], "What RoboRide collects through this website, and why."),
  "about":        ("ABOUT ROBORIDE", ["Built in NWA,", "for NWA."], "An independent Northwest Arkansas company, founded 2026."),
  "press":        ("PRESS KIT", ["Writing about", "RoboRide?"], "Boilerplate, fast facts and brand assets."),
}
GOLD, WHITE, MUTED, BG = (232, 183, 78), (255, 255, 255), (168, 156, 136), (10, 8, 6)
for slug, (eyebrow, lines, sub) in PAGES.items():
    im = Image.new("RGB", (1200, 630), BG)
    glow = Image.new("RGB", (1200, 630), BG); gd = ImageDraw.Draw(glow)
    gd.ellipse((760, 40, 1240, 600), fill=(60, 44, 16)); glow = glow.filter(ImageFilter.GaussianBlur(120))
    im = Image.blend(im, glow, 1.0); d = ImageDraw.Draw(im)
    for x in range(0, 1200, 60): d.line([(x, 0), (x, 630)], fill=(20, 17, 11))
    for y in range(0, 630, 60): d.line([(0, y), (1200, y)], fill=(20, 17, 11))
    logo = svg("image/brand/roboride-logo-white.svg", 44); im.paste(logo, (80, 70), logo)
    d.text((80 + logo.width + 14, 70 + 22), "Robo", font=font(SYNE, 36, 800), fill=WHITE, anchor="lm")
    rw = d.textlength("Robo", font=font(SYNE, 36, 800))
    d.text((80 + logo.width + 14 + rw, 92), "Ride", font=font(SYNE, 36, 800), fill=GOLD, anchor="lm")
    d.text((80, 205), eyebrow, font=font(DM, 24, 600), fill=GOLD)
    size = 66
    while max(d.textlength(t, font=font(SYNE, size, 800)) for t in lines) > 760: size -= 2
    f = font(SYNE, size, 800)
    d.text((80, 250), lines[0], font=f, fill=WHITE); d.text((80, 250 + int(size * 1.18)), lines[1], font=f, fill=GOLD)
    d.text((80, 450), sub, font=font(DM, 28, 400), fill=MUTED)
    d.text((80, 540), "www.nwaroboride.org", font=font(DM, 22, 500), fill=MUTED)
    pin = svg("image/brand/roboride-pin.svg", 280); im.paste(pin, (1120 - pin.width, 175), pin)
    im.save(R / f"image/og/og-{slug}.jpg", quality=85, optimize=True, progressive=True)
    print(slug)
