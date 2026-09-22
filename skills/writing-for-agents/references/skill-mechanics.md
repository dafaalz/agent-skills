# Skill mechanics

This guide covers skill-specific mechanics for `writing-for-agents`, including frontmatter, invocation choices, and router skills. Universal writing rules live in `../SKILL.md`.

## Invocation

Skills balance context load against cognitive load through two invocation modes:

- A **model-invoked** skill includes a description so the agent can discover and run it autonomously. Other skills can also reach it. Humans can still invoke it by typing its name. The description acts as a top-level context pointer that stays loaded at all times. A model-invoked skill containing reference material can serve as shared documentation for other skills. To configure, omit `disable-model-invocation` and write a description that lists trigger conditions.
- A **user-invoked** skill hides the description from the agent. Only a human typing the skill name can run it. This costs zero context load, but it increases cognitive load because the human must remember the skill exists. To configure, set `disable-model-invocation: true` and write a short human-facing summary without trigger lists.

Choose model invocation when the agent must reach the skill independently, or when another skill needs to call it. If a skill runs only through manual user command, make it user-invoked to save context.

If two user-invoked skills need shared reference material, move that material to a standalone markdown file outside the skill directory. Both skills can then link to that file directly.

## Splitting by invocation

Split off a model-invoked skill when you have a distinct leading word that should trigger it independently, or when multiple other skills need to consult its material. Each new model-invoked skill adds permanent context load through its description, so verify that independent discovery justifies the token cost.

## Router skills

When user-invoked skills multiply beyond what a human can easily track, create a router skill. A router skill is a single user-invoked skill that lists related skills and explains when to pick each one. This gives the human one entry point instead of dozens. A router skill cannot run user-invoked skills directly, but it directs the human to the right command.
