#!/usr/bin/env python3
import json
import os
import subprocess
import time
import sys

def read_scheme(path):
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except Exception:
        return None

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def update_spicetify(scheme, config_dir):
    colors = scheme['colours']
    color_ini_path = os.path.join(config_dir, "spicetify/Themes/caelestia/color.ini")
    
    # Mapping based on observation
    # scheme keys: onSurface, onSurfaceVariant, surface, surfaceContainer, surfaceContainerHigh, primary, outline, shadow
    
    # Simple mapping
    mapping = {
        "text": colors.get("onSurface", "e6e2dd"),
        "subtext": colors.get("onSurfaceVariant", "cbc6b9"),
        "main": colors.get("surface", "141311"),
        "sidebar": colors.get("surfaceContainer", "201f1d"),
        "player": colors.get("surfaceContainerHigh", "2b2a27"),
        "card": colors.get("surfaceContainer", "201f1d"),
        "shadow": colors.get("shadow", "000000"),
        "selected-row": colors.get("onSurface", "e6e2dd"),
        "button": colors.get("primary", "b3ac8b"),
        "button-active": colors.get("primary", "b3ac8b"),
        "button-disabled": colors.get("outline", "949085"),
        "tab-active": colors.get("surfaceContainerHighest", "363532"),
        "notification": colors.get("outline", "949085"),
        "notification-error": colors.get("error", "ffb4ab"),
        "misc": colors.get("primary", "b3ac8b"),
        "highlight": colors.get("primary", "b3ac8b"),
        "main-elevated": colors.get("surfaceContainerHigh", "2b2a27"),
        "highlight-elevated": colors.get("surfaceContainerHighest", "363532"),
    }
    
    content = "[caelestia]\n"
    for key, value in mapping.items():
        content += f"{key:<20} = {value}\n"
        
    try:
        with open(color_ini_path, 'w') as f:
            f.write(content)
        
        # Apply spicetify
        subprocess.run(["spicetify", "apply", "-n"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("Updated Spicetify theme.")
    except Exception as e:
        print(f"Failed to update Spicetify: {e}")

def update_discord(scheme, config_dir):
    colors = scheme['colours']
    theme_path = os.path.join(config_dir, "Equicord/themes/caelestia.theme.css")
    
    # If file doesn't exist, we might want to skip or create it from template
    # We will assume it exists as per user setup
    
    if not os.path.exists(theme_path):
        print(f"Discord theme not found at {theme_path}")
        return

    # We need to construct the CSS variables
    # Based on cat output of caelestia.theme.css
    
    def rgb_str(hex_c):
        r, g, b = hex_to_rgb(hex_c)
        return f"rgb({r}, {g}, {b})"
        
    c = colors
    
    # Helper to safe get
    def get(k, default): return c.get(k, default)
    
    # We will reconstruct the file content. 
    # Since we can't easily parse and replace CSS variables without a parser, 
    # and the file has a specific structure with imports, we will read the file,
    # find the :root block, and replace it, or just overwrite the file if we know the structure.
    # But overwriting might lose user customizations if they edited it.
    # However, since this is a "synced" theme, overwriting is expected.
    
    # We'll use a template based on the previous file content
    
    css_content = f"""/**
 * @name Midnight (Caelestia)
 * @description A dark, rounded discord theme. Caelestia scheme colours.
 * @author refact0r, esme, anubis
 * @version 1.6.2
 * @invite nz87hXyvcy
 * @website https://github.com/refact0r/midnight-discord
 * @authorId 508863359777505290
 * @authorLink https://www.refact0r.dev
*/
@import url(\"https://refact0r.github.io/midnight-discord/build/midnight.css\");
body {{
  /* font, change to '' for default discord font */
  --font: \"figtree\";
  /* sizes */
  --gap: 12px; /* spacing between panels */
  --divider-thickness: 4px; /* thickness of unread messages divider and highlighted message borders */
  --border-thickness: 1px; /* thickness of borders around main panels. DOES NOT AFFECT OTHER BORDERS */
  /* animation/transition options */
  --animations: on; /* turn off to disable all midnight animations/transitions */
  --list-item-transition: 0.2s ease; /* transition for list items */
  --dms-icon-svg-transition: 0.4s ease; /* transition for the dms icon */
  /* top bar options */
  --top-bar-height: var(
      --gap
  ); /* height of the titlebar/top bar (discord default is 36px, 24px recommended if moving/hiding top bar buttons) */
  --top-bar-button-position: hide; /* off: default position, hide: hide inbox/support buttons completely, serverlist: move inbox button to server list, titlebar: move inbox button to titlebar (will hide title) */
  --top-bar-title-position: hide; /* off: default centered position, hide: hide title completely, left: left align title (like old discord) */
  --subtle-top-bar-title: off; /* off: default, on: hide the icon and use subtle text color (like old discord) */
  /* window controls */
  --custom-window-controls: on; /* turn off to use discord default window controls */
  --window-control-size: 14px; /* size of custom window controls */
  /* dms button icon options */
  --custom-dms-icon: custom; /* off: use default discord icon, hide: remove icon entirely, custom: use custom icon */
  --dms-icon-svg-url: url(\"https://upload.wikimedia.org/wikipedia/commons/c/c4/Font_Awesome_5_solid_moon.svg\"); /* icon svg url. MUST BE A SVG. */
  --dms-icon-svg-size: 90%; /* size of the svg (css mask-size) */
  --dms-icon-color-before: var(--icon-secondary); /* normal icon color */
  --dms-icon-color-after: var(--white); /* icon color when button is hovered/selected */
  /* dms button background options */
  --custom-dms-background: off; /* off: default discord icon, hide: remove icon entirely, custom: use custom icon */
  --dms-background-image-url: url(\"\"); /* url of the background image */
  --dms-background-image-size: cover; /* size of the background image (css background-size) */
  --dms-background-color: linear-gradient(
      70deg,
      var(--blue-2),
      var(--purple-2),
      var(--red-2)
  ); /* fixed color/gradient (css background) */
  /* background image options */
  --background-image: off; /* turn on to use a background image */
  --background-image-url: url(\"\"); /* url of the background image */
  /* transparency/blur options */
  /* NOTE: TO USE TRANSPARENCY/BLUR, YOU MUST HAVE TRANSPARENT BG COLORS. FOR EXAMPLE: --bg-4: hsla(220, 15%, 10%, 0.7); */
  --transparency-tweaks: off; /* turn on to remove some elements for better transparency */
  --remove-bg-layer: off; /* turn on to remove the base --bg-3 layer for use with window transparency (WILL OVERRIDE BACKGROUND IMAGE) */
  --panel-blur: off; /* turn on to blur the background of panels */
  --blur-amount: 12px; /* amount of blur */
  --bg-floating: #{get("base", "141311")}; /* you can set this to a more opaque color if floating panels look too transparent */
  /* chatbar options */
  --custom-chatbar: aligned; /* off: default chatbar, aligned: chatbar aligned with the user panel, separated: chatbar separated from chat */
  --chatbar-height: 47px; /* height of the chatbar (52px by default, 47px recommended for aligned, 56px recommended for separated) */
  --chatbar-padding: 8px; /* padding of the chatbar. only applies in aligned mode. */
  /* other options */
  --small-user-panel: off; /* turn on to make the user panel smaller like in old discord */
}}

/* color options */
:root {{
  --colors: on; /* turn off to use discord default colors */
  /* text colors */
  --text-0: #{get("onPrimary", "24210a")}; /* text on colored elements */
  --text-1: rgb(232.5, 228.9, 224.4); /* bright text on colored elements */
  --text-2: rgb(231.25, 227.45, 222.7); /* headings and important text */
  --text-3: #{get("onSurface", "e6e2dd")}; /* normal text */
  --text-4: #{get("outline", "949085")}; /* icon buttons and channels */
  --text-5: #{get("outlineVariant", "949085")}; /* muted channels/chats and timestamps */
  /* background and dark colors */
  --bg-1: #{get("surfaceContainerHighest", "363532")}; /* dark buttons when clicked */
  --bg-2: #{get("surfaceContainerHigh", "2b2a27")}; /* dark buttons */
  --bg-3: #{get("base", "141311")}; /* spacing, secondary elements */
  --bg-4: #{get("surface", "201f1d")}; /* main background color */
  --hover: rgba(230, 226, 221, 0.08); /* channels and buttons when hovered */
  --active: rgba(230, 226, 221, 0.1); /* channels and buttons when clicked or selected */
  --active-2: rgba(230, 226, 221, 0.2); /* extra state for transparent buttons */
  --message-hover: rgba(230, 226, 221, 0.08); /* messages when hovered */
  /* accent colors */
  --accent-1: var(--blue-1); /* links and other accent text */
  --accent-2: var(--blue-2); /* small accent elements */
  --accent-3: var(--blue-3); /* accent buttons */
  --accent-4: var(--blue-4); /* accent buttons when hovered */
  --accent-5: var(--blue-5); /* accent buttons when clicked */
  --accent-new: #{get("error", "ffb4ab")}; /* stuff that's normally red like mute/deafen buttons */
  --mention: linear-gradient(
      to right,
      color-mix(in hsl, var(--blue-2), transparent 90%) 40%,
      transparent
  ); /* background of messages that mention you */
  --mention-hover: linear-gradient(
      to right,
      color-mix(in hsl, var(--blue-2), transparent 95%) 40%,
      transparent
  ); /* background of messages that mention you when hovered */
  --reply: linear-gradient(
      to right,
      color-mix(in hsl, var(--text-3), transparent 90%) 40%,
      transparent
  ); /* background of messages that reply to you */
  --reply-hover: linear-gradient(
      to right,
      color-mix(in hsl, var(--text-3), transparent 95%) 40%,
      transparent
  ); /* background of messages that reply to you when hovered */
  /* status indicator colors */
  --online: var(--green-2); /* change to #43a25a for default */
  --dnd: var(--red-2); /* change to #d83a42 for default */
  --idle: var(--yellow-2); /* change to #ca9654 for default */
  --streaming: var(--purple-2); /* change to #593695 for default */
  --offline: var(--text-4); /* change to #83838b for default offline color */
  /* border colors */
  --border-light: rgba(148, 144, 133, 0); /* light border color */
  --border: rgba(148, 144, 133, 0.2); /* normal border color */
  --button-border: rgba(148, 144, 133, 0); /* neutral border color of buttons */
  /* base colors */
  --red-1: #{get("error", "ffb4ab")};
  --red-2: rgb(255, 160.9821428571, 149.7);
  --red-3: rgb(255, 141.9642857143, 128.4);
  --red-4: rgb(255, 122.9464285714, 107.1);
  --red-5: rgb(255, 103.9285714286, 85.8);
  --green-1: #{get("green", "e5e581")};
  --green-2: rgb(225.9381578947, 225.9381578947, 114.1618421053);
  --green-3: rgb(222.8763157895, 222.8763157895, 99.3236842105);
  --green-4: rgb(219.8144736842, 219.8144736842, 84.4855263158);
  --green-5: rgb(216.7526315789, 216.7526315789, 69.6473684211);
  --blue-1: #{get("primary", "b3ac8b")};
  --blue-2: rgb(172.70625, 165.1265625, 129.39375);
  --blue-3: rgb(166.4125, 158.253125, 119.7875);
  --blue-4: rgb(160.11875, 151.3796875, 110.18125);
  --blue-5: rgb(153.7, 144.425, 100.7);
  --yellow-1: #{get("yellow", "fff1bd")};
  --yellow-2: rgb(255, 236.2909090909, 166.8);
  --yellow-3: rgb(255, 231.5818181818, 144.6);
  --yellow-4: rgb(255, 226.8727272727, 122.4);
  --yellow-5: rgb(255, 222.1636363636, 100.2);
  --purple-1: #{get("mauve", "ffad7f")};
  --purple-2: rgb(255, 160.7640625, 107.9);
  --purple-3: rgb(255, 148.528125, 88.8);
  --purple-4: rgb(255, 136.2921875, 69.7);
  --purple-5: rgb(255, 124.05625, 50.6);
}}
"""

    try:
        with open(theme_path, 'w') as f:
            f.write(css_content)
        print("Updated Discord theme.")
    except Exception as e:
        print(f"Failed to update Discord: {e}")

def main():
    scheme_dir = os.path.expanduser("~/.local/state/caelestia")
    config_dir = os.path.expanduser("~/.config")
    scheme_path = os.path.join(scheme_dir, "scheme.json")

    # Initial update
    scheme = read_scheme(scheme_path)
    if scheme:
        update_spicetify(scheme, config_dir)
        update_discord(scheme, config_dir)

    # Watch for changes
    try:
        process = subprocess.Popen(
            ['inotifywait', '-q', '-e', 'close_write,moved_to,create', '-m', scheme_dir],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL
        )

        for line in iter(process.stdout.readline, b''):
            try:
                parts = line.decode('utf-8').strip().split()
                if len(parts) >= 3 and parts[2] == 'scheme.json':
                    time.sleep(0.5) # Wait for write to finish
                    scheme = read_scheme(scheme_path)
                    if scheme:
                        update_spicetify(scheme, config_dir)
                        update_discord(scheme, config_dir)
            except Exception:
                pass
    except FileNotFoundError:
        print("inotifywait not found")
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
