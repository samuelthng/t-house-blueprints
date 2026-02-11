# ✅ Import Instructions - Beta Blueprint with Sections

## IMPORTANT: Use the Correct URL!

### ✅ CORRECT Import URL (Use This!)

```
https://raw.githubusercontent.com/samuelthng/t-house-blueprints/copilot/summarize-notification-blueprint/notifications_beta.yaml
```

**This URL points to the latest version with proper sections that Home Assistant can import.**

### ❌ Don't Use Old URLs

If you see an error like "extra keys not allowed @ data['blueprint']['input']['action_buttons']['collapse']", it means you're using an old URL with the wrong structure.

## What's in the Beta?

### Features
- ✅ **6 Collapsible Sections** - Properly organized inputs
- ✅ **iOS Tag Fix** - Truncates tags to 64 bytes (fixes iOS notification failures)
- ✅ **All 49 Inputs** - Organized logically
- ✅ **Beta Warning** - Banner to distinguish from main blueprint

### Sections
1. Device & Notification Content (7 inputs)
2. Action Buttons (24 inputs)
3. Timeout Settings (6 inputs)
4. Attachments (2 inputs)
5. Links & Behavior (5 inputs)
6. Priority & Importance (5 inputs)

## How to Import

1. Open **Home Assistant**
2. Navigate to **Settings** → **Automations & Scenes** → **Blueprints**
3. Click **Import Blueprint** (bottom right corner)
4. **Paste the URL above**
5. Click **Preview Blueprint**
6. Click **Import Blueprint**

## Expected Result

- ✅ Blueprint imports successfully (no errors)
- ✅ Name: "🔔 Notifications (Version 2.0.2 Beta)"
- ✅ 6 sections visible and collapsible
- ✅ Yellow beta warning banner
- ✅ Can be used alongside your existing blueprint

## Troubleshooting

### Error: "extra keys not allowed...collapse"
**Problem**: You're using an old URL with `collapse: true` syntax  
**Solution**: Use the correct URL above (with `/notifications_beta.yaml` at the end)

### Blueprint doesn't show sections
**Problem**: Old cached version  
**Solution**: Remove and re-import using the correct URL

### Can't find the sections
**Problem**: Might be looking at old version  
**Solution**: Check the blueprint name includes "BETA" or version number

---

**Blueprint Name**: "🔔 Notifications (Version 2.0.2 Beta)"  
**Version**: 2.1.1 BETA - With Sections  
**Status**: ✅ Ready to import!
