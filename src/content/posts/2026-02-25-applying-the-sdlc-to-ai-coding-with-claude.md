---
title: Applying the Software Development Lifecycle to AI-Assisted Coding with Claude Code
date: '2026-02-25'
zone: field
author: jtdub
tags:
- Research
- Claude Code
- AI-Assisted Development
- SDLC
- Software Engineering
- LLM
- iOS Development
- Prompt Engineering
- Developer Productivity
- Agentic Coding
- Claude
---

The rise of AI coding tools has introduced a new and often underestimated challenge: without structure, they tend to produce unstructured results. Many developers new to AI-assisted development treat these tools as a shortcut, submitting loosely defined prompts and expecting production-ready code in return. The results are predictably inconsistent.

What I have found, through direct experimentation, is that the most reliable way to produce quality software with an AI coding assistant is to apply the same disciplined methodology that has guided software engineering for decades: the Software Development Lifecycle (SDLC). When Claude Code CLI is used within this framework, the output is not just functional code, but maintainable, tested, and well-structured software.

This post walks through how I apply each phase of the SDLC using Claude Code, with the goal of giving developers new to AI-assisted coding a replicable process they can adopt immediately.

---

## Step 1: Requirements Gathering — Plan First, Code Never (Yet)

In traditional software development, requirements gathering is the foundation upon which everything else is built. Skipping or rushing this phase is one of the most common sources of rework and technical debt. The same principle applies when working with an AI coding assistant.

I begin every project by prompting Claude to develop a plan, with an explicit instruction not to write any code. A representative prompt looks like this:

> "Let's create a plan to write an iOS app. I don't currently need Android support. In the app, I want to be able to define a user and perform an Acute Mountain Sickness evaluation using the Lake Louise method. Don't create any code. Let's just create an implementation plan."

Claude responds by asking clarifying questions about data persistence, third-party dependencies, project structure, and anticipated edge cases. This exchange mirrors a formal requirements gathering session, with Claude functioning as both a business analyst and a technical consultant. The dialogue continues until the scope is well-defined and both parties, so to speak, are aligned.

The value of this step cannot be overstated. Ambiguities resolved at the requirements stage cost nothing. Ambiguities discovered during implementation are expensive.

---

## Step 2: System Design — Turn the Plan Into Artifacts

With requirements established, the next phase in the SDLC is system design: translating what the software must do into a blueprint for how it will be built. In my workflow, this phase produces three concrete artifacts before any code is written.

The first is an **implementation plan markdown file**, which documents the overall architecture, technology choices, and the phased approach to development. The second is a **`CLAUDE.md` file**, a configuration document that Claude Code reads at the start of every session. I use this file to define and enforce project standards: all GitHub issues must have corresponding tests, linters must pass without error, and no code may be committed until both conditions are satisfied. The third artifact is a set of **GitHub Issues**, automatically organized by development phase. Claude groups these logically (for example, Phase 1: Core Data Models, Phase 2: UI Layer), producing a structured backlog that drives all subsequent work.

At the conclusion of this phase, I function purely as a reviewer, validating that the scope and sequencing of the backlog reflect the original requirements. No implementation has occurred, yet the project already has a clear and auditable roadmap.

---

## Step 3: Implementation and Testing — Let Claude Build, Phase by Phase

With a design in place and a structured backlog established, implementation begins. I initiate each phase with a straightforward prompt:

> "Start working on the Phase 1 issues from GitHub."

Claude Code proceeds autonomously, creating files, authoring tests, executing linters, and iterating until all quality gates defined in `CLAUDE.md` are satisfied. I monitor for permission prompts that require human authorization, but otherwise my involvement during active implementation is minimal.

Upon phase completion, I build the project locally and evaluate it against three criteria: the absence of build errors or warnings, the absence of unexpected debug output, and the correctness of the user experience. Any deficiencies are communicated to Claude in plain language, initiating a correction loop that continues until the phase meets acceptance criteria. Using the Opus model, this loop is typically brief.

Once a phase is accepted, I instruct Claude to open a pull request. I review the results of the GitHub Actions pipeline and conduct a code review. For well-architected projects, such as a Swift iOS application following the Model-View-Controller pattern, this review is straightforward. Upon approval, the code is merged, the working branch is updated, and the process advances to the next phase.

---

## Step 4: Maintenance — Treat Code Review as a Deliverable

In many development workflows, code review is treated as a prerequisite to merging rather than as a systematic quality assurance activity. In my process, I conduct a dedicated, project-wide code review after the bulk of the application is implemented, treating it as a formal deliverable in its own right.

I prompt Claude to perform a comprehensive review of the entire codebase. It surfaces latent bugs, identifies areas for improvement, and occasionally flags features that were implied by the original requirements but not explicitly implemented. Each finding is converted into a GitHub issue, with defects prioritized ahead of enhancements. This ensures the project enters its next iteration with a clean, prioritized backlog and a codebase that has been deliberately examined rather than simply assembled.

---

## Why This Approach Produces Better Results

The effectiveness of this methodology rests on three principles that experienced software engineers will recognize immediately.

**Context determines output quality.** An AI model, like a human developer, produces better work when it has access to complete and well-organized context. A detailed implementation plan, a `CLAUDE.md` encoding project standards, and structured GitHub issues provide Claude with the same foundational understanding a competent engineer would expect before writing a single line of code.

**Quality must be enforced structurally, not assumed.** Requiring tests and linter compliance before every commit transforms quality assurance from a best-effort practice into a hard constraint. The code does not advance until it meets the standard.

**Human oversight remains essential.** This process does not eliminate the developer; it elevates the developer's role. By reviewing plans before implementation and pull requests before merging, the developer functions as an architect and technical lead, while Claude handles execution. The separation of responsibilities is clear and productive.

---

## Getting Started

For developers interested in adopting this methodology, the following sequence provides a practical starting point:

1. Install [Claude Code CLI](https://docs.anthropic.com/en/docs/claude-code) and initialize a new project session.
2. Write a requirements prompt describing the intended application, with an explicit instruction to produce no code.
3. Iterate on the plan through dialogue until the scope is well-defined.
4. Request the generation of an implementation plan, a `CLAUDE.md` file, and a set of phased GitHub Issues.
5. Review and approve the backlog before any implementation begins.
6. Proceed through the phases sequentially, applying the build-test-review loop at each stage.

In practice, I completed a working iOS application through this process in an evening.

The capabilities of modern AI coding tools are, by most measures, remarkable. What they lack is process. The SDLC provides it.
