"""
Generate high-resolution theme images for TVK Chrome Extension.
Creates a new tab background and toolbar texture using party colors.
"""

from PIL import Image, ImageDraw, ImageFilter
import math
import os

# TVK Party Colors
CRIMSON = (163, 19, 42)
GOLD = (245, 184, 0)
GREEN = (27, 140, 27)
DARK_CRIMSON = (120, 14, 30)
DEEP_GOLD = (200, 150, 0)

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "images")


def create_ntp_background(width=1920, height=1080):
    """Create a stunning new tab page background with gradient and geometric patterns."""
    img = Image.new("RGB", (width, height), CRIMSON)
    draw = ImageDraw.Draw(img)

    # Create a rich gradient background: crimson top -> dark crimson bottom
    for y in range(height):
        ratio = y / height
        r = int(CRIMSON[0] * (1 - ratio * 0.5) + DARK_CRIMSON[0] * ratio * 0.5)
        g = int(CRIMSON[1] * (1 - ratio * 0.6))
        b = int(CRIMSON[2] * (1 - ratio * 0.4))
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    # Draw golden horizontal band across the middle (like the flag)
    band_top = int(height * 0.38)
    band_bottom = int(height * 0.62)
    band_height = band_bottom - band_top

    for y in range(band_top, band_bottom):
        # Add subtle gradient within the gold band
        progress = (y - band_top) / band_height
        # Slight darkening at edges for depth
        edge_factor = 1.0 - 0.15 * (abs(progress - 0.5) * 2) ** 2
        r = int(GOLD[0] * edge_factor)
        g = int(GOLD[1] * edge_factor)
        b = int(GOLD[2] * edge_factor * 0.3)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    # Add thin golden accent lines above and below the band
    for offset in [-3, -2, -1, 0]:
        draw.line([(0, band_top + offset), (width, band_top + offset)],
                  fill=(255, 215, 0), width=1)
        draw.line([(0, band_bottom - offset), (width, band_bottom - offset)],
                  fill=(255, 215, 0), width=1)

    # Draw decorative geometric pattern — radiating lines from center
    cx, cy = width // 2, height // 2
    num_rays = 36
    for i in range(num_rays):
        angle = (2 * math.pi * i) / num_rays
        length = min(width, height) * 0.45
        ex = cx + int(length * math.cos(angle))
        ey = cy + int(length * math.sin(angle))
        # Semi-transparent gold rays
        draw.line([(cx, cy), (ex, ey)], fill=(GOLD[0], GOLD[1], GOLD[2]), width=1)

    # Draw concentric circles in the center (inspired by the emblem)
    for radius in [120, 100, 80]:
        bbox = (cx - radius, cy - radius, cx + radius, cy + radius)
        draw.ellipse(bbox, outline=GOLD, width=2)

    # Inner filled circle
    inner_r = 60
    bbox = (cx - inner_r, cy - inner_r, cx + inner_r, cy + inner_r)
    draw.ellipse(bbox, fill=DARK_CRIMSON, outline=GOLD, width=3)

    # Draw small green stars around the inner circle
    num_stars = 18
    star_radius = 105
    for i in range(num_stars):
        angle = (2 * math.pi * i) / num_stars - math.pi / 2
        sx = cx + int(star_radius * math.cos(angle))
        sy = cy + int(star_radius * math.sin(angle))
        # Small diamond/star shape
        size = 5
        star_points = [
            (sx, sy - size),
            (sx + size, sy),
            (sx, sy + size),
            (sx - size, sy),
        ]
        draw.polygon(star_points, fill=GREEN)

    # Add subtle diagonal pattern overlay for texture
    for i in range(-height, width + height, 40):
        draw.line([(i, 0), (i + height, height)],
                  fill=(255, 255, 255, 8) if img.mode == "RGBA" else (
                      min(255, CRIMSON[0] + 8),
                      min(255, CRIMSON[1] + 3),
                      min(255, CRIMSON[2] + 5),
                  ), width=1)

    # Apply slight blur for a polished look
    img = img.filter(ImageFilter.GaussianBlur(radius=0.8))

    return img


def create_ntp_attribution(width=200, height=50):
    """Small attribution image shown on new tab page."""
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    # Small TVK text area with gold background
    draw.rounded_rectangle([(5, 5), (195, 45)], radius=8, fill=(*CRIMSON, 220), outline=(*GOLD, 255), width=2)
    return img


def create_toolbar_texture(width=200, height=48):
    """Subtle texture for the toolbar area."""
    img = Image.new("RGB", (width, height), DARK_CRIMSON)
    draw = ImageDraw.Draw(img)
    # Subtle gradient
    for y in range(height):
        ratio = y / height
        r = int(DARK_CRIMSON[0] + (CRIMSON[0] - DARK_CRIMSON[0]) * ratio * 0.3)
        g = int(DARK_CRIMSON[1] + (CRIMSON[1] - DARK_CRIMSON[1]) * ratio * 0.3)
        b = int(DARK_CRIMSON[2] + (CRIMSON[2] - DARK_CRIMSON[2]) * ratio * 0.3)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    # Gold accent line at bottom
    draw.line([(0, height - 1), (width, height - 1)], fill=GOLD, width=2)
    return img


if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("Generating new tab background (1920x1080)...")
    ntp = create_ntp_background(1920, 1080)
    ntp.save(os.path.join(OUTPUT_DIR, "ntp_background.png"), "PNG", quality=95)

    print("Generating NTP attribution...")
    attr = create_ntp_attribution()
    attr.save(os.path.join(OUTPUT_DIR, "ntp_attribution.png"), "PNG")

    print("Generating toolbar texture...")
    toolbar = create_toolbar_texture()
    toolbar.save(os.path.join(OUTPUT_DIR, "toolbar_texture.png"), "PNG")

    # Also create a high-res version of the flag as theme_frame
    print("Processing flag image for theme frame...")
    try:
        flag = Image.open(os.path.join(OUTPUT_DIR, "flag.jpeg"))
        # Resize to a good header size while maintaining aspect ratio
        flag_resized = flag.resize((1920, int(1920 * flag.height / flag.width)), Image.LANCZOS)
        flag_resized.save(os.path.join(OUTPUT_DIR, "theme_frame.png"), "PNG", quality=95)
        print(f"  Flag resized to {flag_resized.size}")
    except Exception as e:
        print(f"  Could not process flag: {e}")

    print("All theme images generated!")
