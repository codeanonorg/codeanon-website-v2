from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OGRAPH_SIZE = (1200, 630)
DATADIR = Path(__file__).parent / "data"
LOGO = DATADIR / "logo.png"
GRADIENT = DATADIR / "gradient.png"
FONT = DATADIR / "fonts" / "WorkSans-Medium.ttf"


def center(canvas: tuple[int, int], size: tuple[int, int]) -> tuple[int, int, int, int]:
    cw, ch = canvas
    w, h = size
    assert cw >= w and ch >= h

    mw = cw - w
    mh = ch - h
    x = mw / 2
    y = mh / 2
    return int(x), int(y), w, h


def resize_fill(im: Image.Image, size: tuple[int, int]) -> Image.Image:
    w, h = size
    sw, sh = im.size
    ratio = max(w / sw, h / sh)
    new_size = (int(sw * ratio), int(sh * ratio))

    box = center(new_size, size)

    print("box", box, "new_size", new_size)
    return im.resize(new_size)  # .crop(box)


def layout_lines(font: ImageFont.FreeTypeFont, title: str, bounds: tuple[int, int]) -> Image.Image:
    lines: list[str] = []
    for line in title.splitlines():
        cur_line = ""
        for word in line.split():
            if font.getsize(cur_line)[0] > bounds[0]:
                lines.append(cur_line)
                cur_line = ""
            cur_line += f"{word} "
            cur_line.strip()
        if len(cur_line) > 0:
            lines.append(cur_line.strip())

    text = "\n".join(lines)
    fw, fh = font.getsize_multiline(text)
    size = (fw, max(fh, bounds[1]))
    im = Image.new("RGBA", size)
    draw = ImageDraw.Draw(im)
    draw.multiline_text((0, 0), text, font=font)
    return im


def assemble(bg: Image.Image, title: str) -> Image.Image:
    out = Image.new("RGBA", OGRAPH_SIZE, "black")
    out.paste(resize_fill(bg, OGRAPH_SIZE))
    with Image.open(str(LOGO)) as logo:
        out.alpha_composite(logo)
    with Image.open(str(GRADIENT)) as gradient:
        y = OGRAPH_SIZE[1] - gradient.size[1]
        out.alpha_composite(gradient, (0, y))

    font = ImageFont.truetype(str(FONT), 40)
    margin = 60
    tw = OGRAPH_SIZE[0] - 2 * margin
    text_layer = layout_lines(font, title, (tw, 400))
    ty = OGRAPH_SIZE[1] - margin - text_layer.size[1]
    print("Text layer:", (margin, ty), text_layer.size)
    out.alpha_composite(text_layer, (margin, ty))

    return out
