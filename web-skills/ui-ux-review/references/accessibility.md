# Web accessibility standards and ARIA patterns

Audit frontend components against WCAG 2.2 standards, W3C WAI-ARIA Authoring Practices, and Accessible Name computation rules.

## Authoritative sources

| Source | Author or organization | Domain | Official URL |
| --- | --- | --- | --- |
| W3C WAI-ARIA Authoring Practices Guide: Combobox | W3C Web Accessibility Initiative | Combobox design pattern | https://www.w3.org/WAI/ARIA/apg/patterns/combobox/ |
| W3C WAI-ARIA Authoring Practices Guide: Dialog Modal | W3C Web Accessibility Initiative | Modal focus trapping | https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/ |
| W3C WAI-ARIA Authoring Practices Guide: Tabs | W3C Web Accessibility Initiative | Tabs and roving tabindex | https://www.w3.org/WAI/ARIA/apg/patterns/tabs/ |
| W3C WAI-ARIA Authoring Practices Guide: Accordion | W3C Web Accessibility Initiative | Expandable section pattern | https://www.w3.org/WAI/ARIA/apg/patterns/accordion/ |
| W3C WAI-ARIA Authoring Practices Guide: Menu Button | W3C Web Accessibility Initiative | Action menu pattern | https://www.w3.org/WAI/ARIA/apg/patterns/menu-button/ |
| Web Content Accessibility Guidelines 2.2 (2023) | W3C Accessibility Guidelines Working Group | International digital standard | https://www.w3.org/TR/WCAG22/ |
| Accessible Name and Description Computation 1.2 | W3C ARIA Working Group | AccName calculation rules | https://www.w3.org/TR/accname-1.2/ |
| Understanding WCAG 2.2: Non-text Contrast (SC 1.4.11) | W3C Web Accessibility Initiative | Control contrast requirements | https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html |
| Understanding WCAG 2.2: Target Size Minimum (SC 2.5.8) | W3C Web Accessibility Initiative | Pointer target area rules | https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html |
| Understanding WCAG 2.2: Focus Not Obscured (SC 2.4.11) | W3C Web Accessibility Initiative | Viewport focus visibility | https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum.html |

## 1. W3C WAI-ARIA APG component patterns

### Combobox pattern
A combobox pairs a single-line textbox with an inline popup listbox, grid, or dialog:
- **ARIA roles and states.**
  - The input element must declare `role="combobox"`, `aria-expanded="true"` when the popup is visible, and `"false"` when closed.
  - Set `aria-haspopup="listbox"` and link to the popup container via `aria-controls="popup-id"`.
  - Set `aria-autocomplete="list"` or `"both"` depending on input behavior.
  - The popup container declares `role="listbox"`. Each item inside declares `role="option"` with a unique ID.
  - Maintain active selection via `aria-activedescendant="option-id"` on the input. DOM focus must remain within the text input so the user can continue typing.
- **Keyboard interaction.**
  - `ArrowDown`: Opens the listbox if closed, then moves active selection to the next option.
  - `ArrowUp`: Moves active selection to the previous option. If on the first option, closes popup or returns to input.
  - `Enter`: Selects the active option, updates the input value, and closes the listbox.
  - `Escape`: Closes the listbox if open. Clears input text if the listbox is already closed.
  - `Alt + ArrowDown`: Opens the listbox without changing the active option.
  - `Alt + ArrowUp`: Closes the listbox, retaining current selection.

### Dialog modal pattern
Modals isolate interaction strictly within the dialog container until dismissed:
- **ARIA structure.**
  - Container declares `role="dialog"` or `role="alertdialog"` for urgent interruptions.
  - Declare `aria-modal="true"` to signal that content outside the modal is inert.
  - Link the primary heading using `aria-labelledby="heading-id"`.
  - Link supporting explanatory copy using `aria-describedby="desc-id"`.
- **Focus trapping and restoration.**
  - On open, shift focus to the first interactive element inside, or to the dialog container itself via `tabindex="-1"`.
  - Intercept `Tab` and `Shift + Tab` keydown events. When pressing `Tab` on the final focusable element, loop focus back to the first focusable element. When pressing `Shift + Tab` on the first element, wrap to the final element.
  - Mark sibling elements outside the modal with the HTML `inert` attribute to suppress them from the screen reader tree and tabbing sequence.
  - Save a reference to `document.activeElement` prior to opening. Return focus to that trigger element when the modal closes.

### Tabs pattern
Tabs divide content into separate panels where only one panel renders at a time:
- **Roving tabindex.**
  - The wrapper declares `role="tablist"` with `aria-label`.
  - Each tab trigger declares `role="tab"`, `aria-controls="panel-id"`, and `aria-selected="true"` or `"false"`.
  - The active tab carries `tabindex="0"`. Inactive tabs carry `tabindex="-1"`. This ensures the entire tablist occupies exactly one tab stop in the document flow.
  - Content panels declare `role="tabpanel"` and `aria-labelledby="tab-id"`.
- **Keyboard navigation.**
  - `ArrowRight` and `ArrowLeft`: Navigate through tabs horizontally, moving focus and shifting the active `tabindex="0"`.
  - `Home` and `End`: Jump directly to the first or last tab.
  - `Space` or `Enter`: Activate the focused tab when using manual tab activation mode.
  - `Tab`: Shifts focus directly from the active tab into the open tabpanel.

### Accordion pattern
Accordions display vertically stacked panels that expand or collapse on demand:
- Each trigger must be wrapped in a semantic HTML heading tag (`<h2>`, `<h3>`).
- The trigger must be a native `<button>` declaring `aria-expanded="true"` or `"false"`, with `aria-controls="panel-id"`.
- The collapsible panel declares `role="region"` and `aria-labelledby="trigger-id"`.
- When collapsed, hide the panel content using the HTML `hidden` attribute to remove it from accessibility trees.

### Menu button pattern
Menu buttons provide dropdown action lists:
- The trigger button declares `aria-haspopup="menu"`, `aria-expanded="true"` or `"false"`, and `aria-controls="menu-id"`.
- The menu container declares `role="menu"`. Children declare `role="menuitem"`.
- Do not use `role="menu"` for site-wide navigation links. Site navigation must use semantic `<nav>`, `<ul>`, `<li>`, and standard `<a href="...">` elements.

## 2. WCAG 2.2 success criteria requirements

### SC 2.5.8 Target Size Minimum (Level AA)
- Interactive pointer targets must measure at least 24 by 24 CSS pixels.
- If a target is smaller than 24px, an offset circle of 24px diameter centered on the target must not intersect any other target or offset circle.
- At Level AAA (SC 2.5.5), targets must measure at least 44 by 44 CSS pixels without spacing compensations.

### SC 2.4.11 Focus Not Obscured Minimum (Level AA)
- When an element receives keyboard focus, it must not be entirely hidden beneath sticky navigation bars, fixed headers, or floating banners.
- Declare `scroll-padding-top` and `scroll-padding-bottom` on the root scroll container equal to the height of fixed bars.

```css
html, :root {
  scroll-padding-top: var(--header-height, 64px);
  scroll-padding-bottom: var(--banner-height, 0px);
}
```

### SC 2.4.13 Focus Appearance (Level AAA)
- The focus indicator area must equal at least a 2px solid border around the component perimeter.
- Focus pixels must demonstrate a contrast ratio of at least 3:1 between focused and unfocused states, as well as against the adjacent background.

### SC 3.3.7 Redundant Entry (Level A)
- Information previously entered by a user within the same workflow or session must not be requested again.
- The system must auto-populate previously entered data or provide a selection mechanism (such as a "Same as shipping address" toggle).

### SC 3.3.8 Accessible Authentication Minimum (Level AA)
- Authentication must not rely solely on cognitive function tests (memorizing complex passwords, solving CAPTCHAs, or transcribing characters).
- Support password managers by providing `autocomplete="username"` and `autocomplete="current-password"`, permitting clipboard paste operations, or offering WebAuthn/Passkey authentication.

## 3. Non-text contrast (WCAG 1.4.11 Level AA)

Visual representations of user interface components and graphical objects must achieve a contrast ratio of at least 3:1 against adjacent colors:

### Input boundaries
If a text field relies on an outline border to indicate its interactive boundary on a white canvas, the border color must reach at least 3:1 contrast. On white (`#ffffff`), border colors must be `#767676` or darker. Light gray borders such as `#d1d5db` or `#e5e7eb` fail this criterion.

### Checkboxes, radio buttons, and switches
- The outer border of checkboxes and radio circles requires 3:1 contrast against the background canvas.
- Active checkmarks or interior dots require 3:1 contrast against the control background.
- Toggle switch tracks in both active and inactive states require 3:1 contrast against the surrounding surface.

### Standalone icons
Icons that convey meaning without supporting text (search glass, cart, close buttons) require a minimum 3:1 contrast ratio against their container background.

## 4. Keyboard navigation mechanics

### Roving tabindex versus aria-activedescendant
- **Roving tabindex.** Only the active item receives `tabindex="0"`, while all sibling items carry `tabindex="-1"`. Arrow keys shift `tabindex="0"` and call `element.focus()`. Ideal for Tabs, Toolbars, and Action Menus.
- **aria-activedescendant.** Focus stays locked on the parent container or text input. Pressing arrow keys updates the attribute to point to the active item's ID. Ideal for Combobox and Autocomplete fields.

### Focus trapping implementation
Custom modals must bind `keydown` listeners to trap `Tab` and `Shift + Tab` cycles. Sibling elements must carry the `inert` attribute:

```javascript
function trapFocus(modalElement, event) {
  if (event.key !== 'Tab') return;
  const focusables = modalElement.querySelectorAll(
    'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
  );
  const first = focusables[0];
  const last = focusables[focusables.length - 1];

  if (event.shiftKey && document.activeElement === first) {
    event.preventDefault();
    last.focus();
  } else if (!event.shiftKey && document.activeElement === last) {
    event.preventDefault();
    first.focus();
  }
}
```

### Skip links
Skip links provide direct access to primary content, bypassing repetitive header navigation. Render the link as the first child of `<body>`:

```html
<a href="#main-content" class="skip-link">Skip to main content</a>

<main id="main-content" tabindex="-1">
  <!-- Primary content -->
</main>
```

```css
.skip-link {
  position: absolute;
  top: -9999px;
  left: 16px;
  z-index: 1000;
  padding: 8px 16px;
  background: #0f172a;
  color: #ffffff;
}

.skip-link:focus-visible {
  top: 16px;
}
```

## 5. Accessible Name Computation (AccName 1.2)

Assistive technologies determine an element's accessible name using this strict priority hierarchy:

1. `aria-labelledby`. Highest priority. Gathers text content from one or more referenced element IDs.
2. `aria-label`. Second priority. Overrides native inner text content.
3. Native HTML labeling. Associated `<label for="...">` tags, `alt` attributes on images, or `<caption>` tags on data tables.
4. Inner text content. Gathers plain text rendered directly inside the element.
5. `title` attribute. Secondary fallback.
6. `placeholder` attribute. Emergency fallback. Never use placeholder text as the primary accessible name.

### Critical AccName rules
- Do not apply `aria-label` to generic non-interactive elements (`<div>`, `<span>`) unless they carry an explicit interactive ARIA role.
- **Label in Name (WCAG 2.5.3).** Accessible names must contain the visible text rendered on screen. If a button displays "Send", its `aria-label` must begin with "Send" (such as "Send payment").

## 6. Concrete automated verification checks

### CSS focus ring standards
```css
:focus-visible {
  outline: 2px solid #0f172a;
  outline-offset: 2px;
}
```

### Automated testing pattern (Testing Library and axe-core)
```typescript
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { axe, toHaveNoViolations } from 'jest-axe';
expect.extend(toHaveNoViolations);

test('dialog modal satisfies accessibility standards and restores focus', async () => {
  const user = userEvent.setup();
  const { container } = render(<CustomModal />);
  
  const trigger = screen.getByRole('button', { name: /view details/i });
  await user.click(trigger);
  
  const modal = screen.getByRole('dialog', { name: /confirm submission/i });
  expect(modal).toBeInTheDocument();
  
  const results = await axe(container);
  expect(results).toHaveNoViolations();
  
  await user.keyboard('{Escape}');
  expect(trigger).toHaveFocus();
});
```
