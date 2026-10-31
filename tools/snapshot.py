"""Build site/ for www.allangeske.ca from the private archive stungeye/archive-www.allangeske.ca.
Usage: python3 -I tools/snapshot.py <archive-www.allangeske.ca checkout>   (from the repo root)

The archive's source/ is the old server's web root: an HTTrack mirror (2022-03-03) of the Drupal 6 site,
433 static files, no PHP. Every file is copied byte for byte from commit 7d63abf, except .htaccess
(its extensionless -> .html 301 is replaced by Workers' auto-trailing-slash, which serves /blog as blog.html).
Refuses to run if site/ already exists."""
import os, subprocess, sys

src = sys.argv[1]
COMMIT = '7d63abf'
assert not os.path.exists('site'), 'site/ exists'
tree = subprocess.run(['git', '-C', src, 'ls-tree', '-r', '-z', COMMIT, 'source/'], capture_output=True, check=True).stdout
kept = skipped = 0
for entry in tree.split(b'\0'):
    if not entry:
        continue
    meta, rel = entry.split(b'\t', 1)
    mode, kind, _ = meta.split()
    assert kind == b'blob' and mode == b'100644', (meta, rel)
    rel = rel.decode()[len('source/'):]
    if os.path.basename(rel) == '.htaccess':
        skipped += 1
        continue
    data = subprocess.run(['git', '-C', src, 'cat-file', 'blob', f'{COMMIT}:source/{rel}'], capture_output=True, check=True).stdout
    dst = os.path.join('site', rel)
    os.makedirs(os.path.dirname(dst) or '.', exist_ok=True)
    open(dst, 'wb').write(data)
    kept += 1
print(f'files {kept}, skipped {skipped}')
