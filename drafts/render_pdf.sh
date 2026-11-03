#!/bin/bash
# Render a Markdown deliverable to PDF: pandoc -> HTML -> headless Chrome.
# Usage: bash drafts/render_pdf.sh memo.md memo.pdf [font-size, default 10.5pt]
# Optional EXTRA_CSS env var is appended (used for the 1-page process note).
set -e
src="$1"; out="$2"; size="${3:-10.5pt}"; dir="$(cd "$(dirname "$0")" && pwd)"
tmp="$(mktemp -d)"
printf '<style>html{font-size:%s}%s</style>\n' "$size" "${EXTRA_CSS:-}" > "$tmp/size.html"
pandoc "$src" -s --css "$dir/memo.css" --embed-resources --metadata pagetitle=Memo -H "$tmp/size.html" -o "$tmp/doc.html"
python3 - "$tmp/doc.html" "$PWD/$out" <<'PY'
import subprocess, sys
chrome = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
subprocess.run([chrome, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                f"--print-to-pdf={sys.argv[2]}", "file://" + sys.argv[1]],
               check=True, timeout=90, capture_output=True)
PY
python3 -c "import re,sys; d=open(sys.argv[1],'rb').read(); print(sys.argv[1], 'pages:', len(re.findall(rb'/Type\s*/Page[^s]', d)))" "$out"
