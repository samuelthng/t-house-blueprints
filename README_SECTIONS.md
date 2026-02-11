# Notifications Blueprint - With Organized Sections

## Import URL

```
https://raw.githubusercontent.com/samuelthng/t-house-blueprints/copilot/summarize-notification-blueprint/notifications.yaml
```

## What's New

### Organized Sections ✅

All 49 inputs are now organized into **7 collapsible sections** following the Blackshome blueprint pattern:

1. **Device & Notification Content** (4 inputs) - `mdi:cellphone-message`
   - Device selection, title, subtitle, message

2. **Action Buttons** (24 inputs) - `mdi:gesture-tap-button`
   - All 3 action options with their configurations
   - Includes iOS-specific action settings (icons, destructive, auth)

3. **Timeout Settings** (6 inputs) - `mdi:timer-outline`
   - Timeout configuration and behavior

4. **Attachments** (2 inputs) - `mdi:camera`
   - Camera snapshots and image attachments

5. **Links & Behavior** (3 inputs) - `mdi:link-variant`
   - Notification links, tags, groups

6. **iOS Specific Settings** (1 input) - `mdi:apple` 🆕
   - Interruption level

7. **Android Specific Settings** (9 inputs) - `mdi:android` 🆕
   - Icon and icon color
   - Channel, importance, high priority
   - Visibility, persist, car UI

Each section:
- Has an icon for visual identification
- Is collapsed by default for cleaner UI
- Contains related inputs grouped logically

### Platform-Specific Organization ✅

Settings are now organized by platform:

**iOS Settings:**
- Interruption level (passive, active, time-sensitive, critical)
- Action button icons (SF Symbols) - in Action Buttons section
- Destructive action styling - in Action Buttons section
- Authentication required - in Action Buttons section

**Android Settings:**
- Notification icon and color
- Channel and importance levels
- High priority mode
- Lockscreen visibility
- Persistent notifications
- Android Auto (car UI)

### iOS Fix Included ✅

- Tags truncated to 64 bytes to prevent iOS notification failures
- Fixes issue where long entity IDs caused iOS to reject notifications

## Section Structure

Following the Blackshome Sensor Light blueprint pattern:

```yaml
input:
  section_name:
    name: "Section Title"
    icon: mdi:icon-name
    collapsed: true
    input:
      field1: {...}
      field2: {...}
```

This is the **correct and tested** structure that Home Assistant recognizes for collapsible sections.

## Requirements

- Home Assistant 2024.6.0 or later (for blueprint section support)

## Features

All original notification features plus:
- Better organization with visual icons
- Platform-specific settings separated for clarity
- Collapsed sections for cleaner interface
- Easier to find and configure settings
- iOS notification fix included
