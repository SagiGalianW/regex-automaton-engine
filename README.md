# Regex Automaton Engine 🔍🤖

Welcome to **Regex Automaton Engine** — a Python-based engine that builds and simulates finite automata (both NFA and DFA) from custom regular expressions written in a simplified syntax.

---

## ✨ Features

- ✅ Parse custom regular expressions (regex) with:
  - `|` → OR
  - `$` → CONCATENATION
  - `+` → ONE OR MORE
- ✅ Build Nondeterministic Finite Automata (NFA) with ε-transitions
- ✅ Convert NFA to Deterministic Finite Automata (DFA)
- ✅ Minimize DFA to smallest equivalent machine
- ✅ Simulate DFA on input strings
- ✅ Friendly console interface and examples

---

## 🧠 Custom Regex Syntax

This engine uses a **simplified syntax**, designed for clarity and ease of parsing.  
All operators must be wrapped with parentheses on both sides.

• To use '|': (?|?)
• To use '$': (?$?)
• To use '+': ((?)+)
• To use '*': ((?)*)
• ? - state for a valid machine
• For atoms e.g., 'a' -> (a) is a valid machine that accept a
• Operators must be binary → e.g., ((a)|(b)) NOT ((a)|(b)|(c))

---

