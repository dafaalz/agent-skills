/**
 * Automated CSSOM and Computed Style Token Extractor
 * Run directly in browser developer console or evaluate via Playwright/Puppeteer.
 */
(() => {
  const tokens = {
    customProperties: {},
    colors: new Set(),
    fonts: new Set(),
    fontSizes: new Set(),
    spacing: new Set(),
    mediaQueries: new Set(),
  };

  // 1. Extract CSS Custom Properties and Media Queries from accessible stylesheets
  for (const sheet of document.styleSheets) {
    let rules;
    try {
      rules = sheet.cssRules;
    } catch {
      continue; // Skip cross-origin stylesheets that block access
    }
    if (!rules) continue;

    const processRule = (rule) => {
      if (rule.type === CSSRule.MEDIA_RULE) {
        tokens.mediaQueries.add(rule.conditionText || rule.media.mediaText);
        for (const innerRule of rule.cssRules) {
          processRule(innerRule);
        }
      } else if (rule.type === CSSRule.STYLE_RULE) {
        if (rule.selectorText && (rule.selectorText.includes(':root') || rule.selectorText.includes('html'))) {
          for (let i = 0; i < rule.style.length; i++) {
            const prop = rule.style[i];
            if (prop.startsWith('--')) {
              tokens.customProperties[prop] = rule.style.getPropertyValue(prop).trim();
            }
          }
        }
      }
    };

    for (const rule of rules) {
      processRule(rule);
    }
  }

  // 2. Sample computed styles from DOM tree
  const elements = document.querySelectorAll('*');
  const sampleLimit = Math.min(elements.length, 1000);

  for (let i = 0; i < sampleLimit; i++) {
    const el = elements[i];
    const style = window.getComputedStyle(el);

    // Colors
    if (style.color) tokens.colors.add(style.color);
    if (style.backgroundColor && style.backgroundColor !== 'rgba(0, 0, 0, 0)') {
      tokens.colors.add(style.backgroundColor);
    }
    if (style.borderColor && style.borderColor !== 'rgba(0, 0, 0, 0)') {
      tokens.colors.add(style.borderColor);
    }

    // Typography
    if (style.fontFamily) tokens.fonts.add(style.fontFamily);
    if (style.fontSize) tokens.fontSizes.add(style.fontSize);

    // Spacing
    if (style.gap && style.gap !== 'normal') tokens.spacing.add(style.gap);
    if (style.padding && style.padding !== '0px') tokens.spacing.add(style.padding);
  }

  const result = {
    customPropertiesCount: Object.keys(tokens.customProperties).length,
    customProperties: tokens.customProperties,
    colors: Array.from(tokens.colors).slice(0, 50),
    fonts: Array.from(tokens.fonts).slice(0, 20),
    fontSizes: Array.from(tokens.fontSizes).sort((a, b) => parseFloat(a) - parseFloat(b)),
    spacing: Array.from(tokens.spacing).slice(0, 30),
    mediaQueries: Array.from(tokens.mediaQueries),
  };

  console.log('Token Extraction Result:', result);
  return result;
})();
