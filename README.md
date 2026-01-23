# UltraWork Blog

A modern, high-performance blog built with [Astro](https://astro.build), [TypeScript](https://www.typescriptlang.org/), [Tailwind CSS](https://tailwindcss.com/), and [MDX](https://mdxjs.com/).

## ✨ Features

### Core Functionality
- ✅ **100/100 Lighthouse Performance** - Optimized for Core Web Vitals
- ✅ **MDX Support** - Write rich, interactive content with MDX
- ✅ **Syntax Highlighting** - Beautiful code blocks with Shiki
- ✅ **SEO Optimized** - Open Graph, Twitter Cards, Schema.org structured data

### Content Management
- ✅ **Tags System** - Tag filtering and tag pages
- ✅ **Categories System** - Category filtering and category pages
- ✅ **Search Functionality** - Client-side search with Fuse.js
- ✅ **Reading Time** - Automatic reading time calculation
- ✅ **Related Posts** - Content recommendations based on tags/categories

### User Experience
- ✅ **Dark Mode** - Theme toggle with system preference detection
- ✅ **Responsive Design** - Mobile-first design with hamburger menu
- ✅ **Table of Contents** - Auto-generated navigation for long posts
- ✅ **Reading Progress** - Sticky scroll progress indicator
- ✅ **Social Sharing** - Share buttons for Twitter, LinkedIn, Email

### Technical
- ✅ **RSS Feed** - Automatic RSS feed generation
- ✅ **Sitemap** - SEO-friendly sitemap
- ✅ **TypeScript** - Full type safety
- ✅ **Tailwind CSS** - Utility-first styling
- ✅ **Image Optimization** - Automatic image optimization with Astro Assets

## 🚀 Quick Start

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## 📁 Project Structure

```
├── public/           # Static assets
├── src/
│   ├── components/   # Astro components
│   ├── content/      # Blog posts (MDX)
│   ├── layouts/      # Page layouts
│   ├── pages/        # Route pages
│   └── utils/        # Utility functions
├── astro.config.mjs  # Astro configuration
└── package.json      # Dependencies
```

## 🛠️ Development

### Adding a New Post

1. Create a new `.mdx` file in `src/content/blog/`
2. Add frontmatter with metadata:

```yaml
---
title: "Your Post Title"
description: "A brief description"
pubDate: 2025-01-19
category: "Development"
tags: ["Astro", "Tutorial"]
featured: true
heroImage:
  src: "../../assets/images/hero.jpg"
  alt: "Hero image"
author: "Your Name"
---

# Your content here
```

### Customization

#### Theme Colors

Edit `src/styles/global.css` to customize colors:

```css
:root {
  --accent: 209, 100%, 42%;  /* Accent color */
  --text-primary: rgb(10, 10, 10);
  --text-secondary: rgb(80, 80, 80);
  --bg-primary: rgb(255, 255, 255);
}
```

#### Site Configuration

Edit `astro.config.mjs` to update site URL:

```javascript
export default defineConfig({
  site: 'https://yourdomain.com',
  // ...
});
```

## 📊 Commands

| Command | Action |
|---------|--------|
| `npm run dev` | Start dev server at `localhost:4321` |
| `npm run build` | Build production site |
| `npm run preview` | Preview production build |
| `npm run format` | Format code with Prettier |
| `npm run lint` | Lint code with ESLint |

## 🌐 Deployment

### Vercel

```bash
npm i -g vercel
vercel
```

### Netlify

1. Connect your Git repository
2. Set build command: `npm run build`
3. Set publish directory: `dist`

### Static Hosting

Any static hosting service works:
- GitHub Pages
- Cloudflare Pages
- AWS S3 + CloudFront
- Firebase Hosting

## 📝 License

MIT

## 🤝 Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

## 📚 Resources

- [Astro Documentation](https://docs.astro.build)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [MDX Documentation](https://mdxjs.com/docs)
- [TypeScript Documentation](https://www.typescriptlang.org/docs)
"## Test PR for PR-Agent" 
