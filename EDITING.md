# Editing your portfolio

## Everyday updates

1. Open https://app.pagescms.org and sign in with GitHub.
2. Choose **Amalearner / cynthia-udoh-portfolio** and the **main** branch.
3. Choose the page you want from the sidebar.
4. Open a section. Edit its headings, paragraphs, button destinations or images. Keep the existing section structure.
5. Click **Save**. GitHub Actions checks and publishes the website automatically. Wait for the green deployment check before refreshing the live site.

## What you can edit

- **Navigation, footer & social links:** shared navigation text, menu links, footer message and social profiles; these apply across all pages.
- **Home, About, Work, Contact and other pages:** copy, images, image descriptions, links and section visibility. Search/browser titles and descriptions are at the top of each page editor.
- **Project pages:** project titles, responsibilities, activities, status and working outputs.
- **Blog pages:** all existing essay headings, paragraphs and article details. The homepage and Field Notes listings have their own card text; update those when changing an article title or summary.
- **Ring notes, process & sketch notebooks:** popup copy, the four delivery-stage descriptions, notebook content and individual sketch cards/roadmaps. Keep the four delivery stages and eight notebook covers. You may edit sketch contents and add/remove slides inside each notebook.
- **Media:** upload images into the assets folder; choose them in page image fields. Add a useful image description for accessibility.
- **Show this section:** turn a section on or off. If hiding a section linked from navigation, update that link too.

Content editing does not change the visual design, handwritten typography, animations or mobile layout. New page types, new layouts and adding/removing notebook covers require a design/code change.

## One-time editor access

Pages CMS needs access to this repository. On the GitHub App authorization screen, choose **Only select repositories** and select **cynthia-udoh-portfolio**. You do not need to grant access to your other repositories. Review and approve the requested permissions yourself.

## One-time GitHub Pages setting

In the repository, choose **Settings → Pages → Build and deployment → Source → GitHub Actions**. The workflow is already included. Use **Actions → Deploy portfolio to GitHub Pages → Run workflow** if no run starts after setting the source.

## Technical notes

The design is in templates.json. Editable content lives in content/. The build script uses Python's standard library and renders the site into _site/. The workflow publishes only that generated output. There are no passwords, API keys or CMS secrets in this repository.

The original portrait is in assets/cynthia.jpg. You can replace it with an uploaded JPG, PNG or WebP through the image fields.
