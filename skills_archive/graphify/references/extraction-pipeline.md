# Extraction pipeline: AST, semantic subagents, and merge

Run the extraction pipeline according to the active corpus types.

## Part A. Structural extraction for code files

For any code files detected, run AST extraction:

```bash
$(cat graphify-out/.graphify_python) -c "
import sys, json
from graphify.extract import collect_files, extract
from pathlib import Path

code_files = []
detect = json.loads(Path('graphify-out/.graphify_detect.json').read_text(encoding='utf-8'))
for f in detect.get('files', {}).get('code', []):
    code_files.extend(collect_files(Path(f)) if Path(f).is_dir() else [Path(f)])

if code_files:
    result = extract(code_files, cache_root=Path('INPUT_PATH'))
    Path('graphify-out/.graphify_ast.json').write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f'AST: {len(result[\"nodes\"])} nodes, {len(result[\"edges\"])} edges')
else:
    Path('graphify-out/.graphify_ast.json').write_text(json.dumps({'nodes':[],'edges':[],'input_tokens':0,'output_tokens':0}, ensure_ascii=False), encoding='utf-8')
    print('No code files, skipping AST extraction')
"
```

## Part B. Semantic extraction (parallel subagents)

If detection found zero docs, papers, and images (code-only corpus), write the empty semantic file:

```bash
$(cat graphify-out/.graphify_python) -c "
import json
from pathlib import Path
Path('graphify-out/.graphify_semantic.json').write_text(json.dumps({'nodes':[],'edges':[],'hyperedges':[],'input_tokens':0,'output_tokens':0}), encoding='utf-8')
"
```

For non-code content files:
1. Check extraction cache:

```bash
$(cat graphify-out/.graphify_python) -c "
import json
from graphify.cache import check_semantic_cache
from pathlib import Path

detect = json.loads(Path('graphify-out/.graphify_detect.json').read_text(encoding='utf-8'))
all_files = [f for cat in ('document', 'paper', 'image') for f in detect['files'].get(cat, [])]

cached_nodes, cached_edges, cached_hyperedges, uncached = check_semantic_cache(all_files, root='INPUT_PATH', prompt_file='SPEC_PATH')

if cached_nodes or cached_edges or cached_hyperedges:
    Path('graphify-out/.graphify_cached.json').write_text(json.dumps({'nodes': cached_nodes, 'edges': cached_edges, 'hyperedges': cached_hyperedges}, ensure_ascii=False), encoding='utf-8')
else:
    Path('graphify-out/.graphify_cached.json').unlink(missing_ok=True)
Path('graphify-out/.graphify_uncached.txt').write_text('\n'.join(uncached), encoding='utf-8')
print(f'Cache: {len(all_files)-len(uncached)} files hit, {len(uncached)} files need extraction')
"
```

2. Split uncached files into chunks of 20 to 25 files each (each image gets its own chunk).
3. Dispatch semantic extraction subagents using the prompt in `references/extraction-spec.md`.
4. Collect chunk outputs into `graphify-out/.graphify_chunk_0N.json`.

## Part C. Merge AST and semantic into final extraction

```bash
$(cat graphify-out/.graphify_python) -c "
import json, glob
from pathlib import Path
from graphify.cache import write_semantic_cache

ast = json.loads(Path('graphify-out/.graphify_ast.json').read_text(encoding='utf-8'))

semantic_nodes = []
semantic_edges = []
semantic_hyperedges = []
total_input_tokens = ast.get('input_tokens', 0)
total_output_tokens = ast.get('output_tokens', 0)

chunk_files = sorted(glob.glob('graphify-out/.graphify_chunk_*.json'))
for cf in chunk_files:
    try:
        chunk = json.loads(Path(cf).read_text(encoding='utf-8'))
        semantic_nodes.extend(chunk.get('nodes', []))
        semantic_edges.extend(chunk.get('edges', []))
        semantic_hyperedges.extend(chunk.get('hyperedges', []))
        total_input_tokens += chunk.get('input_tokens', 0)
        total_output_tokens += chunk.get('output_tokens', 0)
    except Exception as e:
        print(f'Warning: failed to read {cf}: {e}')

cached_path = Path('graphify-out/.graphify_cached.json')
if cached_path.exists():
    try:
        cached = json.loads(cached_path.read_text(encoding='utf-8'))
        semantic_nodes.extend(cached.get('nodes', []))
        semantic_edges.extend(cached.get('edges', []))
        semantic_hyperedges.extend(cached.get('hyperedges', []))
    except Exception as e:
        print(f'Warning: failed to read cache: {e}')

seen_ids = set()
deduped_nodes = []
for n in ast.get('nodes', []) + semantic_nodes:
    nid = n.get('id')
    if nid and nid not in seen_ids:
        seen_ids.add(nid)
        deduped_nodes.append(n)

all_edges = ast.get('edges', []) + semantic_edges

result = {
    'nodes': deduped_nodes,
    'edges': all_edges,
    'hyperedges': semantic_hyperedges,
    'input_tokens': total_input_tokens,
    'output_tokens': total_output_tokens
}
Path('graphify-out/.graphify_extract.json').write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding='utf-8')
print(f'Merged: {len(deduped_nodes)} nodes, {len(all_edges)} edges, {len(semantic_hyperedges)} hyperedges')
"
```
