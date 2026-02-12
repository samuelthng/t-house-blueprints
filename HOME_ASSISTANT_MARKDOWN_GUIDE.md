# Home Assistant Blueprint Markdown Guide

## Overview

Home Assistant's markdown rendering in blueprint descriptions has specific quirks that differ from standard markdown. This guide documents the rules for proper rendering.

---

## Critical Rules

### 1. Blank Lines Are Essential

**Rule**: In YAML `description: >-` blocks, you need **blank lines** to separate elements.

```yaml
# ❌ WRONG - Will render as one paragraph
description: >-
  First line of text.
  Second line of text.
  - List item 1
  - List item 2

# ✅ CORRECT - Properly separated
description: >-
  First line of text.

  Second line of text.

   - List item 1
   - List item 2
```

**Key Points**:
- Blank lines create proper separation for markdown parser
- Without blank lines, everything becomes one paragraph
- Lists MUST have blank line before them

---

### 2. Lists Require Space Before Hyphen

**Rule**: Bullet lists need a space before the hyphen: ` - item` not `- item`

```yaml
# ❌ WRONG
description: >-
  My list:
  - Item 1
  - Item 2

# ✅ CORRECT - Note the space before hyphen
description: >-
   - Item 1
   - Item 2
```

**Why**: Home Assistant's YAML parser needs the leading space to recognize bullets.

---

### 3. Lists Cannot Be Inline

**Rule**: You cannot put list items on the same line as header text.

```yaml
# ❌ WRONG - "Examples:" and list items run together
description: >-
  Examples: - Static text - Template text - Conditional text

# ❌ ALSO WRONG - Even with proper format, inline doesn't work
description: >-
  Examples:
   - Static text
   - Template text

# ✅ CORRECT - Blank line separates header from list
description: >-
  Examples:

   - Static text
   - Template text
   - Conditional text
```

---

### 4. Details Blocks Require Blank Lines

**Rule**: `<details>` blocks MUST have blank lines after `<summary>` and before `</details>` for markdown inside to render.

```yaml
# ❌ WRONG - Markdown won't render
description: >-
  <details>
  <summary>Click to expand</summary>
  **Bold text**
   - List item
  </details>

# ✅ CORRECT - Blank lines allow markdown parsing
description: >-
  <details>
  <summary>Click to expand</summary>

  **Bold text**

   - List item 1
   - List item 2

  </details>
```

**Critical**: Without the blank lines, content appears as raw unformatted text.

---

### 5. Two Lines Create One Blank Line

**Rule**: In HA YAML descriptions, need 2 blank lines in source to create 1 blank line in display.

```yaml
# To create visual spacing in HA UI:
description: >-
  First paragraph.


  Second paragraph (appears with 1 blank line above in UI).
```

**Note**: This applies to the `>-` folded scalar style in YAML.

---

### 6. Bold and Code Formatting

**Rule**: Bold and code work normally, but need proper line separation.

```yaml
# ✅ CORRECT
description: >-
  **Bold text** works fine on its own line.

  `Code snippets` work inline.

  For multi-line code or lists with code:

   - Example: `code here`
   - Another: `more code`
```

---

## Working Patterns

### Pattern 1: Simple Description with List

```yaml
description: >-
  Main description text goes here.

  Available options:

   - Option 1: Description
   - Option 2: Description
   - Option 3: Description

  📖 [Documentation Link](https://example.com) | Optional
```

### Pattern 2: Description with Examples

```yaml
description: >-
  Field purpose and description.

  Examples:

   - Static: `Simple static text`
   - Template: `{{ template.code }}`
   - Conditional: `{% if condition %}text{% endif %}`

  📖 [Docs](https://link) | Platform | Status
```

### Pattern 3: Description with Details Block

```yaml
description: >-
  Brief description here.

  <details>
  <summary>Click for more details</summary>

  **Section Header:**

   - Detail point 1
   - Detail point 2
   - Detail point 3

  Additional explanation text.

  </details>

  Default: Value
```

### Pattern 4: Description with Multiple Sections

```yaml
description: >-
  Primary description of the field.

  How it works:

   - Step 1: Description
   - Step 2: Description
   - Step 3: Description

  Use case: Example scenario text here.

  📖 [Documentation](https://link) | Optional
```

---

## Common Mistakes

### Mistake 1: Inline Lists

```yaml
# ❌ WRONG - Renders as paragraph, not list
description: >-
  Select mode: - Option A - Option B - Option C
```

**Fix**: Put list on separate lines with blank line before.

### Mistake 2: Missing Space Before Hyphen

```yaml
# ❌ WRONG - Won't render as list
description: >-
  Options:
  - Item 1
  - Item 2
```

**Fix**: Add space before hyphen: ` - Item 1`

### Mistake 3: No Blank Line Before List

```yaml
# ❌ WRONG - List won't separate from text
description: >-
  Choose from these options:
   - Option 1
   - Option 2
```

**Fix**: Add blank line between text and list.

### Mistake 4: Details Block Without Blank Lines

```yaml
# ❌ WRONG - Content won't be parsed as markdown
description: >-
  <details>
  <summary>More info</summary>
  **This won't be bold**
   - This won't be a list
  </details>
```

**Fix**: Add blank lines after `<summary>` and before `</details>`.

---

## Blueprint Main Description

The main blueprint description (lines 9-280) works differently - it can use more complex HTML because it's not inside a `description: >-` field.

**In main description** (works):
- HTML tags: `<div>`, `<ul>`, `<li>`, `<h2>`, `<b>`, etc.
- Blockquotes: `>` for indented sections
- Complex nesting

**In field descriptions** (limited):
- Markdown: Lists, bold, code, links
- Simple HTML: `<details>`, `<summary>`, `<br>` (discouraged)
- Must follow blank line rules strictly

---

## Testing Checklist

When writing HA blueprint descriptions:

- [ ] Blank line before every list
- [ ] Space before hyphen in lists: ` - item`
- [ ] Blank lines around headers/sections
- [ ] Blank line after `<summary>` in details
- [ ] Blank line before `</details>`
- [ ] No inline lists (header + list on same line)
- [ ] Code examples use backticks
- [ ] Links use markdown format: `[text](url)`
- [ ] Proper spacing for readability

---

## Quick Reference

| Element | Syntax | Notes |
|---------|--------|-------|
| Bullet List | ` - Item` | Space before hyphen, blank line before list |
| Bold | `**text**` | Works normally |
| Code | `` `code` `` | Works normally |
| Link | `[text](url)` | Works normally |
| Details | See Pattern 3 | Blank lines required |
| Paragraph break | Two blank lines | Creates one blank line in display |
| Header | `**Header:**` or HTML | Use bold for inline headers |

---

## Examples from Working Main Description

The main description (lines 9-280) demonstrates working patterns:

```yaml
description: >-
  <div>
    <h2>🔔 Notifications</h2>
    <b>Version info</b> | Links
  </div>


  <b>⚠️ BREAKING CHANGES:</b>
  <ul>
    <li>Item 1</li>
    <li>Item 2</li>
  </ul>


  ---


  ### Features

  <details>
  <summary>Expand/collapse features</summary>

   - Feature 1
   - Feature 2
   - Feature 3

  </details>
```

Note the double blank lines for spacing and proper list formatting.

---

## Summary

**Golden Rules**:
1. Blank lines are your friend - use them liberally
2. Lists need: blank line before + space before hyphen
3. Details blocks need: blank lines after summary and before close
4. Test in HA UI to verify rendering
5. Follow working examples from main description

**When in doubt**: Add blank lines and use the working patterns in this guide.
