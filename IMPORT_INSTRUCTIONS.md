# Import Instructions for Beta Blueprint

## ✅ Beta Blueprint Created!

You can now import the beta version alongside your current blueprint without replacing it.

## Import URLs

### Main Blueprint (Current Stable)
```
https://github.com/samuelthng/t-house-blueprints/blob/main/notifications.yaml
```
**Name in HA**: "🔔 Notifications (Version 2.0.2 Beta)"

### Beta Blueprint (with iOS Fix)
```
https://raw.githubusercontent.com/samuelthng/t-house-blueprints/copilot/summarize-notification-blueprint/notifications_beta.yaml
```
**Name in HA**: "🔔 Notifications BETA (v2.1.1 - iOS Fixed)"

## What's Different in Beta?

### Critical iOS Fix
- **iOS tag truncation to 64 bytes** - Fixes notification failures on iOS devices
- Resolves Issue #47 where iOS users couldn't receive notifications in v2.0+
- Applied: `| truncate(64, killwords=True, end='')`

### Beta Features
- Separate name so it won't replace your current blueprint
- Beta warning banner in the UI
- Comprehensive changelog
- Can be tested alongside stable version

## How to Import in Home Assistant

1. Go to **Settings** → **Automations & Scenes** → **Blueprints**
2. Click **Import Blueprint** (bottom right)
3. Paste the beta URL above
4. Click **Preview Blueprint**
5. Click **Import Blueprint**

The beta will appear as a new, separate blueprint in your list!

## Testing

After importing, you can:
- Create a test script using the BETA blueprint
- Test iOS notifications
- Compare with your current working blueprint
- Keep both versions available

## Feedback

If the beta works well, especially for iOS users, please report back so we can merge the fix to the main branch.

---

**Status**: ✅ Ready to import and test!
