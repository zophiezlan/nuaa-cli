# Fluent UI Web Components Integration

## Overview

This document describes the integration of Microsoft Fluent UI Web Components across the NUAA Web Interface. Fluent UI provides a modern, accessible, and consistent design language aligned with Microsoft's design system.

## What's Changed

### 1. Fluent UI Web Components Added

All HTML templates now include the Fluent UI Web Components library:

```html
<script type="module" src="https://unpkg.com/@fluentui/web-components@2.6.1"></script>
```

### 2. Components Converted

The following components have been converted from standard HTML to Fluent UI Web Components:

#### Buttons
- **Before**: `<button class="btn primary">Submit</button>`
- **After**: `<fluent-button appearance="accent">Submit</fluent-button>`

Available appearances:
- `accent` - Primary action buttons (blue)
- `neutral` - Secondary action buttons (gray)
- `outline` - Outlined buttons
- `stealth` - Icon-only buttons without background
- `lightweight` - Minimal styling

#### Cards
- **Before**: `<div class="card">...</div>`
- **After**: `<fluent-card>...</fluent-card>`

Used for:
- Team selection cards
- Template cards
- Statistics cards
- Content containers

#### Form Fields
- **Before**: `<input type="text" />`
- **After**: `<fluent-text-field></fluent-text-field>`

- **Before**: `<textarea></textarea>`
- **After**: `<fluent-text-area></fluent-text-area>`

#### Checkboxes
- **Before**: `<input type="checkbox" />`
- **After**: `<fluent-checkbox></fluent-checkbox>`

#### Progress Bars
- **Before**: `<div class="progress-bar" style="width: 50%"></div>`
- **After**: `<fluent-progress value="50" max="100"></fluent-progress>`

#### Badges
- **Before**: `<span class="badge">New</span>`
- **After**: `<fluent-badge>New</fluent-badge>`

#### Dialogs/Modals
- **Before**: `<div class="modal">...</div>`
- **After**: `<fluent-dialog modal>...</fluent-dialog>`

### 3. Custom Theme CSS

A new stylesheet `fluent-theme.css` has been created to:
- Customize Fluent UI components to match NUAA branding
- Ensure consistent spacing and sizing
- Support dark mode and high contrast accessibility modes
- Provide responsive design breakpoints

### 4. Color Palette Updates

The color palette has been updated to align with Fluent Design System:
- Primary Blue: `#0f6cbd` (Fluent Blue 70)
- Primary Dark: `#115ea3` (Fluent Blue 60)
- Primary Light: `#d6e8fa`

## Benefits

### 1. **Accessibility**
- Built-in ARIA labels and keyboard navigation
- Screen reader support out of the box
- High contrast mode support
- Focus indicators that meet WCAG standards

### 2. **Consistency**
- Microsoft-aligned design language
- Consistent styling across all components
- Professional, modern appearance

### 3. **Maintainability**
- Web Components are framework-agnostic
- Easy to update by changing CDN version
- Reduced custom CSS needed

### 4. **Performance**
- Lazy-loaded components
- Efficient rendering
- Small bundle size via CDN

### 5. **Responsive Design**
- Mobile-first approach
- Touch-friendly controls (44px minimum)
- Adaptive layouts

## Files Modified

### HTML Templates (All Updated)
- `index.html` - Homepage with team selection
- `team_dashboard.html` - Team-specific dashboards
- `form.html` - Document creation forms
- `admin.html` - Admin panel
- `analytics.html` - Analytics dashboard
- `accessibility.html` - Accessibility settings
- `help.html` - Help pages
- `offline.html` - Offline page
- `welcome-wizard.html` - Onboarding wizard

### New CSS Files
- `static/css/fluent-theme.css` - Fluent UI theme customizations

### Existing CSS
- `static/css/main.css` - Updated CSS variables to align with Fluent Design tokens

## Browser Support

Fluent UI Web Components support:
- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Mobile browsers (iOS Safari, Chrome Mobile)

## Migration Guide

### For Developers

If you need to add new buttons:

```html
<!-- ❌ Don't use -->
<button class="btn primary" onclick="doSomething()">Click Me</button>

<!-- ✅ Do use -->
<fluent-button appearance="accent" onclick="doSomething()">Click Me</fluent-button>
```

If you need to add new form fields:

```html
<!-- ❌ Don't use -->
<input type="text" name="username" placeholder="Enter username" />

<!-- ✅ Do use -->
<fluent-text-field
  name="username"
  placeholder="Enter username"
></fluent-text-field>
```

If you need to add new cards:

```html
<!-- ❌ Don't use -->
<div class="card">
  <h3>Title</h3>
  <p>Content</p>
</div>

<!-- ✅ Do use -->
<fluent-card>
  <h3>Title</h3>
  <p>Content</p>
</fluent-card>
```

### JavaScript Updates

For progress bars, update your JavaScript:

```javascript
// ❌ Old way
document.getElementById('progressBar').style.width = '50%';

// ✅ New way
document.getElementById('progressBar').setAttribute('value', 50);
```

For checkboxes:

```javascript
// ❌ Old way
document.getElementById('myCheckbox').checked = true;

// ✅ New way (both work)
document.getElementById('myCheckbox').checked = true;
// or
document.getElementById('myCheckbox').setAttribute('checked', '');
```

## Customization

### Theming

Fluent UI components respect CSS custom properties. You can customize the theme by updating variables in `fluent-theme.css`:

```css
:root {
  --accent-fill-rest: #0f6cbd;  /* Primary button color */
  --neutral-fill-rest: #f5f5f5;  /* Card backgrounds */
  --neutral-foreground-rest: #333;  /* Text color */
}
```

### Dark Mode

Dark mode is automatically supported. The `fluent-theme.css` includes dark mode overrides:

```css
body.dark-mode {
  --neutral-foreground-rest: #ffffff;
  --neutral-fill-rest: #2a2a2a;
}
```

## Resources

- [Fluent UI Web Components Documentation](https://web-components.fluentui.dev/)
- [Microsoft Fluent Design System](https://fluent2.microsoft.design/)
- [Component Explorer](https://web-components.fluentui.dev/?path=/docs/components-button--docs)
- [GitHub Repository](https://github.com/microsoft/fluentui/tree/master/packages/web-components)

## Troubleshooting

### Components not showing correctly

Ensure the Fluent UI script is loaded:
```html
<script type="module" src="https://unpkg.com/@fluentui/web-components@2.6.1"></script>
```

### Styles not applying

Check that `fluent-theme.css` is included after other stylesheets:
```html
<link rel="stylesheet" href="/static/css/themes.css" />
<link rel="stylesheet" href="/static/css/fluent-theme.css" />
```

### JavaScript not working

For dynamically created components, ensure they're registered before use:
```javascript
// Wait for components to be defined
await customElements.whenDefined('fluent-button');
```

## Version

- **Fluent UI Web Components**: v2.6.1
- **Integration Date**: November 2025
- **Last Updated**: November 2025

## Future Enhancements

Potential future improvements:
1. Add more Fluent UI components (tabs, menus, trees)
2. Implement Fluent UI theme tokens via CSS custom properties
3. Add animations using Fluent Motion
4. Integrate Fluent UI Icons
5. Create component library documentation

## Support

For issues or questions about Fluent UI integration:
- Check the [Fluent UI Web Components docs](https://web-components.fluentui.dev/)
- Review this integration guide
- Contact the development team
