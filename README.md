# static-www-allangeske-ca

A static copy of **[www.allangeske.ca](https://www.allangeske.ca)**, "Allan Geske, Printmaker": the blog, image galleries and RSS feed of Allan Geske's printmaking site.

The site was built with Drupal 6. In 2022 it was turned into plain files with HTTrack and served that way from a VPS. That copy is archived privately in `stungeye/archive-www.allangeske.ca`; this repo holds what is served.

## What's in `site/`

* **The HTTrack mirror** (made 2022-03-03): every file of the archive's `source/` at `7d63abf`, byte for byte, except `.htaccess` (`tools/snapshot.py`). HTTrack's file names are kept, including the ones for query-string pages (`index2e76.html` and the like) and image names with spaces.
* **Changes from the old site**, each made by a script in `tools/`:
  * `tools/strip_ga.py`: the Google Analytics tag (`ga.js`, `UA-76943-4`) is removed from all 204 pages.
* `site/404.html`: a minimal not-found page (new).

Rebuild from scratch: `python3 -I tools/snapshot.py <archive-www.allangeske.ca checkout>`, then `python3 -I tools/strip_ga.py --apply`, then add `site/404.html`.

## Hosting

Served from **Cloudflare Workers static assets** (Free plan; the largest file is under 1 MB).

* **Worker:** `static-www-allangeske-ca`, account `Stungeye@gmail.com's Account`.
* **Deploy:** Workers Builds: every push to `main` deploys. No build command; deploy command `npx wrangler deploy`. Only `site/` is uploaded.
* **Serving:** `html_handling: auto-trailing-slash` (`/blog` serves `blog.html`, `/blog.html` 307s to `/blog`). This replaces the old `.htaccess`, which 301'd extensionless URLs to `.html`. `not_found_handling: 404-page` (`site/404.html`).
* **workers.dev:** on until the cutover. Per-version preview URLs are off.
* **Route (since 2026-10-31):** `www.allangeske.ca/*` on zone `allangeske.ca` (moved from DigitalOcean DNS to Cloudflare the same day), over a proxied `www` record. Rollback: delete the route.
* **Apex:** `allangeske.ca` 301s to `https://www.allangeske.ca` with the path and query kept, by a Single Redirect rule in the zone (not by this Worker).
