# Portfolio

Personal portfolio site for Aniket Karkala. Plain HTML, CSS and JavaScript, with no frameworks.

## Layout

- `index.html`, `projects.html`, `teaching.html`, `about.html` and `projects/*.html` are generated pages.
- `data/projects.json` holds every project: name, type, size, role, description, parts and notes.
- `build.py` turns the data into pages. `css/site.css` and `js/site.js` are shared by all pages.

## Adding or editing a project

1. Edit `data/projects.json`. Copy an existing entry and change the fields. `slug` becomes the page address.
2. Run `python3 build.py`.
3. Commit and push.

Set `"featured": true` to put a project in the 3D carousel on the home page.

## Before going public

Every page carries `<meta name="robots" content="noindex, nofollow">` so search engines skip the site. Remove that line from `page()` in `build.py` and rebuild when you want it indexed.
