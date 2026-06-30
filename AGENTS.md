# AEGIS OS
# AI Engineering Guide

Version 0.2.0-alpha

---

# Purpose

This document provides engineering guidance for AI coding agents contributing to AEGIS OS.

Read this document before making any modifications.

Read PROJECT_BRIEF.md before reading this document.

---

# What is AEGIS?

AEGIS OS is an offline-first field operating system.

It is NOT:

- a Linux desktop
- a web dashboard
- a Python application
- a Raspberry Pi demo

It IS:

- a field terminal
- a resilience platform
- a knowledge appliance
- a community tool

Every contribution should reinforce this identity.

---

# Mission

Preserve knowledge.

Strengthen communities.

Remain operational.

---

# Engineering Philosophy

Before writing code ask:

Does this improve usability?

Does this improve maintainability?

Does this improve resilience?

If not, reconsider.

---

# Project Priorities

Priority 1

Reliability

Priority 2

Readability

Priority 3

Maintainability

Priority 4

Performance

Priority 5

Features

Never sacrifice architecture for feature count.

---

# Core Principles

Offline First

Human First

Keyboard First

Everything Searchable

Plain Files

Community Before Cloud

Modular Architecture

---

# User Experience

AEGIS should feel like operating equipment.

Not software.

Inspirations:

Garmin

Aircraft displays

Emergency Operations Centers

Public safety terminals

Amateur radio equipment

Never imitate desktop applications.

---

# Navigation

Every screen supports:

↑

↓

Enter

Escape

/

R

Q

No exceptions without strong justification.

---

# Code Organization

Business logic belongs in services.

Rendering belongs in screens.

Reusable UI belongs in widgets.

Shared behavior belongs in core.

Appearance belongs in themes.

Never mix responsibilities.

---

# File Size

Prefer:

Functions under 50 lines.

Files under 300 lines.

Split files when they become difficult to understand.

---

# Python Standards

Use:

Type hints

Dataclasses where appropriate

Meaningful names

Docstrings

Avoid:

Magic numbers

Global state

Duplicate code

Nested conditionals

Large functions

---

# Documentation

Every meaningful feature updates:

README

CHANGELOG

ROADMAP

Relevant specifications

Documentation is part of the feature.

---

# Git

One logical change per commit.

Write meaningful commit messages.

Never leave main broken.

Never intentionally commit failing code.

---

# UI

High contrast.

Readable.

Minimal.

Consistent.

Calm.

Professional.

Never flashy.

---

# Home Screen

The home screen is mission-oriented.

It should answer only:

"What would you like to do?"

Diagnostics belong elsewhere.

---

# Hardware

Hardware owns:

CPU

Memory

Storage

Temperature

Power

GPIO

Battery

Network

---

# Knowledge

Knowledge is the primary capability.

Never compromise Knowledge for aesthetics.

Search quality is more important than animations.

---

# Journal

The Journal is a field notebook.

Fast.

Simple.

Timestamped.

Searchable.

---

# Inventory

Inventory answers:

What?

Where?

How many?

When does it expire?

Nothing more.

---

# Plugins

Plugins must remain isolated.

Adding a plugin should never require changing Core.

---

# Search

Search is universal.

Search should include every capability whenever practical.

---

# Errors

Never expose Python tracebacks to operators.

Display friendly messages.

Write technical details to logs.

---

# Security

Offline first.

No telemetry.

No mandatory accounts.

No cloud dependency.

Least privilege.

---

# Raspberry Pi

Always preserve compatibility.

Never assume desktop hardware.

Optimize for PiTFT usability.

---

# Definition of Done

Code builds.

Code runs.

Pi boots.

PiTFT verified.

Documentation updated.

Git committed.

Main remains bootable.

---

# Final Instruction

You are not writing a Python application.

You are contributing to an operating environment.

Every decision should make AEGIS feel more like dedicated field equipment and less like a Linux computer.

Prepared Together.