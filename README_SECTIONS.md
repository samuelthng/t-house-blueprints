# Notifications Blueprint - With Organized Sections

## Import URL

```
https://raw.githubusercontent.com/samuelthng/t-house-blueprints/copilot/summarize-notification-blueprint/notifications.yaml
```

## What's New

### Organized Sections ✅

All 49 inputs are now organized into **6 collapsible sections** following the Blackshome blueprint pattern:

1. **Device & Notification Content** (7 inputs) - `mdi:cellphone-message`
2. **Action Buttons** (24 inputs) - `mdi:gesture-tap-button`
3. **Timeout Settings** (6 inputs) - `mdi:timer-outline`
4. **Attachments** (2 inputs) - `mdi:camera`
5. **Links & Behavior** (5 inputs) - `mdi:link-variant`
6. **Priority & Importance** (5 inputs) - `mdi:bell-ring`

Each section:
- Has an icon for visual identification
- Is collapsed by default for cleaner UI
- Contains related inputs grouped logically

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
- Collapsed sections for cleaner interface
- Easier to find and configure settings
- iOS notification fix included
