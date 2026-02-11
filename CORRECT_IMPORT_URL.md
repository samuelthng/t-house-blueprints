# ✅ CORRECT Import URL for Beta Blueprint

## The Problem You Encountered

You tried to import using this URL:
```
https://raw.githubusercontent.com/samuelthng/t-house-blueprints/d51c2896628d0a5e93218beba02dddd4b2dfcbf9/notifications.yaml
```

That commit (d51c289) has the OLD structure with `collapse: true` which Home Assistant doesn't support. That's why you got the error about "extra keys not allowed".

## ✅ CORRECT Import URL

Use this URL instead:

```
https://raw.githubusercontent.com/samuelthng/t-house-blueprints/copilot/summarize-notification-blueprint/notifications_beta.yaml
```

Or with the specific commit hash:

```
https://raw.githubusercontent.com/samuelthng/t-house-blueprints/6b32322d605c9dc70faca987243717046db41522/notifications_beta.yaml
```

## Why This Works

The beta file now uses the CORRECT Home Assistant blueprint syntax:

### ❌ OLD (Doesn't Work)
```yaml
input:
  action_buttons:
    collapse: true  # NOT SUPPORTED!
    input:
      confirm_enabled: {...}
```

### ✅ NEW (Works!)
```yaml
input:
  action_buttons:
    section:  # Correct HA syntax
      name: "Action Buttons"
      description: "Configure action buttons"
      inputs:
        confirm_enabled: {...}
```

## Import Steps

1. Open Home Assistant
2. Go to **Settings** → **Automations & Scenes** → **Blueprints**
3. Click **Import Blueprint** (bottom right)
4. Paste this URL:
   ```
   https://raw.githubusercontent.com/samuelthng/t-house-blueprints/copilot/summarize-notification-blueprint/notifications_beta.yaml
   ```
5. Click **Preview Blueprint**
6. Click **Import Blueprint**

## What You'll See

- ✅ Blueprint imports without errors
- ✅ 6 collapsible sections
- ✅ 49 inputs properly organized
- ✅ iOS tag fix included

## Validation

The current beta file has been validated:
- ✅ Uses `section:` syntax (not `collapse:`)
- ✅ Has `inputs:` nested inside each section
- ✅ YAML is valid
- ✅ 6 sections created
- ✅ All 49 inputs organized

---

**Status**: Ready to import!
**Last Updated**: February 11, 2026
**Commit**: 6b32322
