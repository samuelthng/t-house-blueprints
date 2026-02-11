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

## User Feedback & Common Issues

Based on analysis of the [GitHub Issues](https://github.com/samuelthng/t-house-blueprints/issues) and [Community Forum](https://community.home-assistant.io/t/notifications-actionable-mobile-notifications-script-with-optional-timeout-feature-and-camera-snapshots-works-with-ios-android/551552), here are the most common complaints and issues reported by users:

### Critical Bugs (Open Issues)

#### 1. **UndefinedError on Timeout** ([Issue #43](https://github.com/samuelthng/t-house-blueprints/issues/43))
- **Status**: Open (Bug confirmed by developer)
- **Symptom**: Error `'None' has no attribute 'event'` when notification times out
- **Root Cause**: Incomplete handling of all timeout condition permutations
- **Impact**: Script fails when timeout occurs in certain configurations
- **Workaround**: None yet - developer acknowledged but fix pending
- **Affected Users**: Multiple users reporting (3+ comments)

#### 2. **iOS Notifications Not Working on Newer Versions** ([Issue #47](https://github.com/samuelthng/t-house-blueprints/issues/47))
- **Status**: Open
- **Symptom**: Last working version is 1.4; newer versions don't send iOS notifications
- **Root Cause**: Unknown - potentially iOS-specific code changes in v2.0+
- **Impact**: Users cannot upgrade to access new features (image attachments, etc.)
- **Workaround**: Downgrade to version 1.4
- **Affected Users**: iOS users only

#### 3. **Notifications Don't Work Off LAN** ([Issue #50](https://github.com/samuelthng/t-house-blueprints/issues/50))
- **Status**: Open
- **Symptom**: Notifications work on local network but fail when device is off-network (via HA Cloud)
- **Root Cause**: Likely not blueprint-specific (developer suggests checking notification setup)
- **Impact**: Critical feature loss when users are away from home
- **Workaround**: Check HA Cloud and companion app configuration
- **Note**: Developer indicates this is likely a configuration issue, not a blueprint bug

### Common Complaints & Limitations

#### 4. **Script Mode Concurrency Issues**
- **Source**: Community forum discussions
- **Issue**: Script uses `mode: restart`, which interrupts first notification when second is triggered
- **Scenario**: Multiple automations triggering the same script simultaneously
- **Impact**: Only the last notification completes; earlier ones are cancelled
- **User Request**: Support for "parallel" script mode
- **Developer Response**: Acknowledged but warns it may break other features
- **Workaround**: Create separate script instances for each automation

#### 5. **Camera Snapshot Timing Delay** ([Issue #44](https://github.com/samuelthng/t-house-blueprints/issues/44))
- **Status**: Open
- **Issue**: Camera snapshot shows time of notification receipt, not trigger time
- **Scenario**: Delayed notification delivery (poor network) shows outdated snapshot
- **Example**: Trigger at 15:33, notification arrives at 15:35 with 15:35 snapshot
- **User Request**: Pre-capture snapshot and store as .jpg at trigger time
- **Impact**: Security/monitoring use cases show wrong moment
- **Workaround**: None - requires blueprint redesign

#### 6. **Android Notification Clearing**  ([Issue #41](https://github.com/samuelthng/t-house-blueprints/issues/41))
- **Status**: Open
- **Issue**: Clear notification commands only sent to iOS devices
- **Impact**: Android notifications persist even when cleared in automation
- **Documentation**: HA companion docs show clearing works on both platforms
- **User Workaround**: Edit blueprint to remove iOS-only condition
- **Additional Request**: Support for sticky notifications (Android)

#### 7. **Multi-Device Support**
- **Source**: Multiple forum requests
- **Current Status**: Intentionally not supported (FAQ states conflict with timeout feature)
- **User Need**: Send same notification to multiple devices (e.g., doorbell to all phones)
- **Impact**: Requires calling script multiple times or custom solutions
- **Developer Position**: "Sadly, no" - timeout feature incompatible with multi-device

#### 8. **Cross-Instance Camera Images** ([Issue #42](https://github.com/samuelthng/t-house-blueprints/issues/42))
- **Status**: Closed
- **Issue**: Camera image URLs are relative, fail if companion app points to different HA instance
- **Impact**: Multi-instance setups can't see camera attachments
- **Resolution**: Closed (likely addressed or workaround exists)

### Development Status

- **Active Development**: Paused (2024) due to personal reasons
- **Community Support**: Active on GitHub and forums
- **Updates**: Irregular but blueprint still widely used
- **Support**: Community-driven troubleshooting and workarounds

### User Sentiment

**Positive Feedback**:
- Described as "game changer" by users
- Praised for flexibility and active (historical) development
- Excellent for security/automation scenarios
- Well-documented with clear examples

**Frustrations**:
- Concurrency/parallel notification handling
- iOS compatibility issues with newer versions
- Lack of multi-device native support
- Some bugs remain unfixed due to paused development

### Troubleshooting Tips from Community

1. **Notifications Not Showing**:
   - Verify Home Assistant Companion app permissions
   - Check notification channels (Android)
   - Disable battery optimization for HA app
   - Test `mobile_app_notification_action` event reception
   - Review Do Not Disturb/Focus mode settings
   - Ensure app is updated (iOS: 2023.4+, Android: 2023.8.2+)

2. **Event Reception Issues**:
   - Navigate to Developer Tools → Events
   - Listen to `mobile_app_notification_action`
   - Trigger notification and select action
   - If no event appears, check network configuration

3. **Concurrency Problems**:
   - Create separate script instances for parallel automations
   - Consider using direct `notify.mobile_app` calls for simple cases
   - Avoid triggering same script from multiple automations simultaneously

4. **iOS Upgrade Issues**:
   - If newer versions fail, try version 1.4 (last known stable for some users)
   - Check [releases page](https://github.com/samuelthng/t-house-blueprints/releases) for version history

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

**Known bugs and issues**:
- **Timeout error handling** - UndefinedError in certain timeout scenarios (unfixed)
- **iOS compatibility** - Some users report v2.0+ doesn't work, requiring downgrade to v1.4
- **Script concurrency** - `mode: restart` causes notification conflicts with parallel automations
- **Camera snapshot timing** - Shows notification receipt time, not trigger time

For most notification use cases—particularly security alerts, device status, and interactive confirmations—this blueprint provides excellent functionality. **However, users should be aware**:

1. **Development is currently paused** - Bug fixes may not arrive promptly
2. **iOS users may experience issues** - Consider testing thoroughly or using v1.4
3. **Community support is active** - Forum and GitHub remain valuable resources
4. **Some bugs remain open** - Workarounds exist for most issues

Users needing advanced media attachments, guaranteed reliability, or multi-device support should consider using the native `notify.mobile_app` service directly or extending this blueprint with their own modifications.

---

## Resources & Links

- **GitHub Repository**: [samuelthng/t-house-blueprints](https://github.com/samuelthng/t-house-blueprints)
- **Community Forum**: [Notifications Blueprint Discussion](https://community.home-assistant.io/t/notifications-actionable-mobile-notifications-script-with-optional-timeout-feature-and-camera-snapshots-works-with-ios-android/551552)
- **GitHub Issues**: [Report bugs and request features](https://github.com/samuelthng/t-house-blueprints/issues)
- **HA Companion Docs**: [Notifications Documentation](https://companion.home-assistant.io/docs/notifications/notifications-basic/)
- **Release History**: [Older versions for compatibility](https://github.com/samuelthng/t-house-blueprints/releases)

---

**Version**: Analysis based on Notifications Blueprint v2.0.2 Beta  
**Analysis Date**: February 11, 2026  
**Blueprint Status**: Development paused (2024), community-supported  
**Data Sources**: GitHub Issues, Community Forum, HA Companion Documentation
