# Lighthouse CI and Core Web Vitals automated gating

Configuration and flakiness prevention protocols for automated web performance and accessibility audits.

## 1. Deterministic configuration

Create `lighthouserc.cjs` in the project root.

```javascript
module.exports = {
  ci: {
    collect: {
      numberOfRuns: 3,
      startServerCommand: 'npm run preview',
      url: ['http://localhost:4173/'],
      settings: {
        preset: 'desktop',
        throttlingMethod: 'simulate',
      },
    },
    assert: {
      assertions: {
        'categories:performance': ['error', { minScore: 0.9 }],
        'categories:accessibility': ['error', { minScore: 0.95 }],
        'largest-contentful-paint': ['error', { maxNumericValue: 2500 }],
        'cumulative-layout-shift': ['error', { maxNumericValue: 0.1 }],
        'total-blocking-time': ['error', { maxNumericValue: 200 }],
      },
    },
    upload: {
      target: 'temporary-public-storage',
    },
  },
};
```

## 2. Flakiness prevention rules

Variable container CPU speeds create noisy test failures. Enforce these invariants.

1. Median of three runs. Always run at least 3 collection passes (`numberOfRuns: 3`). Lighthouse selects median values to neutralize cold cache anomalies.
2. Build preview over dev server. Audit against production builds (`npm run preview` or static dist folder). Never run Lighthouse CI against hot reloading dev servers (`vite` or `next dev`).
3. Mock dynamic network data. Route external API requests to deterministic local fixtures during audit runs to prevent external latency spikes.

## 3. Local and CI execution commands

Run Lighthouse CI via the standalone runner.

```bash
npx @lhci/cli@0.14.x autorun
```

A non-zero exit code blocks the pull request gate if any metric breaches defined thresholds.
