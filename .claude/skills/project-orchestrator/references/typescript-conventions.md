# TypeScript/Vite/Astro Project Conventions

## Directory Structure

### Vite/React Projects
```
project-name/
├── src/
│   ├── main.tsx
│   ├── App.tsx
│   ├── components/
│   └── assets/
├── public/
├── .gitignore
├── .pre-commit-config.yaml
├── package.json
├── tsconfig.json
├── vite.config.ts
├── tailwind.config.js (if using Tailwind)
├── README.md
└── .github/
    └── workflows/ (for deployment)
```

### Astro Projects
```
project-name/
├── src/
│   ├── pages/
│   ├── layouts/
│   ├── components/
│   └── content/ (for content collections)
├── public/
├── .gitignore
├── .pre-commit-config.yaml
├── package.json
├── tsconfig.json
├── astro.config.mjs
├── tailwind.config.js (if using Tailwind)
├── README.md
└── .github/
    └── workflows/ (for deployment)
```

## package.json Structure

Include:
- `name`, `version`, `type: "module"`
- Scripts: `dev`, `build`, `preview`, `lint`, `format`
- Dependencies and devDependencies separated
- Engine specification if needed

## Pre-commit Hooks

Standard TypeScript pre-commit hooks:
- `prettier` for formatting
- `eslint` for linting
- Optional: `tsc --noEmit` for type checking

## Linting & Formatting

- **Formatter**: Prettier (opinionated, minimal config)
- **Linter**: ESLint with TypeScript plugin
- **Config**: Use recommended presets, customize sparingly

Common ESLint config:
```js
{
  extends: [
    'eslint:recommended',
    'plugin:@typescript-eslint/recommended',
    'plugin:astro/recommended', // for Astro
    'prettier' // disables conflicting rules
  ]
}
```

## Deployment

### GitHub Pages (Astro/Vite)
- GitHub Actions workflow
- Build static assets
- Deploy to gh-pages branch or Pages directly
- Set correct `base` in config if not at root

### Vercel/Netlify
- Auto-deploy from git
- Zero-config for most frameworks
- Environment variables in platform UI

## Docker (Optional)

Most web projects deploy to static hosts and don't need Docker.

If needed (for SSR or custom deployment):
- Multi-stage build
- Node builder + nginx/minimal runtime
- Copy dist folder to serve
