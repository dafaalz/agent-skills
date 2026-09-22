---
name: graphify
description: Use when turning codebases, documentation, research papers, or media into a persistent knowledge graph, or querying structural dependencies.
---

# Graphify

Turn code repositories, documentation, research papers, and media into an interactive knowledge graph with community clustering and graph-guided exploration.

## Usage

| Invocation | Action |
|---|---|
| `/graphify [path]` | Scan directory or document and build full knowledge graph in `graphify-out/`. |
| `/graphify query "<question>"` | Query graph directly for god nodes, architectural patterns, and cross-cutting paths. |
| `/graphify update` | Incrementally re-scan modified files and update existing graph without full re-run. |
| `/graphify add <file>` | Extract entities from new file and graft onto active graph. |
| `/graphify --watch` | Monitor scan root and incrementally update graph on file changes. |

## Core workflow

Follow these steps in sequence:

### Step 0. Repository triage and path merge

When processing a GitHub URL or multiple disparate paths, triage inputs before scanning:
- Clone remote repositories or consolidate input paths into a local working directory.
- For multi-repo guidance, consult `references/github-and-merge.md`.

Completion criterion. Target paths resolved to a local filesystem root.

### Step 1. Environment check and interpreter detection

Ensure graphify is installed and record the active Python interpreter:

```bash
mkdir -p graphify-out
which graphify || pip install graphifyy
which uv && uv tool which graphify > graphify-out/.graphify_python 2>/dev/null || which python3 > graphify-out/.graphify_python
echo "INPUT_PATH" > graphify-out/.graphify_scan_root
```

Completion criterion. `graphify-out/.graphify_python` contains a verified Python executable path.

### Step 2. File and media detection

Scan the target directory to catalog corpus file types:

```bash
$(cat graphify-out/.graphify_python) -c "
import json
from pathlib import Path
from graphify.detect import detect_corpus
result = detect_corpus(Path('INPUT_PATH'))
Path('graphify-out/.graphify_detect.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
print(f'Detected {result.get(\"total_files\", 0)} files')
"
```

If video or audio files are detected, transcribe them before extraction following `references/transcribe.md`.

Completion criterion. `graphify-out/.graphify_detect.json` written with file counts mapped by category.

### Step 3. Structural and semantic extraction

Run structural AST analysis for code and parallel semantic extraction for documents:
- AST extraction parses code files into deterministic nodes and import edges.
- Semantic extraction dispatches subagents to extract concept entities and latent relationships.
- Follow the execution scripts in `references/extraction-pipeline.md` and subagent prompt specifications in `references/extraction-spec.md`.

Completion criterion. `graphify-out/.graphify_extract.json` written with merged AST and semantic nodes.

### Step 4. Graph construction and community clustering

Construct the graph model, detect community clusters, and generate initial analytics:

```bash
$(cat graphify-out/.graphify_python) -c "
import json
from pathlib import Path
from graphify.build import build_graph_from_extract
extract_data = json.loads(Path('graphify-out/.graphify_extract.json').read_text(encoding='utf-8'))
graph = build_graph_from_extract(extract_data, root='INPUT_PATH')
graph.to_json('graphify-out/graph.json')
"
```

Completion criterion. `graphify-out/graph.json` generated on disk.

### Step 4.5. Graph health check gate

Verify graph integrity before generating user-facing outputs:
- Confirm node count exceeds zero.
- Check that edge count and community clusters meet structural sanity thresholds.

Completion criterion. Graph integrity confirmed with zero missing node references.

### Step 5. Community labeling

Label detected communities based on member nodes and cohesion:
- Review top god nodes and clustered domains.
- Assign human-readable semantic labels to each community cluster.

Completion criterion. All community clusters stamped with distinct descriptive labels.

### Step 6. Output generation and visualization

Generate interactive visualization and export formats:

```bash
graphify export html --input graphify-out/graph.json --output graphify-out/graph.html
```

When flags like `--obsidian`, `--neo4j`, or `--svg` are provided, consult `references/exports.md`.

Completion criterion. Interactive `graphify-out/graph.html` written and accessible in browser.

### Step 7. Manifest persistence, cleanup, and reporting

Persist corpus manifest for future incremental updates, update token cost ledger, and remove temporary chunk files:
- Run the persistence script detailed in `references/manifest-and-reporting.md`.
- Report god nodes, surprising connections, and suggested questions to the user.

Completion criterion. Corpus manifest saved to disk, temporary chunks deleted, and summary report displayed.

## Subcommands and references

Consult specialized reference guides for advanced operations:
- Query syntax and graph navigation: `references/query.md`
- Incremental updates and re-clustering: `references/update.md`
- Continuous watching and live sync: `references/add-watch.md`
- Git hooks and project documentation integration: `references/hooks.md`

## Honesty rules

1. State facts directly from the graph structure without exaggerating connectivity.
2. If a node has no structural connections, state that it is isolated.
3. Distinguish between extracted source relationships and inferred semantic edges.
