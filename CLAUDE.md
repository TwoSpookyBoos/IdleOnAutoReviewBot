# IdleOn AutoReview Bot

Flask app (`mysite/`) that parses an IdleOn save (JSON) and renders advice (`/results`).
Python code lives under `mysite/`; setup is in `README.md`.

## Commands

Run from `mysite/`:

- Tests: `python -m pytest tests/`
- Lint: `ruff check <files>`
- Format: `ruff format <files>`

## Models

Typed classes under `models/` parse the save; `models/caverns/` is the reference
implementation. Section builders (`w1`..`w7`, `general/`, `caverns/`, `master_classes/`)
read model fields directly, so grep the **whole** repo before renaming, deleting or making
a field private.

- **Value objects own their state.** E.g. a bonus's `value` returns 0 itself when locked;
  callers don't reimplement unlock gating. A value object needing its parent gets a
  back-reference (`self.cavern`) and looks things up lazily.
- **Advice builders** are named `get_advice()` (variants: `get_bonus_advice()`,
  `get_unlock_advice()`). If a variant differs only by a flag, build it from
  `get_advice()` and override the attribute instead of duplicating the `Advice(...)` call.
- Per-index special cases: common logic first, then `match self.index:` with a `case _:`
  fallback.
- Cross-cutting alerts go through `Account.add_alert_list(group, [advice_or_none])` (it
  drops `None`s), not `alerts_Advices[...].append()`.

## Derived values

- A derived value is a `@cached_property` on the model that owns it, computed on first
  access. A cheap value derived only from parsed fields can be a plain attribute set
  while parsing. Don't add new `calculate_*` calls to `Account.calculate()`.
- Other systems are read through `session_data.account`, imported at module top:

  ```python
  from models.general.session_data import session_data

  @cached_property
  def sodium_safety_level(self) -> int:
      # Depends on: atom_collider['Sodium - Snail Kryptonite']
      return session_data.account.atom_collider["Sodium - Snail Kryptonite"].level * 5
  ```

  Leave a `# Depends on:` comment listing cross-system reads. Don't pass `account` or
  other systems through constructors. `models/general/session_data.py` imports `Account`
  only under `TYPE_CHECKING` — keep it that way, or the import becomes circular.
- **Never read `session_data.account` while parsing** (`__init__`/`parse()` or module
  level): it is assigned only after `Account(...)` returns.
- **Properties are pure**: no alerts, no logging, no changes to other objects.
- **Don't shadow** a `cached_property` with a same-named attribute set in
  `__init__`/`parse()`: the attribute wins and the property never runs.

## Refactoring

- Port logic 1:1, including quirks. If something looks like a bug, ask before changing
  behavior.
- A pure refactor must render byte-identical `/results` HTML for a real save.
- When a formula changes numbers, verify it against the decompiled game source or a real
  account. Game code uses `2.30259` as ln(10) (`safer_math_log(..., "Lava")`) — keep it.

## Style

- Code follows `ruff format`. Bring the code you change to it where possible, but don't
  reformat untouched parts of a file in the same change.
- For files with pre-existing lint debt, compare `ruff check` counts before/after rather
  than expecting zero.
