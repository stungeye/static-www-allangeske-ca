"""Remove the Google Analytics tag (ga.js, UA-76943-4) from every page in site/ (PLAN F11).
Usage: python3 -I tools/strip_ga.py [--apply]   (from the repo root; dry run by default)

Every page ends with the same two inline scripts, the ga.js loader and the pageTracker block, right
before </body>. Both are removed, with the whitespace before them. The run refuses to apply if any file
still mentions Google Analytics afterwards, or if a page has the tag in another shape."""
import os, re, sys

APPLY = '--apply' in sys.argv[1:]
TAG = re.compile(
    rb'[ \t\r\n]*<script type="text/javascript">\r?\n'
    rb'var gaJsHost = \(\("https:" == document\.location\.protocol\) \? "https://ssl\." : "http://www\."\);\r?\n'
    rb'document\.write\(unescape\("%3Cscript src=\'" \+ gaJsHost \+ "google-analytics\.com/ga\.js\' type=\'text/javascript\'%3E%3C/script%3E"\)\);\r?\n'
    rb'</script>\r?\n'
    rb'<script type="text/javascript">\r?\n'
    rb'var pageTracker = _gat\._getTracker\("UA-76943-4"\);\r?\n'
    rb'pageTracker\._initData\(\);\r?\n'
    rb'pageTracker\._trackPageview\(\);\r?\n'
    rb'</script>(?=\r?\n</body>)')
LEFT = re.compile(rb'google-analytics|_gat\b|pageTracker|UA-76943')

changed, left, writes = 0, [], {}
for root, _, fs in os.walk('site'):
    for f in sorted(fs):
        p = os.path.join(root, f)
        d = open(p, 'rb').read()
        if not LEFT.search(d):
            continue
        new, n = TAG.subn(b'', d)
        if n:
            changed += 1
            writes[p] = new
        if n != 1 or LEFT.search(new):
            left.append((p, n))
print(f'pages with the tag removed: {changed}; problems: {len(left)}')
for p, n in left[:20]:
    print('  ', n, p)
if APPLY:
    assert not left, 'refusing to apply'
    for p, d in writes.items():
        open(p, 'wb').write(d)
    print('applied')
