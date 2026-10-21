# Cynthia Udoh — Portfolio

Project management and communications for VC teams and founders.

## Content editor

Open https://app.pagescms.org, sign in with GitHub, and choose **Amalearner/cynthia-udoh-portfolio → main**. Each page and section has editable fields. Save content to trigger the automated GitHub Pages deployment.

Read [EDITING.md](EDITING.md) for the simple update workflow and the one-time GitHub Pages and editor-access settings.

## Local preview

Run `python build-pages.py`, then `python -m http.server --directory _site 8000`. Open http://localhost:8000.

## Validation

Run `python test_content.py`. The test exercises text edits, section visibility, global social links, interactive ring notes, sketch content and local links.

## Structure

- `content/pages/`: editable copy for 25 pages
- `content/settings.json`: shared navigation/footer/social links
- `content/interactions.json`: ring notes, process stages and sketch decks
- `.pages.yml`: browser-editor fields
- `templates.json`: preserved design and page structure
- `build-pages.py`: static-site renderer
- `.github/workflows/pages.yml`: automatic checks and publishing

Client descriptions identify Cynthia’s project-management contribution within the Tony & Co creative team. Existing blog draft and illustrative sketch labels are retained.
