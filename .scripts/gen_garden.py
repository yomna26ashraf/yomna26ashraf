#!/usr/bin/env python3
"""Generate assets/garden.svg — a hand-designed blooming skill garden (SMIL animated)."""
import math, os

W, H = 1120, 460
GROUND = 372

# (label, petal color, center color, stem height)
FLOWERS = [
    ("SQL",          "#ff8fc0", "#ffd87a", 196),
    ("Python",       "#b79cff", "#ffd87a", 168),
    ("Power BI",     "#ffb38a", "#ff7eb6", 210),
    ("Pandas",       "#8fd0ff", "#ffd87a", 150),
    ("scikit-learn", "#8fe3c8", "#ff9eb0", 184),
    ("PyTorch",      "#ff9e7a", "#fff2c2", 162),
    ("Excel",        "#9be38f", "#ffd87a", 200),
    ("NumPy",        "#ffc59e", "#ff7eb6", 156),
]

def petals(cx, cy, color, n=8, rx=15, ry=27, dist=15):
    out = []
    for i in range(n):
        ang = (360 / n) * i
        out.append(
            f'<ellipse cx="{cx}" cy="{cy-dist}" rx="{rx}" ry="{ry}" fill="{color}" '
            f'transform="rotate({ang:.1f} {cx} {cy})" opacity="0.92"/>'
        )
    return "\n        ".join(out)

def flower(idx, x, label, petal, center, sh):
    base_y = GROUND
    head_y = base_y - sh
    delay = 0.18 * idx
    sway = 3.2 if idx % 2 == 0 else -3.2
    swaydur = 4.2 + (idx % 3) * 0.6
    # stem path (gentle S curve)
    cxoff = 14 if idx % 2 == 0 else -14
    stem_d = f"M{x},{base_y} C{x+cxoff},{base_y-sh*0.4} {x-cxoff},{base_y-sh*0.7} {x},{head_y}"
    stem_len = sh * 1.25
    leaf_y1 = base_y - sh*0.45
    leaf_y2 = base_y - sh*0.68
    return f'''
  <!-- flower: {label} -->
  <g>
    <!-- stem grows -->
    <path d="{stem_d}" fill="none" stroke="#7fc98a" stroke-width="5" stroke-linecap="round"
          stroke-dasharray="{stem_len:.0f}" stroke-dashoffset="{stem_len:.0f}">
      <animate attributeName="stroke-dashoffset" from="{stem_len:.0f}" to="0" dur="0.8s" begin="{delay:.2f}s" fill="freeze"/>
    </path>
    <!-- leaves -->
    <g opacity="0">
      <ellipse cx="{x+cxoff+12}" cy="{leaf_y1:.0f}" rx="16" ry="7" fill="#9bd6a3" transform="rotate(28 {x+cxoff+12} {leaf_y1:.0f})"/>
      <ellipse cx="{x-cxoff-12}" cy="{leaf_y2:.0f}" rx="14" ry="6" fill="#7fc98a" transform="rotate(-30 {x-cxoff-12} {leaf_y2:.0f})"/>
      <animate attributeName="opacity" from="0" to="1" dur="0.5s" begin="{delay+0.5:.2f}s" fill="freeze"/>
    </g>
    <!-- flower head (sway loop wraps bloom) -->
    <g transform="translate({x},{head_y})">
      <animateTransform attributeName="transform" additive="sum" type="rotate"
        values="0;{sway};0;{-sway};0" dur="{swaydur:.1f}s" begin="{delay+0.9:.2f}s" repeatCount="indefinite"/>
      <g transform="scale(0)">
        <animateTransform attributeName="transform" type="scale"
          values="0;1.18;0.95;1" keyTimes="0;0.6;0.85;1" dur="0.7s" begin="{delay+0.7:.2f}s" fill="freeze"/>
        {petals(0,0,petal)}
        <circle cx="0" cy="0" r="11" fill="{center}"/>
        <circle cx="0" cy="0" r="11" fill="none" stroke="#ffffff" stroke-opacity="0.55" stroke-width="2"/>
      </g>
    </g>
    <!-- name tag -->
    <g opacity="0">
      <rect x="{x-46}" y="{base_y+10}" width="92" height="26" rx="13" fill="#ffffff" stroke="{petal}" stroke-width="1.6"/>
      <text x="{x}" y="{base_y+27}" text-anchor="middle" font-family="'Segoe UI',Verdana,sans-serif"
            font-size="12.5" font-weight="700" fill="#7a4d68">{label}</text>
      <animate attributeName="opacity" from="0" to="1" dur="0.5s" begin="{delay+1.0:.2f}s" fill="freeze"/>
    </g>
  </g>'''

flowers_svg = "".join(
    flower(i, 80 + i * ((W-160)//(len(FLOWERS)-1)), lbl, p, c, sh)
    for i, (lbl, p, c, sh) in enumerate(FLOWERS)
)

# drifting clouds
clouds = ""
for cx, cy, s, dur, beg in [(220,70,1.0,26,0),(620,46,0.8,32,4),(940,82,0.9,29,9)]:
    clouds += f'''
  <g opacity="0.9" transform="translate({cx},{cy}) scale({s})">
    <animateTransform attributeName="transform" additive="sum" type="translate" values="0,0;40,0;0,0" dur="{dur}s" begin="{beg}s" repeatCount="indefinite"/>
    <ellipse cx="0" cy="0" rx="34" ry="18" fill="#ffffff"/>
    <ellipse cx="26" cy="6" rx="26" ry="15" fill="#ffffff"/>
    <ellipse cx="-24" cy="6" rx="22" ry="13" fill="#fdf2fb"/>
  </g>'''

# floating hearts rising
hearts = ""
for hx, beg, col in [(160,0,"#ff8fc0"),(520,2.2,"#b79cff"),(860,1.2,"#ffb38a"),(1010,3.0,"#ff7eb6")]:
    hearts += f'''
  <g transform="translate({hx},{GROUND-20})">
    <path d="M0,2 C0,-3 -7,-3 -7,2 C-7,7 0,10 0,13 C0,10 7,7 7,2 C7,-3 0,-3 0,2 Z" fill="{col}" opacity="0">
      <animate attributeName="opacity" values="0;0.9;0" dur="5s" begin="{beg}s" repeatCount="indefinite"/>
      <animateTransform attributeName="transform" type="translate" values="0,0;6,-120" dur="5s" begin="{beg}s" repeatCount="indefinite"/>
    </path>
  </g>'''

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="Skill garden — every flower is a tool Yomna builds with">
  <defs>
    <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#fff6fc"/>
      <stop offset="55%" stop-color="#fdeefb"/>
      <stop offset="100%" stop-color="#eef7f0"/>
    </linearGradient>
    <linearGradient id="grass" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#dff3e2"/>
      <stop offset="100%" stop-color="#cfeccf"/>
    </linearGradient>
    <radialGradient id="sun" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#fff3c4"/>
      <stop offset="100%" stop-color="#ffd87a"/>
    </radialGradient>
  </defs>

  <rect x="0" y="0" width="{W}" height="{H}" rx="22" fill="url(#sky)"/>

  <!-- sun with rotating rays -->
  <g transform="translate({W-92},78)">
    <g stroke="#ffe39b" stroke-width="4" stroke-linecap="round">
      <g>
        <animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="40s" repeatCount="indefinite"/>
        {''.join(f'<line x1="0" y1="-44" x2="0" y2="-56" transform="rotate({a})"/>' for a in range(0,360,30))}
      </g>
    </g>
    <circle r="34" fill="url(#sun)"/>
    <circle r="34" fill="none" stroke="#fff" stroke-opacity="0.5" stroke-width="2"/>
  </g>
{clouds}

  <!-- ground -->
  <path d="M0,{GROUND} Q{W/2},{GROUND-26} {W},{GROUND} L{W},{H} L0,{H} Z" fill="url(#grass)"/>
  <path d="M0,{GROUND} Q{W/2},{GROUND-26} {W},{GROUND}" fill="none" stroke="#bfe5c4" stroke-width="3"/>
{hearts}
{flowers_svg}

  <!-- caption -->
  <text x="34" y="46" font-family="'Segoe UI',Verdana,sans-serif" font-size="17" font-weight="800" fill="#c0539a">my little skill garden</text>
  <text x="34" y="68" font-family="'Segoe UI',Verdana,sans-serif" font-size="12.5" fill="#9a6f88">every flower is a tool i actually build with — and it keeps growing</text>
</svg>
'''

out = os.path.join(os.path.dirname(__file__), "..", "assets", "garden.svg")
with open(out, "w", encoding="utf-8") as f:
    f.write(svg)
print("wrote", os.path.abspath(out), len(svg), "bytes")
