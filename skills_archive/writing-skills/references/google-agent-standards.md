# Google Agent Standards and Authoring Practices

This document compiles authoritative agent design and instruction standards from five official Google sources. Use these rules when authoring skills, system instructions, and tool workflows.

## 1. Google Cloud Dialogflow CX Playbooks

Sources:
- Playbook instructions (https://cloud.google.com/dialogflow/cx/docs/concept/playbook/instruction)
- Playbook best practices (https://cloud.google.com/dialogflow/cx/docs/concept/playbook/best-practices)

### Core rules
- Use hierarchical numbering for deterministic steps (`Step 1`, `Step 2`, `Step 2.1`) and indent sub-instructions.
- Reference tools with explicit identifiers and define expected inputs and outputs.
- Ground responses against tool outputs. Instruct the agent explicitly: "If the tool returns no data, state that the data is unavailable. Do not invent an answer."
- Break large playbooks into small, modular sub-playbooks with distinct goals.
- Forbid recursive calls and loops between agents.

## 2. Google Cloud Vertex AI Prompt Health Checklist

Source:
- Overview of prompting strategies (https://cloud.google.com/vertex-ai/generative-ai/docs/learn/prompts/prompt-design-strategies)

### Core rules
- Divide agent instructions into clear components: objective, instructions, constraints, context, output format, and examples.
- Eliminate overt manipulation. Do not use emotional appeals, flattery, artificial urgency, or simulated stress (such as "very bad things will happen"). Modern foundation models degrade when exposed to artificial pressure.
- Remove conflicting, redundant, or irrelevant instructions. Repeating a rule across multiple sentences with slight variations degrades model attention.
- Pair negative constraints with immediate positive actions. State what the agent must do instead of leaving a vacuum after a prohibition.
- Define objective constraints rather than vague adjectives. Replace "write a brief summary" with "write a summary of three sentences or less".

## 3. Google Gemini API System Instructions

Sources:
- System instructions (https://ai.google.dev/gemini-api/docs/system-instructions)
- Prompting strategies (https://ai.google.dev/gemini-api/docs/prompting-strategies)

### Core rules
- Define the operational scope and role boundaries before describing execution steps.
- Set deterministic execution order so the model completes prerequisites before moving forward.
- Use standardized data exchange formats such as JSON, YAML, or clean Markdown tables for tool interactions.

## 4. Google Antigravity Customization Architecture

Sources:
- Workspace Skills Guide (antigravity/builtin/skills/agy-customizations/docs/skills.md)
- Antigravity Customization System Guide (antigravity/builtin/skills/agy-customizations/SKILL.md)

### Core rules
- Practice progressive disclosure. Keep `SKILL.md` under 250 lines. Store deep reference material in `references/`, reusable scripts in `scripts/`, and working examples in `examples/`.
- Frontmatter naming: `name` must be lowercase and hyphenated (`kebab-case`).
- Frontmatter description: write in third person, starting with "Use when...". Describe triggering symptoms and conditions only. Never summarize the internal workflow in the description, or the agent may follow the summary and skip reading the skill body.
- Discovery locations: skills resolve from workspace projects (`.agents/skills/`), followed by global configuration (`~/.gemini/config/skills/`), and built-in mounts.
- Add deterministic validation steps. Every operational step must explain how the agent confirms success before proceeding.

## 5. Google Developer Documentation Style Guide

Sources:
- Active voice (https://developers.google.com/style/voice)
- Tone (https://developers.google.com/style/tone)
- Technical writing courses (https://developers.google.com/tech-writing)

### Core rules
- Write in the active voice. Name the actor before the action.
- Write in a direct, conversational, and respectful tone without decorative fluff.
- Strip jargon, idioms, and puffery.
- Use sentence case for all headings.
- Avoid em dashes, en dashes, and mid-sentence colons.
