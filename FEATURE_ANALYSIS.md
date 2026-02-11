# Notification Blueprint - Feature Gap Analysis

## Current Features (Implemented ✅)

### Basic Notification
- ✅ Title
- ✅ Subtitle  
- ✅ Message
- ✅ Device selection

### Action Buttons
- ✅ Up to 3 action buttons
- ✅ Button text
- ✅ Action sequences (Home Assistant actions)
- ✅ URI mode (Android deep links)
- ✅ SF Symbol icons (iOS)
- ✅ Destructive styling (iOS)
- ✅ Authentication required (iOS)

### Timeouts
- ✅ Enable/disable timeout
- ✅ Configurable duration
- ✅ Timeout actions
- ✅ Clear on timeout
- ✅ Swipe away as timeout (Android)

### Attachments
- ✅ Camera entity snapshots

### Links & Behavior
- ✅ Notification link (clickAction/url)
- ✅ Tag (notification ID)
- ✅ Group

### iOS Specific
- ✅ Interruption level (passive, active, time-sensitive, critical)

### Android Specific  
- ✅ Icon
- ✅ Icon color
- ✅ Channel
- ✅ Importance
- ✅ High priority mode
- ✅ Visibility (lockscreen)
- ✅ Persist (sticky)
- ✅ Car UI (Android Auto)

---

## Missing Features from HA Companion Documentation

### Priority: HIGH (Commonly Used) 🔴

| Feature | Platform | Input Name | Description | Implementation Complexity |
|---------|----------|------------|-------------|--------------------------|
| **Sound** | Both | `sound` | Custom notification sound | LOW |
| **Badge** | iOS | `badge` | App icon badge number | LOW |
| **Sticky** | Android | `sticky` | Non-dismissible notification | LOW |
| **Thread ID** | iOS | `thread_id` | Conversation grouping | LOW |
| **Image URL** | Both | `image_url` | Direct image URL (non-camera) | LOW |
| **Video URL** | Both | `video_url` | Attach video to notification | MEDIUM |
| **Presentation** | iOS | `presentation_options` | Banner/alert/sound/badge control | MEDIUM |
| **Critical Sound** | iOS | `critical_sound` | Volume & critical flag for sound | MEDIUM |
| **Action Categories** | iOS | `category` | Pre-defined action sets | MEDIUM |

### Priority: MEDIUM (Useful) 🟡

| Feature | Platform | Input Name | Description | Implementation Complexity |
|---------|----------|------------|-------------|--------------------------|
| **Subject** | Android | *(exists as auto-set)* | Notification subject line | N/A (already set) |
| **Vibration Pattern** | Android | `vibration_pattern` | Custom vibration | LOW |
| **LED Color** | Android | `led_color` | Notification LED color | LOW |
| **Chronometer** | Android | `chronometer` | Show timer/countdown | MEDIUM |
| **When** | Android | `when` | Override notification timestamp | LOW |
| **Ticker** | Android | `ticker` | Scrolling text in status bar | LOW |
| **Alert Once** | Android | `alert_once` | Sound/vibrate only once | LOW |
| **Reply Text** | Both | `action_reply_*` | Text input actions | HIGH |
| **Image Type** | iOS | `attachment_content_type` | Force image/video type | LOW |

### Priority: LOW (Advanced/Niche) 🟢

| Feature | Platform | Input Name | Description | Implementation Complexity |
|---------|----------|------------|-------------|--------------------------|
| **Actions Location** | iOS | `actions_location` | Inline/modal action display | LOW |
| **Target Content ID** | iOS | `target_content_id` | Notification threading | LOW |
| **Subtitle HTML** | Android | `subtitle_html` | HTML in subtitle | LOW |
| **Title HTML** | Android | `title_html` | HTML in title | LOW |
| **Message HTML** | Android | *(already works)* | HTML formatting | N/A |
| **Media Stream** | Android | `media_stream` | Audio stream type | LOW |
| **Shortcut ID** | Android | `shortcut_id` | Link to app shortcut | LOW |
| **Notification ID** | Android | `notification_id` | Numeric ID override | LOW |
| **Tag Suffix** | Android | `tag_suffix` | Append to tag | LOW |

---

## Backwards Compatibility Strategy

### Keep Existing Names
- ✅ All current input names remain unchanged
- ✅ All current field logic remains

### New Inputs
- Add to appropriate sections (iOS/Android/Common)
- Use optional defaults (won't break existing automations)
- Document platform-specific features clearly

### Fields Section
- Ensure every input has corresponding field
- Fields allow runtime override of blueprint inputs
- Use same naming pattern: `field_name` → `!input field_name`

---

## Implementation Priorities

### Phase 1: High Priority (Simple Additions) ✅
1. **sound** - Custom sound name/URL
2. **badge** (iOS) - App badge number
3. **sticky** (Android) - Non-dismissible
4. **thread_id** (iOS) - Conversation grouping  
5. **image_url** - Direct image URL
6. **video_url** - Video attachment
7. **vibration_pattern** (Android) - Custom pattern
8. **led_color** (Android) - LED color
9. **alert_once** (Android) - Single alert

### Phase 2: Medium Priority (Requires Logic) 🔄
1. **presentation_options** (iOS) - Array of options
2. **critical_sound** (iOS) - Volume + critical flag
3. **chronometer** (Android) - Timer display
4. **when** (Android) - Timestamp override
5. **ticker** (Android) - Status bar text

### Phase 3: Advanced (Complex) ⏳
1. **Reply actions** - Text input from notification
2. **Action categories** (iOS) - Pre-defined action sets
3. **Attachment content types** - Force media types

---

## Description Improvements Needed

### Current Issues
- Some descriptions lack practical examples
- Platform-specific features not always clearly marked
- Missing links to documentation
- No usage tips for complex features

### Improvements
1. Add **practical examples** to all descriptions
2. Clearly mark **🍎 iOS Only** and **🤖 Android Only**
3. Add **links to official docs** where helpful
4. Include **common use cases** in tooltips
5. Note **requirements** (e.g., requires HA 2024.x)

---

## Next Steps

1. ✅ Create this analysis document
2. ⏭️ Implement Phase 1 features (simple additions)
3. ⏭️ Update all descriptions with examples
4. ⏭️ Add fields for all inputs
5. ⏭️ Test YAML structure
6. ⏭️ Update documentation
7. ⏭️ Consider Phase 2 features if requested

