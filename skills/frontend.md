---
name: frontend
description: >
  Frontend development assistance for component design, state management, accessibility,
  and UI patterns. Framework-aware (React, Vue, Svelte, Angular). Triggers:
  "create component", "frontend pattern", "UI component", "state management",
  "accessibility", "CSS", "React hook", "form handling", "client-side".
---

## Purpose

Provide frontend-specialized AI assistance. Understands component architecture,
reactivity models, accessibility requirements, and performance considerations
specific to UI development. Adapts to the detected framework.

## Activation Criteria

- User asks to create, modify, or review UI components
- User mentions React, Vue, Svelte, Angular, or similar UI frameworks
- User asks about state management, props, events, or reactivity
- User asks about accessibility (a11y), ARIA, or semantic HTML
- User asks about CSS, styling systems (Tailwind, CSS Modules, styled-components)
- User mentions "client-side", "frontend", "UI", "page", "layout"

## Steps

1. **Detect framework and conventions**:
   - React: check for `react` in dependencies, `.jsx`/`.tsx` files
   - Vue: check for `vue` dependency, `.vue` files
   - Svelte: check for `svelte` dependency, `.svelte` files
   - Angular: check for `@angular/core`, `.component.ts` files
   - Detect styling: Tailwind (`tailwind.config.*`), CSS Modules (`*.module.css`), styled-components, etc.
   - Detect state management: Redux, Zustand, Pinia, Jotai, Recoil, etc.

2. **Component design**:
   - Single responsibility: one component, one purpose
   - Props/inputs: define with types; avoid prop drilling beyond 2-3 levels (use context/store)
   - Composition over inheritance: use render props, slots, or HOCs rather than extending components
   - Controlled vs. uncontrolled: prefer controlled components for forms
   - Keep components pure: same props → same output (no side effects in render)

3. **State management rules**:
   - Local state (`useState`, `ref`, reactive): for UI-only state (open/closed, hover, etc.)
   - Shared local state: lift to nearest common ancestor
   - Global state (Redux, Zustand, Pinia): for cross-feature data (auth, cart, user preferences)
   - Server state (React Query, SWR, TanStack Query): for async data fetching — do not duplicate in global store
   - Form state: use a form library (React Hook Form, Vee-Validate, Felte) for complex forms

4. **Accessibility (a11y) checklist** (apply to all generated UI):
   - Semantic HTML: use `<button>`, `<nav>`, `<main>`, `<header>` over `<div>` where appropriate
   - Interactive elements: keyboard navigable, visible focus indicator
   - Images: `alt` text (empty `alt=""` for decorative images)
   - Forms: `<label>` associated with every input via `for`/`htmlFor` or wrapping
   - ARIA: use sparingly and only when semantic HTML is insufficient
   - Color contrast: don't use color as the only differentiator
   - Focus management: when modals/dialogs open, move focus to them; restore on close

5. **Performance considerations**:
   - Avoid unnecessary re-renders: memoize components and callbacks where proven needed
   - Code splitting: lazy-load routes and heavy components (`React.lazy`, `defineAsyncComponent`)
   - Image optimization: `width`/`height` attributes, appropriate formats (WebP, AVIF)
   - Avoid layout thrash: batch DOM reads before writes
   - List rendering: always provide a stable `key` prop; virtualize long lists (>100 items)

6. **Generate the component**:
   - Follow detected naming conventions (PascalCase files and components)
   - Include prop type definitions (TypeScript interface, PropTypes, or framework equivalent)
   - Export as named export (default exports make refactoring harder)
   - Include basic accessibility attributes
   - Include a brief JSDoc/TSDoc comment for the component's purpose

## Output Format

Complete component file(s) with proper imports, types, and framework conventions.
For new components: also provide a minimal usage example.

## Scope

`src/**/*.{tsx,jsx,vue,svelte,ts}` — frontend source files.

## Constraints

- Always include TypeScript types if the project uses TypeScript
- Never use deprecated framework APIs (check detected framework version)
- Do not use `dangerouslySetInnerHTML` without explicit XSS-safe justification
- Do not import from a parent directory (`../../`) more than 2 levels up — suggest restructuring

## Edge Cases

- **Server Components (Next.js App Router)**: Clearly distinguish server vs. client components;
  avoid `useState`/`useEffect` in server components; add `'use client'` directive when needed
- **Hydration mismatches (SSR)**: Flag code that reads browser-only APIs (`window`, `document`)
  without client-side guards
- **Accessibility in drag-and-drop**: Always provide a keyboard alternative

## Cross-Ecosystem Notes

- **Cursor**: Activate with `@50-skill-frontend` while working on UI files
- **Aider**: `/add <component-file>`, reference the Frontend section in CONVENTIONS.md
- **Codex**: Reference "Task: Frontend Development" in AGENTS.md
