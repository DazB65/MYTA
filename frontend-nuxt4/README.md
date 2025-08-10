# Vidalytics Frontend

Modern YouTube analytics dashboard built with Nuxt 4, Vue 3, and Tailwind CSS.

## Features

- 📊 **Interactive Analytics Dashboard** with real-time charts
- 🎯 **Content Pillars Management** for organizing content themes
- 📱 **Responsive Design** optimized for all devices
- 🎨 **Modern UI/UX** with Tailwind CSS styling
- ⚡ **Fast Performance** with Nuxt 4 optimizations
- 🔄 **Real-time Updates** with reactive data

## Tech Stack

- **Framework**: Nuxt 4 (Vue 3)
- **Styling**: Tailwind CSS
- **TypeScript**: Full type safety
- **Icons**: Lucide Icons
- **Charts**: Chart.js integration
- **State**: Nuxt composables

## Setup

Install dependencies:

```bash
npm install
```

## Development

Start the development server on `http://localhost:3000`:

```bash
npm run dev
```

The frontend will connect to the backend API at `http://localhost:8000`.

## Project Structure

```
frontend-nuxt4/
├── app/
│   ├── pages/              # Nuxt pages (routes)
│   └── layouts/            # Layout components
├── components/
│   ├── analytics/          # Analytics dashboard components
│   ├── ui/                 # Reusable UI components
│   └── charts/             # Chart components
├── composables/            # Nuxt composables
│   ├── useAnalytics.js     # Analytics data management
│   └── useApi.js           # API utilities
├── public/                 # Static assets
└── nuxt.config.ts          # Nuxt configuration
```

## Key Components

- **AnalyticsOverview** - Main dashboard overview
- **ChartsDashboard** - Interactive charts and metrics
- **ContentPillars** - Content theme management
- **PerformanceMetrics** - Key performance indicators

## API Integration

The frontend connects to the FastAPI backend:

- **Base URL**: `http://localhost:8000`
- **Analytics**: `/api/analytics/*`
- **Content**: `/api/content/*`
- **Auth**: `/api/auth/*`

## Production

Build for production:

```bash
npm run build
```

Preview production build:

```bash
npm run preview
```

## Environment Variables

Frontend environment variables (if needed):

```env
# API Configuration
NUXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

## Development Tips

- Use browser dev tools to inspect components
- Check console for any API connection issues
- Backend must be running on port 8000
- Hot reload is enabled for fast development

For more information, see the [main project documentation](../docs/README.md).
