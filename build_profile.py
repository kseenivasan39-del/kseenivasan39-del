import os
import sys
from pathlib import Path
from PIL import Image

# ==============================================================================
# CONFIGURATION
# Feel free to edit these values to customize your terminal profile README!
# ==============================================================================
CONFIG = {
    "username": "kseenivasan39-del",
    "name": "Anish",
    "role": "Aeronautics & Space Technology",
    "origin": "India",
    "education": "Aeronautics & Space Technology",
    "status": "Exploring Space-Tech • Programming",
    "toolchain": "Git, MATLAB, VS Code, Python",
    
    # Core Skills
    "core_lang": "Python, C, SQL",
    "core_frontend": "HTML5, CSS3",
    "core_backend": "Python, SQL",
    "core_database": "SQL, SQLite",
    "core_infra": "GitHub Actions",
    
    # Contact & Socials
    "contact_email": "anish@example.com",
    "contact_portfolio": "anish.dev",
    "contact_linkedin": "anish-profile",
    "contact_github": "kseenivasan39-del",
    
    # SVG Settings
    "theme_color_primary": "#22D3EE",   # Cyan
    "theme_color_secondary": "#818CF8", # Indigo/Purple
    "theme_color_accent": "#10B981",    # Emerald Green
    "font_family": "'Fira Code', 'JetBrains Mono', monospace",
}

ASCII_CHARS_LIGHT = " .:-=+*#%@" # From darkest (space/dot) to brightest (@) for dark mode
ASCII_CHARS_DARK  = "@%#*+=-:. " # Standard from darkest (@) to brightest (space)

def image_to_ascii(image_path, width=50, invert=False):
    """
    Converts an image into ASCII art.
    If the image has transparency (alpha channel), transparent pixels are mapped to spaces.
    """
    try:
        img = Image.open(image_path)
    except Exception as e:
        print(f"Error loading image '{image_path}': {e}")
        print("Using a placeholder ASCII portrait instead.")
        return get_placeholder_ascii()
    
    # Handle transparency
    has_alpha = img.mode == 'RGBA' or 'transparency' in img.info
    if has_alpha:
        # Separate alpha channel
        img_rgba = img.convert('RGBA')
        alpha = img_rgba.split()[3]
        # Create black background for grayscale conversion
        background = Image.new("RGBA", img_rgba.size, (0, 0, 0, 255))
        img = Image.alpha_composite(background, img_rgba).convert('L')
    else:
        img = img.convert('L')
    
    # Monospace fonts are typically taller than they are wide.
    # We adjust the height scale factor (typically 0.5 - 0.6) to prevent stretching.
    aspect_ratio = img.height / img.width
    height = int(width * aspect_ratio * 0.55)
    img = img.resize((width, height), Image.Resampling.LANCZOS)
    
    # Map pixels to ASCII
    chars = ASCII_CHARS_DARK if invert else ASCII_CHARS_LIGHT
    num_chars = len(chars)
    
    ascii_lines = []
    for y in range(height):
        line_chars = []
        for x in range(width):
            # Check transparency mask if it exists
            if has_alpha:
                # Get transparency at scaled coordinate
                orig_x = int(x * (alpha.width / width))
                orig_y = int(y * (alpha.height / height))
                # Bounds check
                orig_x = min(orig_x, alpha.width - 1)
                orig_y = min(orig_y, alpha.height - 1)
                if alpha.getpixel((orig_x, orig_y)) < 50:
                    line_chars.append(" ")
                    continue
            
            pixel_val = img.getpixel((x, y))
            char_idx = int(pixel_val / 256 * num_chars)
            line_chars.append(chars[char_idx])
        ascii_lines.append("".join(line_chars))
        
    return ascii_lines

def get_placeholder_ascii():
    # A beautiful cyberpunk avatar placeholder ASCII
    placeholder = """
      .----------------.
     /  ..---------..  \\
    /  /           \\  \\
   |  /   _     _   \\  |
   |  |  (o)   (o)  |  |
   |  |    _____    |  |
   |  \\   \\___/   /  |
    \\  \\           /  /
     \\  ''---------''  /
      '----------------'
    """
    return [line for line in placeholder.splitlines() if line.strip()]

def escape_xml(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def generate_svg(ascii_lines, output_path="profile.svg"):
    # SVG Dimensions
    svg_width = 1000
    svg_height = 550
    
    primary = CONFIG["theme_color_primary"]
    secondary = CONFIG["theme_color_secondary"]
    accent = CONFIG["theme_color_accent"]
    font = CONFIG["font_family"]
    
    # Format ASCII text lines into SVG tspan
    ascii_xml_lines = []
    start_y = 65
    line_height = 9.5
    
    # Limit to max 45 lines to fit inside the visual map panel
    max_ascii_lines = 45
    trimmed_ascii = ascii_lines[:max_ascii_lines]
    
    for i, line in enumerate(trimmed_ascii):
        y_pos = start_y + (i * line_height)
        escaped_line = escape_xml(line)
        ascii_xml_lines.append(
            f'<tspan x="40" y="{y_pos:.2f}">{escaped_line}</tspan>'
        )
    
    ascii_tspans = "\n".join(ascii_xml_lines)
    
    # Format system info key-value pairs
    system_info = [
        ("Subject", CONFIG["name"]),
        ("Role", CONFIG["role"]),
        ("Origin", CONFIG["origin"]),
        ("Education", CONFIG["education"]),
        ("Status", CONFIG["status"]),
        ("ToolChain", CONFIG["toolchain"]),
        ("", ""), # Empty line spacer
        ("Core.Lang", CONFIG["core_lang"]),
        ("Core.Frontend", CONFIG["core_frontend"]),
        ("Core.Backend", CONFIG["core_backend"]),
        ("Core.Database", CONFIG["core_database"]),
        ("Core.Infra", CONFIG["core_infra"]),
        ("", ""), # Spacer
        ("Contact.Mail", CONFIG["contact_email"]),
        ("Contact.Web", CONFIG["contact_portfolio"]),
        ("Contact.In", CONFIG["contact_linkedin"]),
        ("Contact.Git", CONFIG["contact_github"]),
    ]
    
    info_xml_lines = []
    info_start_y = 80
    info_line_height = 22
    
    # Generate line-by-line clipPaths for the typing animation
    clip_paths = []
    typing_durations = []
    
    current_delay = 0.5  # animation delay start
    
    for idx, (key, value) in enumerate(system_info):
        y_pos = info_start_y + (idx * info_line_height)
        
        # Clip path ID for this line
        clip_id = f"info_line_{idx}"
        
        if key == "" and value == "":
            # Just spacer, no text
            continue
            
        # Standard layout: Label : Value with leader dots
        # E.g. "  Role: ......................... Developer"
        # Total characters roughly 60
        label = f"  {key}"
        label_len = len(label)
        
        # Leader dots
        leader_dots = "." * (22 - label_len) if label_len < 22 else ".."
        
        line_text = f"{label} {leader_dots} {value}"
        escaped_line = escape_xml(line_text)
        
        # We wrap keys in coloring by splitting in SVG, or just render it as a single line.
        # To make it gorgeous, let's write it with colored spans:
        # <tspan fill="#10B981">key</tspan> <tspan fill="#6B7280">...</tspan> <tspan fill="#F3F4F6">value</tspan>
        # Let's generate the text node with sub-tspans
        text_xml = (
            f'<text x="470" y="{y_pos:.2f}" fill="#9CA3AF" font-size="13" clip-path="url(#{clip_id})">'
            f'<tspan fill="{accent}" font-weight="bold">{escape_xml(key)}</tspan>'
            f'<tspan fill="#4B5563">{leader_dots}</tspan> '
            f'<tspan fill="#F3F4F6">{escape_xml(value)}</tspan>'
            f'</text>'
        )
        info_xml_lines.append(text_xml)
        
        # Create typing animation clip path
        clip_paths.append(
            f'<clipPath id="{clip_id}">'
            f'<rect x="470" y="{y_pos - 15:.2f}" width="0" height="24">'
            f'<animate attributeName="width" from="0" to="500" dur="0.5s" begin="{current_delay:.2f}s" fill="freeze"/>'
            f'</rect>'
            f'</clipPath>'
        )
        current_delay += 0.12 # Delay before typing the next line
        
    clip_paths_xml = "\n  ".join(clip_paths)
    info_text_xml = "\n  ".join(info_xml_lines)
    
    # SVG Template
    svg_template = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{svg_width}" height="{svg_height}" viewBox="0 0 {svg_width} {svg_height}">
  <defs>
    <!-- Background Gradient -->
    <radialGradient id="bgGlow" cx="50%" cy="30%" r="80%">
      <stop offset="0%" stop-color="#0F172A"/>
      <stop offset="100%" stop-color="#020617"/>
    </radialGradient>
    
    <!-- Neon Border Gradient -->
    <linearGradient id="borderGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{primary}"/>
      <stop offset="50%" stop-color="{secondary}"/>
      <stop offset="100%" stop-color="{accent}"/>
    </linearGradient>

    <!-- Animated ASCII Gradient -->
    <linearGradient id="asciiGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{primary}">
        <animate attributeName="stop-color" values="{primary};{secondary};{primary}" dur="6s" repeatCount="indefinite"/>
      </stop>
      <stop offset="100%" stop-color="{secondary}">
        <animate attributeName="stop-color" values="{secondary};{primary};{secondary}" dur="6s" repeatCount="indefinite"/>
      </stop>
    </linearGradient>
    
    <!-- Scanlines Pattern -->
    <pattern id="scanlines" width="4" height="4" patternUnits="userSpaceOnUse">
      <rect width="4" height="1" fill="#FFFFFF" opacity="0.03"/>
    </pattern>
    
    <!-- Soft Glow Filter -->
    <filter id="softGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <!-- Typing Animation Clip Paths -->
    {clip_paths_xml}
  </defs>

  <style>
    @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;700&amp;display=swap');
    .term-text {{
      font-family: {font};
      white-space: pre;
    }}
    .glow-border {{
      filter: drop-shadow(0 0 4px {primary}40);
    }}
  </style>

  <!-- Background -->
  <rect width="{svg_width}" height="{svg_height}" fill="url(#bgGlow)" rx="12"/>
  <rect width="{svg_width}" height="{svg_height}" fill="url(#scanlines)" rx="12"/>

  <!-- Outer Window Shell -->
  <g class="glow-border">
    <!-- Main Outer Border -->
    <rect x="15" y="15" width="{svg_width - 30}" height="{svg_height - 30}" fill="none" stroke="url(#borderGrad)" stroke-width="1.5" rx="8"/>
  </g>

  <!-- Window Header Title Bar -->
  <g>
    <!-- Window Controls (Mac Style) -->
    <circle cx="40" cy="35" r="5" fill="#EF4444"/>
    <circle cx="55" cy="35" r="5" fill="#F59E0B"/>
    <circle cx="70" cy="35" r="5" fill="#10B981"/>
    
    <!-- Terminal Command/Title -->
    <text x="50%" y="40" fill="#64748B" font-size="12" font-family="{font}" text-anchor="middle">
      {CONFIG["username"]}@devos ~ % ./profile.sh --live
    </text>
    
    <!-- Scanning Status -->
    <text x="{svg_width - 90}" y="40" fill="#EF4444" font-size="11" font-family="{font}" font-weight="bold" letter-spacing="1">
      ● SCANNING
      <animate attributeName="opacity" values="1;0.2;1" dur="1.5s" repeatCount="indefinite"/>
    </text>
  </g>

  <!-- Inner Panels -->
  <!-- Left Panel: VISUAL.MAP (ASCII Art) -->
  <g>
    <!-- Border -->
    <rect x="25" y="60" width="410" height="460" fill="#030712" fill-opacity="0.6" stroke="#1E293B" stroke-width="1" rx="6"/>
    <!-- Label -->
    <rect x="40" y="52" width="90" height="16" fill="#0B1329" stroke="#1E293B" stroke-width="1" rx="3"/>
    <text x="85" y="64" fill="{primary}" font-size="10" font-family="{font}" font-weight="bold" text-anchor="middle" letter-spacing="1">VISUAL.MAP</text>
    
    <!-- ASCII Art Display -->
    <text class="term-text" font-size="7.5" line-height="{line_height}" fill="url(#asciiGrad)" font-weight="bold" filter="url(#softGlow)">
      {ascii_tspans}
    </text>
  </g>

  <!-- Right Panel: SYSTEM.INFO (Details) -->
  <g>
    <!-- Border -->
    <rect x="450" y="60" width="525" height="460" fill="#030712" fill-opacity="0.6" stroke="#1E293B" stroke-width="1" rx="6"/>
    <!-- Label -->
    <rect x="465" y="52" width="100" height="16" fill="#0B1329" stroke="#1E293B" stroke-width="1" rx="3"/>
    <text x="515" y="64" fill="{secondary}" font-size="10" font-family="{font}" font-weight="bold" text-anchor="middle" letter-spacing="1">SYSTEM.INFO</text>

    <!-- Title inside panel -->
    <text x="470" y="86" fill="{secondary}" font-size="14" font-family="{font}" font-weight="bold">
      {CONFIG["username"]}@devos
    </text>
    
    <!-- Divider Line under user heading -->
    <line x1="470" y1="94" x2="955" y2="94" stroke="#334155" stroke-dasharray="3,3"/>

    <!-- Key-Value Lines -->
    {info_text_xml}

    <!-- Live Stats Note at Bottom -->
    <text x="470" y="490" fill="#64748B" font-size="11" font-family="{font}">
      - Live Stats ---------------------------------------
    </text>
    <text x="470" y="508" fill="#9CA3AF" font-size="12" font-family="{font}">
      See live GitHub stats badges below in README ↓
    </text>
  </g>
</svg>
"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_template)
    print(f"Successfully generated profile SVG: {output_path}")

def main():
    print("Cyberpunk Terminal Profile SVG Generator")
    print("---------------------------------------------")
    
    image_name = "portrait.png"
    if not os.path.exists(image_name):
        image_name = "portrait.jpg"
        
    if os.path.exists(image_name):
        print(f"Found portrait image: '{image_name}'. Converting to ASCII...")
        # Width 55 works best for the 410px wide panel
        ascii_lines = image_to_ascii(image_name, width=55, invert=True)
        # Write ASCII output to portrait.txt for review
        with open("portrait.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(ascii_lines))
        print("Saved raw ASCII art to 'portrait.txt' for reference.")
    else:
        print("No 'portrait.png' or 'portrait.jpg' found.")
        print("Generating SVG with default cyberpunk placeholder avatar.")
        ascii_lines = get_placeholder_ascii()
        
    generate_svg(ascii_lines, "profile.svg")
    print("\nNext Steps:")
    print("1. Customize the metadata CONFIG at the top of this script.")
    print("2. Put a transparent portrait image in this folder named 'portrait.png'.")
    print("3. Run: python build_profile.py")
    print("4. Upload the generated 'profile.svg' to your GitHub profile repository.")

if __name__ == "__main__":
    main()
