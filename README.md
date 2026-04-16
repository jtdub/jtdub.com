# jtdub.com

Personal site for James Williams -- network software engineer by profession, anthropologist by education.

Built with [Astro](https://astro.build) and hosted on [Cloudflare Pages](https://pages.cloudflare.com).

## Architecture

The site uses a dual-zone editorial design system with two distinct visual personalities under one shell:

- **Field & Research** -- anthropology, archaeology, fieldwork, expeditions, publications, community science, photography
- **Engineering & Code** -- network automation, open source, Python, Linux, apps, resume

Each zone carries its own accent color (terracotta for field, deep ink-blue for engineering) while sharing the same typography (Fraunces serif, Inter sans, JetBrains Mono) and layout primitives.

## Stack

- **Framework**: Astro 6 with Content Collections
- **Styling**: Hand-rolled CSS with custom properties, no framework
- **Fonts**: Self-hosted via @fontsource-variable (Fraunces, Inter, JetBrains Mono)
- **Search**: Pagefind (post-build indexing, lazy-loaded modal)
- **Images**: Cloudflare Images (imagedelivery.net)
- **Files**: Cloudflare R2 (publication PDFs)
- **Analytics**: Cloudflare Web Analytics
- **SEO**: JSON-LD, OpenGraph, Twitter Cards, RSS, Sitemap

## Development

```sh
pnpm install
pnpm dev          # start dev server at localhost:4321
pnpm build        # build to ./dist/ (includes pagefind indexing)
pnpm preview      # preview the built site
```

Search requires at least one `pnpm build` before it works in dev mode (Pagefind indexes post-build HTML).

## Content

- **Posts**: `src/content/posts/*.md` -- 135 blog posts (2009--2026) with Zod-validated frontmatter
- **Data**: `src/data/*.json` -- resume, publications, academic papers, projects, photos
- **Pages**: `src/pages/` -- zone landings, writing index, tags, about, resume, contact, apps, community science, memberships, photography

Post URLs follow the Jekyll-compatible pattern `/:year/:month/:day/:slug/` for backward compatibility.
