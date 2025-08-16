# Vidalytics Design System

A comprehensive design system built with Tailwind CSS and custom CSS variables for the Vidalytics application.

## 🎨 Color Palette

### Background Colors

- `bg-background` / `--color-bg` - Main background (#111827)
- `bg-background-card` / `--color-bg-card` - Card backgrounds (#1f2937)
- `bg-background-elevated` / `--color-bg-elevated` - Elevated surfaces (#374151)

### Text Colors

- `text-text-primary` / `--color-text-primary` - Primary text (#ffffff)
- `text-text-secondary` / `--color-text-secondary` - Secondary text (#d1d5db)
- `text-text-tertiary` / `--color-text-tertiary` - Tertiary text (#9ca3af)
- `text-text-muted` / `--color-text-muted` - Muted text (#6b7280)

### Agent-Based Brand Colors

- `bg-brand-primary` / `--color-brand-primary` - Agent 1 Purple (#9333ea)
- `bg-brand-secondary` / `--color-brand-secondary` - Agent 2 Blue (#2563eb)

### Agent Colors

- `bg-agent-1` / `--color-agent-1` - Agent 1 Purple (#9333ea)
- `bg-agent-2` / `--color-agent-2` - Agent 2 Blue (#2563eb)
- `bg-agent-3` / `--color-agent-3` - Agent 3 Green (#059669)
- `bg-agent-4` / `--color-agent-4` - Agent 4 Orange (#ea580c)
- `bg-agent-5` / `--color-agent-5` - Agent 5 Pink (#db2777)
- `bg-agent-boss` / `--color-agent-boss` - Boss Agent Brown (#7c2d12)

### Accent Colors (Agent-Based)

- `bg-accent-purple` - Agent 1 Purple (#9333ea)
- `bg-accent-blue` - Agent 2 Blue (#2563eb)
- `bg-accent-green` - Agent 3 Green (#059669)
- `bg-accent-orange` - Agent 4 Orange (#ea580c)
- `bg-accent-pink` - Agent 5 Pink (#db2777)
- `bg-accent-red` - Error/Alert Red (#ef4444)

### Status Colors

- `bg-success` / `text-success` - Success states (#10b981)
- `bg-warning` / `text-warning` - Warning states (#f59e0b)
- `bg-error` / `text-error` - Error states (#ef4444)

## 🎭 Gradients

### Agent Gradients

- `bg-gradient-brand` - Main brand gradient (Agent 1 to Agent 2)
- `bg-gradient-agent-1` - Agent 1 Purple gradient
- `bg-gradient-agent-2` - Agent 2 Blue gradient
- `bg-gradient-agent-3` - Agent 3 Green gradient
- `bg-gradient-agent-4` - Agent 4 Orange gradient
- `bg-gradient-agent-5` - Agent 5 Pink gradient
- `bg-gradient-boss` - Boss Agent gradient
- `bg-gradient-multi-agent` - All agents combined gradient
- `bg-gradient-glass` - Glass morphism gradient

## 📝 Typography

### Font Families

- `font-sans` - Inter (primary font)
- `font-mono` - JetBrains Mono (monospace)

### Font Weights

- `font-light` (300)
- `font-normal` (400)
- `font-medium` (500)
- `font-semibold` (600)
- `font-bold` (700)
- `font-extrabold` (800)

### Font Sizes

- `text-xs` - 12px
- `text-sm` - 14px
- `text-base` - 16px
- `text-lg` - 18px
- `text-xl` - 20px
- `text-2xl` - 24px
- `text-3xl` - 30px
- `text-4xl` - 36px

## 📏 Spacing

### Spacing Scale

- `space-1` / `p-1` - 4px
- `space-2` / `p-2` - 8px
- `space-3` / `p-3` - 12px
- `space-4` / `p-4` - 16px
- `space-5` / `p-5` - 20px
- `space-6` / `p-6` - 24px
- `space-8` / `p-8` - 32px
- `space-10` / `p-10` - 40px
- `space-12` / `p-12` - 48px
- `space-16` / `p-16` - 64px
- `space-20` / `p-20` - 80px
- `space-24` / `p-24` - 96px
- `space-32` / `p-32` - 128px

## 🔲 Border Radius

- `rounded-sm` - 4px
- `rounded-md` - 6px
- `rounded-lg` - 8px
- `rounded-xl` - 12px (standard for cards)
- `rounded-2xl` - 16px
- `rounded-3xl` - 24px

## 🌟 Shadows

- `shadow-sm` - Subtle shadow
- `shadow-md` - Medium shadow (default for cards)
- `shadow-lg` - Large shadow (hover states)
- `shadow-xl` - Extra large shadow
- `shadow-glass` - Glass morphism shadow
- `shadow-glow` - Pink glow effect
- `shadow-glow-blue` - Blue glow effect

## 🧩 Component Classes

### Cards

```html
<!-- Basic card -->
<div class="card">Content</div>

<!-- Hoverable card -->
<div class="card card-hover">Content</div>

<!-- Glass morphism card -->
<div class="card-glass">Content</div>

<!-- Elevated card -->
<div class="card-elevated card">Content</div>
```

### Buttons

```html
<!-- Primary button -->
<button class="btn btn-primary">Primary</button>

<!-- Secondary button -->
<button class="btn btn-secondary">Secondary</button>

<!-- Ghost button -->
<button class="btn btn-ghost">Ghost</button>

<!-- Small button -->
<button class="btn btn-primary btn-sm">Small</button>

<!-- Large button -->
<button class="btn btn-primary btn-lg">Large</button>
```

### Inputs

```html
<!-- Standard input -->
<input class="input" type="text" placeholder="Enter text..." />
```

### Badges

```html
<!-- Primary badge -->
<span class="badge badge-primary">Primary</span>

<!-- Status badges -->
<span class="badge badge-success">Success</span>
<span class="badge badge-warning">Warning</span>
<span class="badge badge-error">Error</span>
```

### Glass Morphism

```html
<!-- Glass effect -->
<div class="glass rounded-xl p-6">Glass content</div>
```

## 🎬 Animations

### Available Animations

- `animate-fade-in` - Fade in effect
- `animate-slide-up` - Slide up from bottom
- `animate-slide-down` - Slide down from top
- `animate-scale-in` - Scale in effect
- `animate-pulse-glow` - Pulsing glow effect

### Transitions

- `transition-fast` - 150ms
- `transition-normal` - 200ms (default)
- `transition-slow` - 300ms

## 📱 Responsive Design

### Breakpoints

- `sm:` - 640px and up
- `md:` - 768px and up
- `lg:` - 1024px and up
- `xl:` - 1280px and up
- `2xl:` - 1536px and up

## 🎯 Usage Guidelines

### Do's

- ✅ Use the predefined color palette
- ✅ Stick to the spacing scale
- ✅ Use component classes for consistency
- ✅ Apply hover effects for interactive elements
- ✅ Use glass morphism sparingly for special elements

### Don'ts

- ❌ Don't use arbitrary colors outside the palette
- ❌ Don't mix different border radius values randomly
- ❌ Don't skip the transition classes for interactive elements
- ❌ Don't overuse glass effects (can impact performance)

## 🔧 Customization

To extend the design system, modify:

1. `tailwind.config.js` - For Tailwind utilities
2. `assets/css/main.css` - For CSS variables and component classes

## 📚 Examples

### Dashboard Card

```html
<div class="card card-hover">
  <div class="mb-6 flex items-center justify-between">
    <h3 class="text-lg font-semibold text-text-primary">Card Title</h3>
    <button class="btn btn-ghost btn-sm">Action</button>
  </div>
  <p class="text-text-secondary">Card content goes here...</p>
</div>
```

### Status Badge

```html
<span class="badge badge-success">
  <svg class="mr-1 h-3 w-3" fill="currentColor">...</svg>
  Completed
</span>
```

This design system ensures consistency, maintainability, and a premium look across the entire Vidalytics application.
