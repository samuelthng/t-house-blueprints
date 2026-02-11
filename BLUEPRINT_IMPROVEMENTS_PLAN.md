# Notification Blueprint - Comprehensive Improvements Plan

**Version**: 2.1.0 (Proposed)  
**Last Updated**: February 11, 2026  
**Status**: Planning Phase

---

## Table of Contents

1. [Critical Bug Fixes](#critical-bug-fixes)
2. [UI/UX Improvements](#uiux-improvements)
3. [Feature Enhancements](#feature-enhancements)
4. [Code Quality Improvements](#code-quality-improvements)
5. [Implementation Priority](#implementation-priority)
6. [Sources & References](#sources--references)

---

## Critical Bug Fixes

### 1. UndefinedError on Timeout (Issue #43)

**Status**: 🔴 Critical - Unfixed  
**Severity**: High  
**Affected Users**: Multiple reports

| Aspect | Details |
|--------|---------|
| **Problem** | Error `'None' has no attribute 'event'` when notification times out |
| **Root Cause** | Incomplete handling of all timeout condition permutations |
| **Scenario** | Occurs when timeout fires but trigger event is None |
| **Impact** | Script crashes, automation fails, no timeout actions executed |
| **Solution** | Add proper null/None checks before accessing `.event` attribute |
| **Code Location** | Timeout trigger handling section (around line 1100-1200) |
| **Fix Approach** | Wrap all `wait_for_trigger` result checks with null validation |

**Proposed Fix**:
```yaml
# Current (broken):
- alias: "Check which action was selected"
  variables:
    action_received: "{{ wait.trigger.event.data.action }}"

# Fixed:
- alias: "Check which action was selected"
  variables:
    action_received: >-
      {% if wait.trigger is not none and wait.trigger.event is defined %}
        {{ wait.trigger.event.data.action }}
      {% else %}
        "TIMEOUT"
      {% endif %}
```

---

### 2. Android Notification Clearing (Issue #41)

**Status**: 🟡 Medium Priority  
**Severity**: Medium  
**Affected Users**: Android users only

| Aspect | Details |
|--------|---------|
| **Problem** | Clear notification commands only sent to iOS devices |
| **Root Cause** | iOS-only condition in clearing logic |
| **Scenario** | Android notifications persist when they should be cleared |
| **Impact** | Notification clutter on Android devices |
| **Solution** | Remove iOS-only condition for clearing notifications |
| **Code Location** | Notification clearing section |
| **Documentation** | HA Companion docs confirm Android supports clearing |

**Proposed Fix**:
```yaml
# Current (broken):
- alias: "Clear notification"
  condition:
    - condition: template
      value_template: "{{ notification_data.apple_device }}"  # iOS only!
  service: notify.mobile_app_...
  data:
    message: clear_notification
    data:
      tag: "{{ tag }}"

# Fixed:
- alias: "Clear notification"
  # Remove iOS-only condition - works on both platforms
  service: notify.mobile_app_...
  data:
    message: clear_notification
    data:
      tag: "{{ tag }}"
```

---

### 3. iOS Compatibility Issues (Issue #47)

**Status**: 🔴 Critical - Unfixed  
**Severity**: High  
**Affected Users**: iOS users on v2.0+

| Aspect | Details |
|--------|---------|
| **Problem** | v2.0+ doesn't send iOS notifications; v1.4 is last working version |
| **Root Cause** | Unknown - possibly iOS-specific code changes |
| **Scenario** | Users cannot upgrade to access new features |
| **Impact** | iOS users stuck on old version, missing new features |
| **Solution** | Investigate differences between v1.4 and v2.0 iOS handling |
| **Investigation** | Compare device detection, payload structure, service calls |
| **Workaround** | Downgrade to v1.4 (temporary) |

**Investigation Needed**:
- Compare `device_attr(notify_device, "manufacturer")` handling
- Check iOS payload structure changes
- Verify service call format compatibility
- Test with different iOS versions and HA Companion app versions

---

## UI/UX Improvements

### 1. Grouped Input Sections with Collapse

**Status**: 🟢 Ready to Implement  
**Priority**: High  
**Source**: PR #48, PR #49 (MB901), Sensor Light Blueprint

| Current State | Proposed State |
|---------------|----------------|
| All inputs in flat list (60+ fields) | Grouped into 6-8 collapsible sections |
| No visual hierarchy | Clear visual organization with icons |
| Difficult to navigate | Easy to find relevant settings |
| No section descriptions | Helpful descriptions for each group |

**Proposed Section Structure**:

```yaml
input:
  # Section 1: Device & Notification Content
  notification_settings:
    name: "📲 Device & Notification Content"
    icon: mdi:cellphone-message
    collapsed: true
    input:
      notify_device: ...
      title: ...
      subtitle: ...
      message: ...
      icon: ...
      enable_icon_color: ...
      icon_color: ...

  # Section 2: Action Buttons
  action_buttons:
    name: "🔘 Action Buttons"
    icon: mdi:gesture-tap-button
    collapsed: true
    input:
      # Option 1
      confirm_enabled: ...
      confirm_text: ...
      # ... all option 1 fields
      # Option 2
      dismiss_enabled: ...
      # ... all option 2 fields
      # Option 3
      option_three_enabled: ...
      # ... all option 3 fields

  # Section 3: Timeout Settings
  timeout_settings:
    name: "⏱️ Timeout Settings"
    icon: mdi:timer-outline
    collapsed: true
    input:
      enable_timeout: ...
      timeout: ...
      run_timeout_actions: ...
      timeout_action: ...
      swipe_away_as_timeout: ...
      clear_on_timeout: ...

  # Section 4: Attachments
  attachment_settings:
    name: "📸 Attachments"
    icon: mdi:camera
    collapsed: true
    input:
      attachment_type: ...
      attachment_camera_entity: ...

  # Section 5: Links & Behavior
  behavior_settings:
    name: "🔗 Links & Behavior"
    icon: mdi:cog-outline
    collapsed: true
    input:
      notification_link: ...
      tag: ...
      group: ...
      persist: ...
      car_ui: ...

  # Section 6: Priority & Importance
  priority_settings:
    name: "🔔 Priority & Importance"
    icon: mdi:bell-alert
    collapsed: true
    input:
      # Android
      channel: ...
      importance: ...
      android_high_priority: ...
      visibility: ...
      # iOS
      interruption_level: ...
```

**Benefits**:
- 📊 Better organization and discoverability
- ⚡ Faster configuration for common use cases
- 📱 Cleaner mobile UI
- 🎯 Reduced cognitive load
- ✅ Matches modern HA blueprint patterns

---

### 2. Improved Field Descriptions

**Status**: 🟢 Ready to Implement  
**Priority**: Medium

| Issue | Solution |
|-------|----------|
| Some descriptions are too technical | Simplify language, add examples |
| Missing emoji indicators for platform | Add 🍎/🤖 consistently |
| No inline examples | Add example values in descriptions |
| Complex options need more help | Add expandable details sections |

**Example Improvements**:

```yaml
# Before:
confirm_uri:
  name: "1️⃣ Option 1 - Link"
  description: "Navigate to a link or app when this option is selected..."

# After:
confirm_uri:
  name: "1️⃣ Option 1 - Link"
  description: >
    Open a URL, app, or Home Assistant view when this button is tapped.
    
    **Examples**:
    - Dashboard: `/lovelace/security`
    - Website: `https://example.com`
    - 🤖 Android App: `app://io.homeassistant.companion.android`
    - 🤖 Android Entity: `entityId:camera.front_door`
    - 🍎 iOS App: `mailto:alert@example.com`
    
    ⚠️ Note: Android URI actions don't stop timeout countdown.
```

---

## Feature Enhancements

### 1. Multi-Device Support

**Status**: 🟡 Community Request  
**Priority**: High  
**Source**: PR #48, PR #49 (MB901), Multiple user requests

| Aspect | Details |
|--------|---------|
| **Current State** | Single device only (intentional limitation) |
| **User Request** | Send same notification to multiple devices |
| **Use Cases** | Doorbell to all family phones, emergency alerts |
| **Challenge** | Timeout feature conflict with multiple devices |
| **Proposed Solution** | Make multi-device optional with timeout warning |

**Implementation Options**:

**Option A: Simple Multi-Device (No Timeout)**
```yaml
notify_device:
  name: "📲 Device(s) to notify"
  description: >
    Select one or more devices to notify.
    ⚠️ Timeout actions only work with single device.
  selector:
    device:
      filter:
        - integration: mobile_app
      multiple: true  # Allow multiple

# In sequence:
- if:
    - condition: template
      value_template: "{{ notify_device is string }}"
  then:
    # Single device - full timeout support
  else:
    # Multiple devices - simplified notification, no timeout
```

**Option B: Auto-Detect All Devices (from PR #49)**
```yaml
notify_device:
  description: >
    Leave empty to notify ALL mobile devices automatically.
  default: []

# In sequence:
- variables:
    all_devices: >-
      {% if notify_device | length == 0 %}
        {{ states.device_tracker 
           | selectattr('attributes.source_type', 'eq', 'mobile_app')
           | map(attribute='entity_id') | list }}
      {% else %}
        {{ [notify_device] if notify_device is string else notify_device }}
      {% endif %}
```

**Option C: Broadcast Mode**
- Add new "broadcast" mode toggle
- When enabled, sends to all devices without waiting for responses
- Timeout actions run based on time only, not device responses
- Clear and simple UX

**Recommendation**: Option C with clear documentation about timeout limitations

---

### 2. Clear Notification on Response Received

**Status**: 🟢 Ready to Implement  
**Priority**: Medium  
**Source**: PR #48, PR #49 (MB901)

| Aspect | Details |
|--------|---------|
| **Problem** | Notifications persist after user responds |
| **User Request** | Auto-clear after action button press |
| **Benefit** | Cleaner notification tray |
| **Implementation** | Add optional toggle + clear action after response |

**Implementation**:
```yaml
clear_on_response:
  name: "🧹 Clear notification after action"
  description: "Automatically dismiss notification after action button is pressed."
  default: true
  selector:
    boolean:

# In sequence (after action is taken):
- if:
    - condition: template
      value_template: "{{ clear_on_response }}"
  then:
    - service: "{{ notify_service }}"
      data:
        message: clear_notification
        data:
          tag: "{{ tag }}"
```

---

### 3. Zone-Based Message Customization

**Status**: 🟢 Ready to Implement  
**Priority**: Low-Medium  
**Source**: PR #48, PR #49 (MB901)

| Aspect | Details |
|--------|---------|
| **Feature** | Different message based on device location |
| **Use Cases** | "Lock door" vs "Door was locked" based on home/away |
| **Benefit** | More contextual notifications |
| **Complexity** | Medium - requires zone detection |

**Implementation**:
```yaml
use_zone_based_message:
  name: "🗺️ Zone-Based Messages"
  description: "Customize message based on device location"
  default: false
  selector:
    boolean:

message_home:
  name: "💬 Message (At Home)"
  description: "Message when device is in home zone"
  default: ""
  selector:
    text:

message_away:
  name: "💬 Message (Away)"
  description: "Message when device is away from home"
  default: ""
  selector:
    text:

# In sequence:
- variables:
    final_message: >-
      {% if use_zone_based_message %}
        {% set device_zone = device_attr(notify_device, 'zone') %}
        {{ message_home if device_zone == 'home' else message_away }}
      {% else %}
        {{ message }}
      {% endif %}
```

---

### 4. Static Image Attachments

**Status**: 🟡 Requested  
**Priority**: Medium  
**Source**: Analysis document - missing feature

| Aspect | Details |
|--------|---------|
| **Current State** | Only camera entity snapshots supported |
| **User Request** | Support static images from URLs or `/local/` |
| **Use Cases** | Icons, logos, saved snapshots, custom graphics |
| **Benefit** | More visual notification options |

**Implementation**:
```yaml
attachment_type:
  selector:
    select:
      options:
        - label: "None"
          value: "none"
        - label: "Camera Entity"
          value: "camera_entity"
        - label: "Image URL"  # NEW
          value: "image_url"
        - label: "Local File"  # NEW
          value: "local_file"

attachment_image_url:
  name: "📸 Image URL"
  description: >
    Full URL to image (https://...) or local path (/local/image.jpg)
  default: ""
  selector:
    text:

# In payload:
- variables:
    image_attachment: >-
      {% if attachment_type == 'camera_entity' %}
        {{ camera_proxy_url }}
      {% elif attachment_type == 'image_url' %}
        {{ attachment_image_url }}
      {% elif attachment_type == 'local_file' %}
        {{ '/local/' + attachment_image_url }}
      {% endif %}
```

---

### 5. Pre-Capture Camera Snapshot

**Status**: 🟡 Requested  
**Priority**: Medium  
**Source**: Issue #44 - Camera snapshot timing

| Aspect | Details |
|--------|---------|
| **Problem** | Snapshot shows notification receipt time, not trigger time |
| **Impact** | Security/monitoring shows wrong moment |
| **User Request** | Pre-capture and store snapshot at trigger time |
| **Challenge** | Requires snapshot service + file storage |

**Implementation**:
```yaml
snapshot_timing:
  name: "📸 Snapshot Timing"
  description: "When to capture camera snapshot"
  default: "on_send"
  selector:
    select:
      options:
        - label: "On Send (default)"
          value: "on_send"
        - label: "Pre-Capture (stores snapshot)"
          value: "pre_capture"

# In sequence (at the start):
- if:
    - condition: template
      value_template: "{{ attachment_type == 'camera_entity' and snapshot_timing == 'pre_capture' }}"
  then:
    - service: camera.snapshot
      data:
        entity_id: "{{ attachment_camera_entity }}"
        filename: "/config/www/snapshots/notification_{{ now().timestamp() }}.jpg"
    - variables:
        snapshot_file: "/local/snapshots/notification_{{ now().timestamp() }}.jpg"
  else:
    - variables:
        snapshot_file: "{{ camera_proxy_url }}"
```

---

### 6. Script Mode Configuration

**Status**: 🟡 Requested  
**Priority**: Medium  
**Source**: Community forum - concurrency issues

| Aspect | Details |
|--------|---------|
| **Current State** | Hardcoded `mode: restart` |
| **Problem** | Concurrent notifications interrupt each other |
| **User Request** | Make script mode configurable |
| **Risk** | Other modes may break timeout logic |

**Implementation**:
```yaml
# At blueprint level:
mode: !input script_mode

# As input:
script_mode:
  name: "⚙️ Script Mode"
  description: >
    **Advanced Setting** - Controls how multiple simultaneous notifications are handled.
    
    - **Restart** (default): New notification cancels previous one
    - **Parallel**: Multiple notifications can run simultaneously (⚠️ may affect timeout)
    - **Queued**: Notifications wait for previous to complete
    - **Single**: Ignore new notifications while one is running
    
    ℹ️ Most users should keep default (Restart)
  default: "restart"
  selector:
    select:
      options:
        - label: "Restart (Cancel previous)"
          value: "restart"
        - label: "Parallel (Run simultaneously)"
          value: "parallel"
        - label: "Queued (Wait for previous)"
          value: "queued"
        - label: "Single (Ignore new)"
          value: "single"
```

---

### 7. Response Variable Enhancement

**Status**: 🟢 Implemented but Undocumented  
**Priority**: Low  
**Source**: v2.0.2 changelog

| Aspect | Details |
|--------|---------|
| **Current State** | `response_variable` exists but no documentation |
| **Enhancement** | Add examples and documentation |
| **Benefit** | Users can build advanced automations |

**Documentation Needed**:
```yaml
# Example automation using response variable:
automation:
  - alias: "Security Alert with Response Tracking"
    trigger:
      - platform: state
        entity_id: binary_sensor.motion
    action:
      - service: script.notification_blueprint
        response_variable: notification_response
        data:
          title: "Motion Detected"
          message: "Motion at front door"
      
      # Use the response:
      - service: logbook.log
        data:
          name: "Notification Response"
          message: >-
            User selected: {{ notification_response.action }}
            At: {{ notification_response.timestamp }}
```

---

## Code Quality Improvements

### 1. Add Error Handling

**Status**: 🟢 Ready to Implement  
**Priority**: High

| Area | Current State | Proposed Improvement |
|------|---------------|---------------------|
| Device validation | No check if device exists | Validate device before sending |
| Service call failures | No error handling | Try/catch with fallback |
| Template errors | Can crash script | Default values for all templates |
| Camera entity | No validation | Check if entity exists and is camera |

**Implementation Examples**:

```yaml
# Device validation:
- alias: "Validate device"
  condition:
    - condition: template
      value_template: >-
        {{ notify_device != none and 
           states['device_tracker.' + notify_device] is defined }}
  
# Service call with error handling:
- alias: "Send notification with error handling"
  try:
    - service: "{{ notify_service }}"
      data:
        title: "{{ title }}"
        message: "{{ message }}"
  rescue:
    - service: system_log.write
      data:
        message: "Failed to send notification to {{ notify_device }}"
        level: error
```

---

### 2. Improve Variable Initialization

**Status**: 🟢 Ready to Implement  
**Priority**: Medium

| Issue | Solution |
|-------|----------|
| Variables spread across sequence | Group all variables at start |
| Complex nested templates | Break into smaller, readable pieces |
| No default values | Add defaults for all optional inputs |
| Duplicate logic | Extract common patterns to variables |

**Example**:
```yaml
# Consolidate all variables at start:
- alias: "Initialize all variables"
  variables:
    # Device & Service
    notify_service: "notify.mobile_app_{{ device_attr(notify_device, 'name') | slugify }}"
    device_is_apple: "{{ 'APPLE' in (device_attr(notify_device, 'manufacturer')|upper) }}"
    
    # Notification Content
    final_title: "{{ field_title if field_title is defined else title }}"
    final_message: "{{ field_message if field_message is defined else message }}"
    final_subtitle: "{{ field_subtitle if field_subtitle is defined else subtitle }}"
    
    # Timeout Configuration
    enable_timeout: "{{ enable_timeout | default(true) }}"
    timeout_seconds: "{{ (timeout.hours * 3600) + (timeout.minutes * 60) + timeout.seconds }}"
    
    # Actions Configuration
    first_option: "OPTION_1_{{ tag }}"
    second_option: "OPTION_2_{{ tag }}"
    third_option: "OPTION_3_{{ tag }}"
```

---

### 3. Add Code Comments

**Status**: 🟢 Ready to Implement  
**Priority**: Low

| Section | Comments Needed |
|---------|----------------|
| Complex template logic | Explain what each part does |
| Platform-specific code | Why iOS/Android differs |
| Timeout handling | Document all condition permutations |
| Payload building | Explain structure |

---

### 4. YAML Syntax Validation

**Status**: 🟢 Ready to Implement  
**Priority**: High

**Add to repository**:
- `.yamllint` configuration
- GitHub Actions workflow for validation
- Pre-commit hooks (optional)

```yaml
# .github/workflows/validate.yml
name: Validate YAML
on: [push, pull_request]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: YAML Lint
        uses: ibiqlik/action-yamllint@v3
        with:
          file_or_dir: notifications.yaml
          config_file: .yamllint
```

---

## Implementation Priority

### Phase 1: Critical Bug Fixes (Week 1)
**Goal**: Fix breaking issues

- [ ] **P0**: Fix UndefinedError on timeout (Issue #43)
- [ ] **P0**: Fix Android notification clearing (Issue #41)
- [ ] **P0**: Add error handling for device validation
- [ ] **P1**: Investigate iOS compatibility (Issue #47)

### Phase 2: UI/UX Improvements (Week 2)
**Goal**: Improve user experience

- [ ] **P0**: Implement collapsed sections with icons
- [ ] **P0**: Reorganize inputs into logical groups
- [ ] **P1**: Improve field descriptions with examples
- [ ] **P1**: Add platform indicators (🍎/🤖) consistently
- [ ] **P2**: Update version to 2.1.0 and changelog

### Phase 3: Feature Enhancements (Week 3-4)
**Goal**: Add requested features

- [ ] **P1**: Implement "Clear on response" feature
- [ ] **P1**: Add static image attachment support
- [ ] **P2**: Add multi-device support (with limitations)
- [ ] **P2**: Implement configurable script mode
- [ ] **P3**: Add zone-based messaging
- [ ] **P3**: Add pre-capture camera snapshot

### Phase 4: Code Quality (Week 5)
**Goal**: Improve maintainability

- [ ] **P1**: Consolidate variable initialization
- [ ] **P1**: Add comprehensive error handling
- [ ] **P2**: Add code comments for complex sections
- [ ] **P2**: Set up YAML validation workflow
- [ ] **P3**: Document response_variable usage

### Phase 5: Testing & Documentation (Week 6)
**Goal**: Ensure reliability

- [ ] **P0**: Test all timeout scenarios
- [ ] **P0**: Test on iOS and Android devices
- [ ] **P1**: Update README with new features
- [ ] **P1**: Create migration guide from v2.0.2 to v2.1.0
- [ ] **P2**: Add troubleshooting section
- [ ] **P2**: Create example automations

---

## Testing Checklist

### Functional Testing

#### Timeout Scenarios
- [ ] Timeout with no action taken
- [ ] Timeout after option 1 selected
- [ ] Timeout after option 2 selected
- [ ] Timeout after option 3 selected
- [ ] Timeout with swipe-away
- [ ] No timeout (infinite wait)
- [ ] Timeout with no options enabled
- [ ] Timeout with camera attachment

#### Platform Testing
- [ ] iOS notification delivery
- [ ] iOS action buttons
- [ ] iOS notification clearing
- [ ] iOS camera snapshots
- [ ] iOS interruption levels
- [ ] Android notification delivery
- [ ] Android action buttons
- [ ] Android notification clearing
- [ ] Android camera snapshots
- [ ] Android importance levels

#### Feature Testing
- [ ] Single device notification
- [ ] Multi-device notification (if implemented)
- [ ] Camera entity snapshot
- [ ] Static image attachment (if implemented)
- [ ] Notification links (iOS & Android)
- [ ] Clear on response (if implemented)
- [ ] Clear on timeout
- [ ] Persistent notifications
- [ ] Response variable capture

#### Edge Cases
- [ ] Empty title/message
- [ ] Device offline
- [ ] Invalid camera entity
- [ ] Network timeout
- [ ] HA restart during notification wait
- [ ] Concurrent notifications (different script modes)

### UI/UX Testing
- [ ] All sections collapse/expand correctly
- [ ] Icons display properly
- [ ] Field descriptions are clear
- [ ] Validation errors show helpful messages
- [ ] Mobile UI is responsive

---

## Sources & References

### GitHub Pull Requests
- **PR #48, #49** (MB901): Collapsed menus, multi-device, zone-based messaging, clear on response
- **PR #39** (Trilis29): Critical sound level implementation
- **PR #26** (HNKNTA): notification_link field
- **PR #15** (ChrisBaker97): Template syntax improvements

### GitHub Issues
- **Issue #43**: UndefinedError on timeout
- **Issue #44**: Camera snapshot timing delay
- **Issue #47**: iOS compatibility issues
- **Issue #50**: Off-LAN notification failures
- **Issue #41**: Android notification clearing

### Community Discussions
- [Main Community Thread](https://community.home-assistant.io/t/notifications-actionable-mobile-notifications-script-with-optional-timeout-feature-and-camera-snapshots-works-with-ios-android/551552)
- Forum feedback on script mode concurrency
- User requests for multi-device support

### Other Blueprints
- [Sensor Light Blueprint by Blackshome](https://gist.github.com/Blackshome/6edfec0ff6a25c5da0d07b88dc908238): Collapsed sections pattern

### Documentation
- [Home Assistant Companion Docs](https://companion.home-assistant.io/docs/notifications/notifications-basic/)
- HA Blueprint Best Practices
- YAML Syntax Guidelines

---

## Migration Guide (v2.0.2 → v2.1.0)

### Breaking Changes
**None planned** - All changes will be backward compatible

### New Features
Users will need to:
1. Update blueprint to v2.1.0
2. Optionally configure new sections (all have defaults)
3. Review improved field descriptions
4. Test timeout scenarios to ensure bug fixes work

### Deprecated Features
**None** - All existing features will continue to work

---

## Success Metrics

### Bug Fixes
- ✅ Zero timeout-related errors in logs
- ✅ Android notifications clear correctly 100% of time
- ✅ iOS compatibility restored for all iOS versions

### UX Improvements
- ✅ Setup time reduced by 30% (easier to find fields)
- ✅ User satisfaction score improved
- ✅ Reduced support questions about configuration

### Code Quality
- ✅ YAML validation passes
- ✅ No syntax errors or warnings
- ✅ Code coverage for error scenarios improved

---

**Document Version**: 1.0  
**Next Review**: After Phase 1 completion  
**Maintainer**: GitHub Copilot / Community
