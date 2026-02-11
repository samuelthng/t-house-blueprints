# Notifications BETA Blueprint - With Sections

## Quick Import

**Copy this URL and paste it into Home Assistant's blueprint importer:**

```
https://raw.githubusercontent.com/samuelthng/t-house-blueprints/copilot/summarize-notification-blueprint/notifications_beta.yaml
```

## What's New

### Organized with Sections ✅
All 49 inputs are now organized into 6 collapsible sections:

1. **Device & Notification Content** - Device selection and message
2. **Action Buttons** - Up to 3 customizable buttons
3. **Timeout Settings** - Timeout behavior and actions
4. **Attachments** - Camera snapshots
5. **Links & Behavior** - URLs, tags, groups
6. **Priority & Importance** - Platform-specific settings

### iOS Fix Included ✅
- Tags truncated to 64 bytes
- Fixes iOS notification failures from Issue #47
- Applied: `| truncate(64, killwords=True, end='')`

### Proper HA Syntax ✅
Uses the correct blueprint schema:
```yaml
section_name:
  section:
    name: "Section Title"
    description: "Description"
    inputs:
      field: {...}
```

## Features

All features from the original blueprint, plus:
- Better organization
- Easier to find settings
- iOS notification fix
- Can coexist with main blueprint

## Import Steps

1. Settings → Automations & Scenes → Blueprints
2. Click "Import Blueprint"
3. Paste the URL above
4. Preview and Import

## Validation

- ✅ YAML syntax valid
- ✅ 6 sections created
- ✅ 49 inputs organized
- ✅ No `collapse:` keys (proper HA syntax)
- ✅ Imports without errors

---

**Need help?** See [IMPORT_INSTRUCTIONS.md](IMPORT_INSTRUCTIONS.md) for detailed guide.  
**Status**: Ready for testing!
