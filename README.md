# Min Namgung's Homepage

Source for https://minnamgung.github.io/.

## Updating content

Edit the Markdown files in `content/` and push to `master`. GitHub Actions runs `python3 build.py` and publishes the generated page, stylesheet, and assets to GitHub Pages. No packages or Jekyll dependencies are needed.

| File | Content |
| --- | --- |
| `content/profile.md` | Name, affiliation, email text, professional profile links, CV |
| `content/about.md` | Biography and research interests |
| `content/news.md` | News updates |
| `content/publications/*.md` | One selected paper per file; filename order determines display order |
| `content/recent-work.md` | Broad current research description |
| `content/service.md` | PC and reviewing service |
| `assets/Min_CV.pdf` | Downloadable CV |
| `assets/portrait.jpg` | Portrait |
| `assets/publications/` | Selected publication figures |
| `style.css` | Typography, colors, layout, responsive styles |
| `build.py` | Page structure and Markdown-to-HTML build |

The small Markdown renderer supports headings, paragraphs, flat lists, bold, italic, links, and hard line breaks. HTML, nested lists, and tables are not supported inside content files. Publication front matter supports `year`, `venue`, `type`, `selected`, and optional `image` and `image_alt` fields.

## Local preview

```sh
python3 build.py
python3 -m http.server 8000 --bind 127.0.0.1
```

Open http://localhost:8000. Run the build again after editing Markdown and refresh the page. Stop the server with Ctrl+C.

## Deployment

GitHub Pages uses the GitHub Actions publishing source. The workflow in `.github/workflows/deploy.yml` runs on pushes to `master` or manual dispatch. Pull requests run the build without deploying. Only `index.html`, `style.css`, and `assets/` are included in the public deployment artifact. `index.html` is generated; edit Markdown or `build.py` instead.

The prior Jekyll version remains in Git history. Source and deployment use the existing `master` branch; no additional source branch is required.

## Asset provenance

The portrait comes from the original MinNamgung.github.io repository; its license is retained in `SOURCE-LICENSE`. GELATTO's figure comes from the supplied presentation. Transit for All's figure comes from its public manuscript. The CV is the supplied November 2026 version. This site uses system fonts and has no analytics or external runtime dependencies.
