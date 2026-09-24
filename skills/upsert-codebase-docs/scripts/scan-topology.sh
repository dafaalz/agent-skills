#!/usr/bin/env bash
# scan-topology.sh analyzes directory topology and detects documentation targets

set -euo pipefail

TARGET_DIR="${1:-.}"
cd "$TARGET_DIR"

TOPOLOGY="single-root"
TARGETS=()
MANIFESTS=()

# Check for multi-tier decoupled architecture
if [[ -d "backend" && -d "frontend" ]]; then
    if [[ -f "backend/composer.json" || -f "backend/package.json" || -f "backend/Cargo.toml" ]] && \
       [[ -f "frontend/package.json" ]]; then
        TOPOLOGY="multi-tier-decoupled"
        TARGETS+=("AGENTS.md (Root Orchestrator)")
        TARGETS+=("backend/AGENTS.md" "backend/CODEBASE.md")
        TARGETS+=("frontend/AGENTS.md" "frontend/CODEBASE.md")
    fi
fi

# Check for desktop hybrid (Tauri)
if [[ "$TOPOLOGY" == "single-root" && -d "src-tauri" ]]; then
    if [[ -f "src-tauri/Cargo.toml" && -f "package.json" ]]; then
        TOPOLOGY="desktop-hybrid"
        TARGETS+=("AGENTS.md" "CODEBASE.md")
    fi
fi

# Check for monorepo workspace
if [[ "$TOPOLOGY" == "single-root" ]]; then
    if [[ -f "pnpm-workspace.yaml" || -f "turbo.json" || -f "nx.json" || -f "lerna.json" ]]; then
        TOPOLOGY="monorepo-workspace"
        TARGETS+=("AGENTS.md (Root Monorepo Router)" "CODEBASE.md (Workspace Topology)")
    fi
fi

# Fallback to single-root application
if [[ "$TOPOLOGY" == "single-root" ]]; then
    TARGETS+=("AGENTS.md" "CODEBASE.md")
fi

# Detect manifests present
[[ -f "composer.json" ]] && MANIFESTS+=("composer.json")
[[ -f "package.json" ]] && MANIFESTS+=("package.json")
[[ -f "Cargo.toml" ]] && MANIFESTS+=("Cargo.toml")
[[ -f "pyproject.toml" ]] && MANIFESTS+=("pyproject.toml")
[[ -f "go.mod" ]] && MANIFESTS+=("go.mod")
[[ -f "backend/composer.json" ]] && MANIFESTS+=("backend/composer.json")
[[ -f "frontend/package.json" ]] && MANIFESTS+=("frontend/package.json")
[[ -f "src-tauri/Cargo.toml" ]] && MANIFESTS+=("src-tauri/Cargo.toml")

echo "{"
echo "  \"directory\": \"$(pwd)\","
echo "  \"topology\": \"$TOPOLOGY\","
echo "  \"manifests\": ["
for i in "${!MANIFESTS[@]}"; do
    if [[ $i -lt $((${#MANIFESTS[@]} - 1)) ]]; then
        echo "    \"${MANIFESTS[$i]}\","
    else
        echo "    \"${MANIFESTS[$i]}\""
    fi
done
echo "  ],"
echo "  \"recommended_targets\": ["
for i in "${!TARGETS[@]}"; do
    if [[ $i -lt $((${#TARGETS[@]} - 1)) ]]; then
        echo "    \"${TARGETS[$i]}\","
    else
        echo "    \"${TARGETS[$i]}\""
    fi
done
echo "  ]"
echo "}"
