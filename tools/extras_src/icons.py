# Inline SVG icons (24x24, stroke = currentColor) and generated header art for tool/guide pages.
ICONS = {
 "hyrox": '<path d="M13 4a2 2 0 1 0 0 .01M7 21l3-6 3 2v4M10 15l1-5 4 3 3-1M6 11l3-3 3 1"/>',
 "str": '<path d="M3 11 12 4l9 7M5 10v10h14V10M10 20v-6h4v6"/>',
 "debt": '<path d="M4 18 9 13l4 3 7-8M15 8h5v5"/>',
 "grow": '<path d="M4 20V10M10 20V6M16 20v-8M22 20H2M16 8l3-4 3 4"/>',
 "risk": '<path d="M12 3 3 7v6c0 4 4 7 9 8 5-1 9-4 9-8V7Z M9 12l2 2 4-4"/>',
 "gift": '<path d="M4 11h16v9H4zM3 7h18v4H3zM12 7v13M12 7c-2-4-6-3-5 0M12 7c2-4 6-3 5 0"/>',
 "book": '<path d="M4 5a2 2 0 0 1 2-2h13v16H6a2 2 0 0 0-2 2zM4 21V5M8 7h7M8 11h5"/>',
 "spark": '<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5 18 18M6 18l2.5-2.5M15.5 8.5 18 6"/>',
}
def icon(name, size=24, cls=""):
    return ('<svg class="%s" width="%d" height="%d" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>') % (cls, size, size, ICONS[name])

def art(name, label, seed=1):
    """Decorative header art: gold glow, grid, a rising line and the icon. Pure inline SVG, ~1.5 KB."""
    import random
    r = random.Random(seed)
    pts, y = [], 150
    for i in range(13):
        y = max(40, min(190, y + r.randint(-26, 18)))
        pts.append("%d,%d" % (i * 50, y))
    line = " ".join(pts)
    return f'''<svg class="hart" viewBox="0 0 600 230" preserveAspectRatio="xMidYMid slice" role="img" aria-label="{label}">
<defs><radialGradient id="hg{seed}" cx="78%" cy="30%" r="65%"><stop offset="0" stop-color="#f2d77a" stop-opacity=".38"/><stop offset="1" stop-color="#f2d77a" stop-opacity="0"/></radialGradient>
<linearGradient id="hl{seed}" x1="0" x2="1"><stop offset="0" stop-color="#3fb8af"/><stop offset="1" stop-color="#f2d77a"/></linearGradient>
<linearGradient id="hf{seed}" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#d4af37" stop-opacity=".22"/><stop offset="1" stop-color="#d4af37" stop-opacity="0"/></linearGradient>
<pattern id="hp{seed}" width="30" height="30" patternUnits="userSpaceOnUse"><path d="M30 0H0V30" fill="none" stroke="#fff" stroke-opacity=".05"/></pattern></defs>
<rect width="600" height="230" fill="#0f0f13"/><rect width="600" height="230" fill="url(#hp{seed})"/><rect width="600" height="230" fill="url(#hg{seed})"/>
<polygon points="0,230 {line} 600,230" fill="url(#hf{seed})"/><polyline points="{line}" fill="none" stroke="url(#hl{seed})" stroke-width="3" class="hline"/>
<g transform="translate(430 52) scale(4.6)" fill="none" stroke="#f2d77a" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" opacity=".92">{ICONS[name]}</g>
</svg>'''
ICONS.update({
 "news": '<path d="M4 5h13v14H6a2 2 0 0 1-2-2zM17 9h3v8a2 2 0 0 1-2 2M7 9h7M7 13h7M7 16h4"/>',
 "analysis": '<path d="M4 20h16M6 16l4-5 3 3 5-7M18 7h2v2"/>',
 "markets": '<path d="M7 4v16M17 4v16M5 8h4v7H5zM15 6h4v9h-4z"/>',
 "planners": '<path d="M4 6h16v14H4zM4 10h16M8 3v5M16 3v5M8 14h3M13 14h3M8 17h3"/>',
})
