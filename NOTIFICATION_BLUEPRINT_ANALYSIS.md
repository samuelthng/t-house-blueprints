# Notification Blueprint Analysis

## Summary

The **Notifications Blueprint** (v2.0.2 Beta) is a Home Assistant script blueprint that provides an enhanced notification experience for the Home Assistant Companion app. It wraps the native notification service with additional features like actionable buttons, timeout handling, and camera snapshots.

### What the Blueprint Does

The blueprint creates a script that sends notifications to Home Assistant Companion app users (iOS and Android) with these core capabilities:

1. **Actionable Notifications**: Up to 3 customizable action buttons with configurable titles, icons (iOS), and behaviors
2. **Timeout Handling**: Automatically triggers actions if no response is received within a specified duration
3. **Camera Snapshots**: Attach camera entity snapshots to notifications
4. **Flexible Response Handling**: Options can trigger Home Assistant actions or open URIs/links
5. **Platform-Specific Features**: Supports both iOS and Android with platform-appropriate configurations
6. **Notification Management**: Options for persistent notifications, auto-clearing, and notification links
7. **Response Variables**: Exposes response data through variables for use in automations

### Key Features Implemented

#### Notification Content
- ✅ **Title** - Notification title
- ✅ **Subtitle** - Additional subtitle text
- ✅ **Message** - Main notification body (supports HTML on Android)
- ✅ **Icon** - Custom notification icon (Android only)
- ✅ **Icon Color** - Custom icon color (Android only)

#### Action Buttons (Up to 3)
- ✅ **Custom Titles** - Each button has configurable text
- ✅ **Action Mode Selection** - Choose between Home Assistant actions or URI links
- ✅ **Home Assistant Actions** - Execute any Home Assistant action sequence
- ✅ **URI Links** - Open apps, deep links, entity info, or URLs
- ✅ **Icons** - SF Symbols for iOS action buttons
- ✅ **Destructive Style** - Red destructive button styling (iOS only)
- ✅ **Authentication Required** - Require device unlock to use action (iOS only)

#### Timeout Features
- ✅ **Configurable Timeout Duration** - Set how long to wait for response
- ✅ **Timeout Actions** - Execute actions when timeout occurs
- ✅ **Swipe-Away Handling** - Trigger timeout on notification dismissal (Android)
- ✅ **Auto-Clear on Timeout** - Automatically dismiss notification after timeout

#### Attachments
- ✅ **Camera Entity Snapshots** - Attach live camera snapshots to notifications
  - iOS: Camera stream support
  - Android: Automatic snapshot via camera proxy

#### Notification Behavior
- ✅ **Notification Link** - Navigate to specific URL/view when notification is tapped
- ✅ **Tag** - Unique identifier for notification replacement/updates
- ✅ **Group ID** - Group related notifications together
- ✅ **Persistent** - Prevent accidental swipe-away (Android)
- ✅ **Android Auto** - Show notifications in car interface (Android)

#### Priority & Importance
- ✅ **Channel** - Custom notification channel (Android)
- ✅ **Importance Level** - Urgent, Default, Silent, or Low (Android)
- ✅ **High Priority Mode** - Force timely delivery with high priority + ttl:0 (Android)
- ✅ **Interruption Level** - Silent, Default, Time-Sensitive, or Critical (iOS)
- ✅ **Lockscreen Visibility** - Public, Private, or Secret visibility (Android)

#### Script Fields
- ✅ **Override Capability** - All inputs can be overridden via script fields for dynamic use
- ✅ **Response Variable** - Access notification response data in automations

---

## Comparison to Home Assistant Companion Capabilities

Based on the [Home Assistant Companion documentation](https://companion.home-assistant.io/docs/notifications/notifications-basic/), here's how the blueprint compares:

### Features IMPLEMENTED in Blueprint ✅

| Feature | Blueprint Support | Notes |
|---------|------------------|-------|
| Title | ✅ Full | Direct input field |
| Message | ✅ Full | Supports HTML on Android |
| Subtitle | ✅ Full | Direct input field |
| Notification Link/URL | ✅ Full | Opens on notification tap |
| Actionable Buttons | ✅ Full | Up to 3 buttons with actions/URIs |
| Tag (Replace/Update) | ✅ Full | Unique identifier for notifications |
| Group | ✅ Full | Group related notifications |
| Channel (Android) | ✅ Full | Custom notification channels |
| Importance (Android) | ✅ Full | 4 levels: high, default, low, min |
| Priority (Android) | ✅ Full | High priority mode with ttl:0 |
| Interruption Level (iOS) | ✅ Full | 4 levels: passive, active, time-sensitive, critical |
| Persistent (Android) | ✅ Full | Prevent swipe-away |
| Lockscreen Visibility (Android) | ✅ Full | public, private, secret |
| Camera Attachments | ✅ Full | Camera entity snapshots |
| Icon (Android) | ✅ Full | Custom notification icon |
| Icon Color (Android) | ✅ Full | RGB color picker |
| Android Auto | ✅ Full | Car UI display |
| Action Icons (iOS) | ✅ Full | SF Symbols support |
| Destructive Actions (iOS) | ✅ Full | Red button styling |
| Authentication Required (iOS) | ✅ Full | Unlock requirement |

### Features NOT IMPLEMENTED (Limitations) ❌

| Feature | Status | Impact | Workaround |
|---------|--------|--------|-----------|
| **Sound/Custom Sounds** | ❌ Not Implemented | Cannot set custom notification sounds per notification | Use notification channels (Android) or device settings (iOS) |
| **Vibration Pattern** | ❌ Not Implemented | Cannot customize vibration | Configure via notification channel (Android) |
| **LED Color** | ❌ Not Implemented | Cannot set LED notification color | Configure via notification channel (Android) |
| **Badge** | ❌ Not Implemented | Cannot set or clear app badge count | Use `notify.mobile_app` service directly |
| **Image Attachments** (static) | ❌ Not Implemented | Cannot attach static images from URLs or local files | Only supports camera entity snapshots |
| **Video Attachments** | ❌ Not Implemented | Cannot attach video files (Android feature) | Not supported |
| **Audio Attachments** | ❌ Not Implemented | Cannot attach audio clips | Not supported |
| **Media Source Integration** | ❌ Not Implemented | Cannot use `/media/` path for attachments | Not supported |
| **WWW Folder Attachments** | ❌ Not Implemented | Cannot use `/local/` path for static images | Only camera entities |
| **Reply/Text Input Actions** | ❌ Not Implemented | Cannot collect text input from notification actions | Not supported |
| **Multiple Device Support** | ❌ Intentionally Limited | Can only send to one device at a time | Call script multiple times for multiple devices |
| **Notification Commands** | ❌ Not Implemented | Cannot use special commands (clear_notification, update_widgets, etc.) | Use service calls directly |
| **Progress Bars** | ❌ Not Implemented | Cannot show notification progress indicators (Android) | Not supported |
| **Expandable Text** | ❌ Not Implemented | Cannot use big text or inbox style (Android) | Not supported |
| **Chronometer** | ❌ Not Implemented | Cannot show countdown/countup timer (Android) | Not supported |
| **Action URIs with Feedback** | ⚠️ Partial | Android URI actions don't send events, can't stop timeout | Use action mode instead of URI mode |
| **TTS Notifications** | ❌ Not Implemented | Cannot trigger text-to-speech with notification | Not supported |
| **Wearable Extension** | ❌ Not Implemented | No Apple Watch/Wear OS specific features | Not supported |
| **Message Threading** | ❌ Not Implemented | Cannot create threaded conversation-style notifications (iOS) | Not supported |
| **Summary Text** | ❌ Not Implemented | Cannot set custom summary for notification groups (Android) | Not supported |

### Known Issues & Platform Limitations

1. **iOS Compatibility**: Newer features may not work well on some iOS setups (documented in blueprint)
2. **Event Reception**: Some setups have difficulty receiving `mobile_app_notification_action` events
3. **Android URI Actions**: URI-mode actions don't send events to Home Assistant, preventing timeout cancellation
4. **Single Device Only**: By design, cannot send to multiple devices (timeout feature conflict)

---

## Recommendations for Enhancement

If the blueprint were to be extended, here are high-priority features to consider:

### High Priority
1. **Image Attachments**: Support for static images via URL or `/local/` path
2. **Sound Support**: Add custom sound options where platform allows
3. **Reply Actions**: Enable text input collection from notifications
4. **Media Source Integration**: Support `/media/` paths for authenticated access

### Medium Priority
5. **Badge Management**: Add options to set/clear badge count
6. **Video Attachments**: Support video on Android
7. **Progress Indicators**: Support for progress bars (Android)
8. **Message Threading**: iOS conversation-style notifications

### Low Priority (Advanced)
9. **Wearable Extensions**: Apple Watch and Wear OS specific features
10. **TTS Integration**: Trigger text-to-speech along with visual notification
11. **Chronometer**: Countdown/timer displays (Android)

---

## Conclusion

The Notifications Blueprint provides a robust, user-friendly wrapper around Home Assistant's native notification service. It excels at:

- **Actionable notifications** with sophisticated timeout handling
- **Cross-platform support** with platform-specific optimizations  
- **Camera integration** for security and monitoring use cases
- **Flexible configuration** via blueprint inputs and script fields

**Current limitations** are primarily around:

- **Rich media attachments** (images, video, audio files)
- **Audio customization** (sounds, vibration, TTS)
- **Advanced notification types** (progress bars, replies, threads)
- **Multi-device scenarios** (intentional design choice)

For most notification use cases—particularly security alerts, device status, and interactive confirmations—this blueprint provides excellent functionality. Users needing advanced media attachments or audio customization should consider using the native `notify.mobile_app` service directly or extending this blueprint.

**Version**: Analysis based on Notifications Blueprint v2.0.2 Beta  
**Date**: February 2026  
**Documentation Reference**: [Home Assistant Companion Docs](https://companion.home-assistant.io/docs/notifications/notifications-basic/)
