# React Frontend Structure Explanation

## What We Just Created

You asked "why do we have HTML" - Great question! Here's the clarification:

### The HTML File (`index.html`)

- **Purpose**: Entry point that loads React
- **Size**: Tiny file (just the shell)
- **Content**: Just loads the React app
- **Think of it as**: The container for your React app

### The React App (`.jsx` files)

- **These are your ACTUAL app** - 100% React components
- All your UI, logic, and pages are in `.jsx` files
- React takes over after `index.html` loads

## How It Works

1. Browser loads `index.html`
2. `index.html` has `<div id="root"></div>` (empty container)
3. `index.html` loads `main.jsx` (your React entry point)
4. `main.jsx` renders your `<App />` component into `#root`
5. Everything else is pure React!

## File Structure Breakdown

```
frontend/src/
├── main.jsx                 # React entry point (loads App.jsx)
├── App.jsx                  # Main app with routing
├── styles/
│   └── index.css            # Tailwind CSS + global styles
├── components/
│   ├── Layout.jsx           # Page layout wrapper (Navbar + Footer)
│   ├── Navbar.jsx           # Navigation bar (React component)
│   └── Footer.jsx           # Footer (React component)
├── pages/
│   ├── Home.jsx             # Home page (React component)
│   ├── Alerts.jsx           # Alerts page (React component)
│   ├── AlertDetail.jsx      # Single alert page (React component)
│   ├── Education.jsx        # Education hub (React component)
│   ├── ArticleDetail.jsx    # Single article page (React component)
│   ├── Reports.jsx          # Community reports (React component)
│   └── About.jsx            # About page (React component)
├── services/
│   └── api.js               # API service layer (Axios)
└── utils/
    └── helpers.js           # Utility functions
```

## What's Complete

### 1. Routing System (React Router)

- Routes defined in `App.jsx`
- All routes use React components (not HTML pages)
- Navigation handled by `<Link>` components (React Router)

**Routes:**

- `/` → Home page
- `/alerts` → Alerts list
- `/alerts/:id` → Single alert detail
- `/education` → Education articles list
- `/education/:slug` → Single article
- `/reports` → Community reports
- `/about` → About page

### 2. Layout System

- `Layout.jsx` wraps all pages with Navbar and Footer
- Consistent design across all pages
- Responsive mobile menu included

### 3. Navigation

- `Navbar.jsx` - Fully functional React component
- Active link highlighting
- Mobile-responsive hamburger menu
- All navigation uses React Router (no page reloads)

### 4. Footer

- `Footer.jsx` - Complete React component
- Links to all pages
- Contact information section
- Social/resource links

### 5. Page Skeletons

All pages created as React components (ready to build out):

- Home.jsx
- Alerts.jsx
- AlertDetail.jsx
- Education.jsx
- ArticleDetail.jsx
- Reports.jsx
- About.jsx

### 6. API Service Layer

- `api.js` - Centralized API calls using Axios
- Pre-configured services for:
  - Subscriptions
  - Alerts
  - Education
  - Reports
  - Regions
- Uses environment variables for API URL

### 7. Utility Functions

- `helpers.js` - Common functions:
  - Date formatting
  - Phone number formatting/validation
  - Email validation
  - Text truncation
  - Severity colors
  - Debounce function

### 8. Styling System

- Tailwind CSS configured
- Custom theme with Terraguard colors
- Utility classes for buttons, cards, badges
- Responsive design utilities
- Global styles in `index.css`

## This is 100% React!

Everything you see after the page loads is React:

- Components render dynamically
- Navigation doesn't reload the page
- State management with React hooks
- All UI is JavaScript (JSX)

## No Traditional HTML Needed

You won't write HTML files for pages. Everything is React components:

**OLD WAY (Traditional):**

```
home.html
alerts.html
education.html
about.html
```

**NEW WAY (React - What We Have):**

```jsx
Home.jsx (React component)
Alerts.jsx (React component)
Education.jsx (React component)
About.jsx (React component)
```

## Next Steps

Now you can start building out each page with actual content:

1. **Home.jsx** - Add hero section, subscription form
2. **Alerts.jsx** - Fetch and display alerts from API
3. **Education.jsx** - Display articles
4. **Reports.jsx** - Add report submission form

All using React components, hooks, and your API service!

## To Test This React App

```powershell
cd frontend
npm install
npm run dev
```

Then open http://localhost:3000 and you'll see:

- A fully functional React app
- Working navigation
- All pages accessible
- Responsive design
- No page reloads when navigating

**This is pure React - no HTML page switching!**
