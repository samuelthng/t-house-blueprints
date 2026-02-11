# Platform-Specific Features Mapping

Based on official Home Assistant Companion documentation research (Feb 2026)

## Common Features (Both iOS and Android)

### Notification Content
- **title** - Notification title
- **message** - Notification message body
- **subtitle** - Additional subtitle text
- **tag** - Unique identifier for notification replacement
- **group** - Group related notifications together

### Actionable Features
- **actions** - Up to 3 action buttons (recommended limit)
- **action titles** - Text for action buttons
- **action URIs** - Open URLs/deep links from actions

### Attachments
- **camera entity** - Camera snapshot attachments
- **images** - Image attachments (both platforms support)

### Links
- **notification_link / url / clickAction** - Navigate on notification tap

### Timeout & Behavior
- **timeout/ttl** - Time to live for notifications
- **clear notifications** - Clear notifications programmatically

---

## iOS-Specific Features

### Sound & Interruption
- **sound** - Custom notification sounds (name, critical, volume)
- **interruption-level** - iOS 15+ feature
  - `passive` - Silent, no screen wake
  - `active` - Default notification
  - `time-sensitive` - Bypass Focus modes
  - `critical` - Bypass Do Not Disturb (requires entitlement)
- **critical** - Critical alert flag (iOS 12+)
  - Bypasses mute and Do Not Disturb
  - Plays sound at specified volume
  - Always appears at top of lock screen

### Visual & Interaction
- **badge** - Control app badge count
- **presentation_options** - Control how notification displays

### Action Button Features (iOS Only)
- **action icons** - SF Symbols for action buttons
  - Specified via `sfsymbols:` prefix
  - Example: `sfsymbols:bell.fill`
- **destructive** - Red destructive action styling
- **authenticationRequired** - Require unlock to use action

### Media
- **video** - Video clips in notifications (rich media)
- **dynamic content** - Live camera feeds

### Watch Integration
- **Apple Watch** - Direct notifications to Apple Watch

---

## Android-Specific Features

### Notification Channels & Priority
- **channel** - Notification channel name/ID
  - Grouping and organization
  - Per-channel sound/vibration/LED settings
  - Importance set per channel (cannot change after creation)
- **importance** - Notification importance level
  - `max` - Makes sound with heads-up notification
  - `high` - Makes sound with heads-up notification
  - `default` - Makes sound
  - `low` - No sound
  - `min` - No sound, no status bar
- **priority** - FCM delivery priority
  - `high` - Fast delivery, breaks through dozing
  - `normal` - Standard delivery
- **ttl: 0** - Immediate delivery or discard (used with priority:high)

### Visual Customization
- **notification_icon** - Custom notification icon (mdi: icon name)
- **icon_color / color** - Custom icon color (hex or RGB)
- **led_color** - LED notification color

### Behavior
- **sticky** - Persistent notification (cannot swipe away)
- **persistent** - Same as sticky
- **timeout** - Auto-dismiss after duration
- **visibility** - Lockscreen visibility
  - `public` - Show all content
  - `private` - Show based on phone settings (default)
  - `secret` - Hide all content on lockscreen

### Android Auto
- **car_ui** - Display notification on Android Auto interface

### Message Formatting
- **HTML formatting** - Rich text in message body
  - Bold: `<b>text</b>`
  - Italic: `<i>text</i>`
  - Underline: `<u>text</u>`
  - Color: `<font color='red'>text</font>`

### Device Commands (Android Extensive)
Android supports many device-level commands:
- Screen brightness
- Bluetooth toggle
- App launching
- Ringer mode
- And many more via notification commands

### Wearable
- **Wear OS** - Wear OS smartwatch notifications

---

## Current Blueprint Field Classification

### Fields to Move to iOS Section:
1. `confirm_icon`, `dismiss_icon`, `option_three_icon` - SF Symbols
2. `confirm_is_destructive`, `dismiss_is_destructive`, `option_three_is_destructive`
3. `confirm_authentication_required`, `dismiss_authentication_required`, `option_three_authentication_required`
4. `interruption_level` - iOS 15+ interruption levels

### Fields to Move to Android Section:
1. `icon` - Custom notification icon
2. `enable_icon_color` - Enable icon color customization
3. `icon_color` - Icon color RGB
4. `channel` - Notification channel
5. `importance` - Channel importance (max, high, default, low, min)
6. `android_high_priority` - High priority mode flag
7. `visibility` - Lockscreen visibility (public, private, secret)
8. `persist` - Persistent/sticky notification flag
9. `swipe_away_as_timeout` - Trigger timeout on swipe
10. `car_ui` - Android Auto display

### Fields That Stay in Common Sections:
- `notify_device` - Device selection (common)
- `title`, `subtitle`, `message` - Content (common)
- `notification_link` - Click action (common, different names per platform)
- `tag`, `group` - Organization (common)
- Action buttons structure (common, but some properties are platform-specific)
- `attachment_type`, `attachment_camera_entity` - Attachments (common)
- `enable_timeout`, `timeout`, `timeout_action`, `clear_on_timeout` - Timeout (common concept)

---

## Missing Practical Fields to Consider Adding

### iOS Missing:
1. **sound** - Custom sound selection (currently not configurable)
2. **badge** - Badge count control
3. **presentation_options** - How notification presents

### Android Missing:
1. **sticky** - Explicit sticky flag (similar to persist, may add for clarity)
2. **led_color** - LED color (if still supported by devices)
3. **vibration_pattern** - Custom vibration (channel-level, informational)

### Both Platforms:
1. **clear_on_response** - Clear notification after action selected (from MB901 fork)
2. **sound** - Common sound field with platform-specific behavior

---

## Recommended New Structure

```yaml
input:
  # Section 1: Device & Content (Common)
  notification_content:
    notify_device, title, subtitle, message
  
  # Section 2: Action Buttons (Common structure, platform-specific properties)
  action_buttons:
    Options 1-3 with common fields
  
  # Section 3: Timeout Settings (Common)
  timeout_settings:
    enable_timeout, timeout, timeout_action, etc.
  
  # Section 4: Attachments (Common)
  attachments:
    attachment_type, camera_entity
  
  # Section 5: Links & General Behavior (Common)
  links_behavior:
    notification_link, tag, group, clear_on_timeout
  
  # Section 6: iOS Specific Settings (NEW)
  ios_settings:
    interruption_level
    # Action button properties: icons, destructive, auth (in subsections)
  
  # Section 7: Android Specific Settings (NEW)
  android_settings:
    icon, icon_color, enable_icon_color
    channel, importance, android_high_priority
    visibility, persist, swipe_away_as_timeout, car_ui
```

---

**Documentation Sources:**
- https://companion.home-assistant.io/docs/notifications/notifications-basic/
- https://companion.home-assistant.io/docs/notifications/critical-notifications/
- https://companion.home-assistant.io/docs/notifications/actionable-notifications/
- https://github.com/home-assistant/companion.home-assistant/blob/master/docs/notifications/basic.md
