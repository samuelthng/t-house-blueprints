# Multi-Device Notification Blueprint - REVISED IMPLEMENTATION PLAN

**Date**: 2026-02-11  
**Version**: Plan Revision 2  
**Status**: Ready for Implementation After Review

---

## TABLE OF CONTENTS
1. [Critical Findings from Current Blueprint Analysis](#critical-findings)
2. [Revised Architecture](#revised-architecture)
3. [Detailed Implementation Plan](#detailed-implementation-plan)
4. [Edge Cases and Solutions](#edge-cases-and-solutions)
5. [Testing Matrix](#testing-matrix)
6. [Implementation Iterations](#implementation-iterations)

---

## CRITICAL FINDINGS FROM CURRENT BLUEPRINT ANALYSIS

### Current Structure Understanding

**Inputs Organization:**
- Device selection currently in section (line 129-148)
- Message content in section (line 150-183)
- All sections have `collapsed: true` EXCEPT device_selection (collapsed: false)
- Device selector uses single device (no `multiple: true`)

**Variable Structure (lines 962-1197):**
- Variables are set up in sequential alias blocks
- Field overrides use `iif(field_x is defined, field_x, script_x)` pattern
- Platform detection: `'APPLE' in (device_attr(notify_device, "manufacturer")|upper)`
- Tag generation: Uses `this.entity_id ~ '-' ~ context.id` truncated to 64 bytes

**Notification Sending (lines 1252-1257):**
- Single service call: `service: "{{ notify_service }}"`
- Service constructed: `notify.mobile_app_{id}` where id is device name slugified
- All data passed in one `notification_data` payload

**Event Waiting (lines 1262-1310):**
- Uses `wait_for_trigger` with 3-4 trigger options
- Listens for `mobile_app_notification_action` with specific actions
- Also listens for `mobile_app_notification_cleared` with tag
- Has both timeout and non-timeout branches

**Response Handling (lines 1315-1354):**
- Parses response into `user_response` variable
- Uses `choose` to execute different actions based on response
- Returns `user_response` via `response_variable`

### Key Insights

1. **Platform Detection Method**: Uses device manufacturer attribute, not name pattern
2. **Tag System**: Auto-generated from entity_id and context, with iOS 64-byte truncation fix already applied
3. **Service Name Pattern**: Uses `slugify` filter on device name
4. **Event Structure**: Events contain `action` field and `tag` field
5. **Clear Mechanism**: iOS needs explicit clear notification command sent

### Potential Issues Identified

1. **Device Loop Challenge**: Need to loop through multiple devices for sending
2. **Event Filtering Challenge**: Events don't contain device_id in standard data
3. **Tag Uniqueness**: Need unique tag per notification group, shared across all devices
4. **Service Name Construction**: Need reliable way to get service name for each device
5. **Response Tracking**: Need to track which device responded
6. **Clear All Devices**: Need to send clear to multiple devices

---

## REVISED ARCHITECTURE

### Core Design Principles

1. **Backwards Compatibility**: Existing single-device configs should still work
2. **Progressive Disclosure**: Multi-device features hidden until relevant
3. **Simple Defaults**: Most common use case (first response) is default
4. **Clear Documentation**: Every edge case explained
5. **Fail-Safe**: Graceful degradation if something goes wrong

### Input Structure (Revised)

```yaml
# ============================================
# REQUIRED INPUTS (Outside sections, no defaults)
# ============================================

notify_devices:
  name: "📱 Devices to Notify"
  description: >-
    Select one or more devices to receive the notification.
    All selected devices will get the same notification content.
    
    Supports Jinja2 templates for dynamic device selection.
    
    📖 [Setup Guide](https://companion.home-assistant.io/docs/notifications/)
  selector:
    device:
      integration: mobile_app
      multiple: true

message:
  name: "💬 Message"
  description: >-
    Main notification text. Supports Jinja2 templates and HTML (🤖 Android).
    
    Examples:
     - "Motion detected at front door"
     - "{{ trigger.to_state.name }} is {{ trigger.to_state.state }}"
    
    📖 [Docs](https://companion.home-assistant.io/docs/notifications/notifications-basic)
  selector:
    text:
      multiline: true

# ============================================
# OPTIONAL SECTIONS (With defaults)
# ============================================

message_content:
  # Removed device, message (now top-level)
  # Keep: title, subtitle, sound
  
response_handling:
  name: "Response Handling"
  icon: mdi:reply-all
  collapsed: true
  description: >-
    Configure how responses are handled when multiple devices are notified.
  
  input:
    response_mode:
      name: "🎯 Response Mode"
      description: >-
        Choose how to handle responses from multiple devices:
        
        **First Response Only**: The first device to respond wins. All other 
        responses are ignored. Other devices can optionally be notified or 
        have their notifications cleared.
        
        **Use cases:**
         - Family security alert: "Someone answer the door"
         - Critical action needed: "Who will handle this?"
        
        **All Devices Can Respond**: Each device can respond independently. 
        Each response triggers its configured action.
        
        **Use cases:**
         - Survey: "Will you attend the meeting?"
         - Task assignment: Multiple people can accept
      default: "first_response"
      selector:
        select:
          options:
            - label: "First Response Only (others ignored)"
              value: "first_response"
            - label: "All Devices Can Respond"
              value: "all_responses"
    
    # CONDITIONAL: Only show if response_mode == 'first_response'
    clear_other_notifications:
      name: "🧹 Clear Other Notifications"
      description: >-
        After first response, automatically clear notifications on all 
        other devices. Reduces clutter and confusion.
        
        **Example:** Dad responds "I'll check" - Mom's phone notification 
        auto-dismisses.
      default: true
      selector:
        boolean:
    
    notify_other_devices:
      name: "📢 Notify Other Devices"
      description: >-
        Send a follow-up notification to devices that didn't respond,
        informing them who responded and what action was taken.
        
        **Example:** "John has acknowledged the security alert"
      default: false
      selector:
        boolean:
    
    # CONDITIONAL: Only show if notify_other_devices == true
    other_devices_message:
      name: "📝 Other Devices Message"
      description: >-
        Message to send to non-responding devices. Supports templates.
        
        **Available variables:**
         - `responding_device_name`: Name of device that responded
         - `response_action`: Which button was pressed
         - `response_timestamp`: When response was received
        
        **Example:** 
        "{{ responding_device_name }} has responded at {{ response_timestamp }}"
      default: "{{ responding_device_name }} has already responded"
      selector:
        text:
          multiline: true
    
    other_devices_actions:
      name: "⚙️ Other Devices Actions"
      description: >-
        Additional actions to perform after sending follow-up notification.
        Runs once, not per device.
      default: []
      selector:
        action:

timeout_configuration:
  name: "Timeout Configuration"
  icon: mdi:timer-off
  collapsed: true
  description: >-
    Configure how timeouts are handled across multiple devices.
  
  input:
    enable_timeout:
      # Keep existing, but update description for multi-device
      description: >-
        Enable timeout feature. With multiple devices, you can choose
        individual or global timeout behavior below.
    
    timeout:
      # Keep existing
    
    timeout_mode:
      name: "⏱️ Timeout Mode"
      description: >-
        Choose how timeouts work with multiple devices:
        
        **Individual Device Timeouts**: Each device tracks its own timeout
        independently. Useful when people check notifications at different
        times (e.g., one person at home, another traveling).
        
        **Single Global Timeout**: One timeout countdown for all devices 
        together. Simpler and clearer when devices should timeout together.
        
        **Examples:**
         - Individual: Security alert where each person has 5 minutes to respond
         - Global: "Dinner's ready in 10 minutes" - one timer for everyone
      default: "global"
      selector:
        select:
          options:
            - label: "Individual Device Timeouts"
              value: "individual"
            - label: "Single Global Timeout"
              value: "global"
    
    # CONDITIONAL: Only show if timeout_mode == 'individual'
    first_timeout_behavior:
      name: "⚡ First Timeout Behavior"
      description: >-
        What happens when the first device times out:
        
        **Trigger Timeout for All**: If any device's notification is cleared
        (often means "I dismissed this"), immediately timeout all devices.
        Useful when clearing means "we're done with this".
        
        **Let Devices Timeout Independently**: Each device waits for its
        full timeout period. Useful when each person should have full time.
        
        **Examples:**
         - Trigger All: "Acknowledge alarm" - if anyone clears it, done
         - Independent: "RSVP to event" - everyone gets full time to decide
      default: "independent"
      selector:
        select:
          options:
            - label: "Trigger Timeout for All Devices"
              value: "trigger_all"
            - label: "Let Devices Timeout Independently"
              value: "independent"
    
    run_timeout_actions:
      # Keep existing
    
    timeout_action:
      # Keep existing
    
    clear_on_timeout:
      # Keep existing, but note it clears ALL devices now
      description: >-
        Clear notifications on ALL devices when timeout occurs.
        
        Note: With multiple devices, this clears the notification
        on every notified device, not just ones that timed out.
    
    swipe_away_as_timeout:
      # Keep existing
```

### Variable Structure (Revised)

```yaml
sequence:
  # ==========================================
  # PHASE 1: Process Inputs & Fields
  # ==========================================
  - alias: "Process device input"
    variables:
      script_notify_devices: !input notify_devices
      notify_devices: "{{ iif(field_notify_devices is defined, field_notify_devices, script_notify_devices) }}"
      # Ensure it's always a list
      notify_devices_list: >-
        {% if notify_devices is string %}
          {{ [notify_devices] }}
        {% elif notify_devices is iterable %}
          {{ notify_devices | list }}
        {% else %}
          {{ [notify_devices] }}
        {% endif %}
      device_count: "{{ notify_devices_list | length }}"
      is_multi_device: "{{ device_count > 1 }}"
  
  # Message now required, no default
  - alias: "Process message"
    variables:
      script_message: !input message
      message: "{{ iif(field_message is defined, field_message, script_message) }}"
  
  # All other existing variables...
  # (title, subtitle, sound, attachments, etc.)
  
  # ==========================================
  # PHASE 2: Multi-Device Specific Variables
  # ==========================================
  - alias: "Response handling configuration"
    variables:
      response_mode: !input response_mode
      clear_other_notifications: !input clear_other_notifications
      notify_other_devices: !input notify_other_devices
      other_devices_message: !input other_devices_message
      other_devices_actions: !input other_devices_actions
  
  - alias: "Timeout configuration"
    variables:
      timeout_mode: !input timeout_mode
      first_timeout_behavior: !input first_timeout_behavior
  
  - alias: "Generate unique notification tag for this group"
    variables:
      # Generate tag that's shared across all devices in this notification
      custom_tag: !input tag
      notification_group_id: "{{ this.entity_id ~ '-' ~ context.id }}"
      tag: >-
        {{ 
          iif(
            custom_tag|length, 
            custom_tag, 
            notification_group_id
          ) | truncate(64, killwords=True, end='') 
        }}
  
  - alias: "Build device info list"
    variables:
      # Create list of device info objects
      devices_info: >-
        {% set ns = namespace(devices=[]) %}
        {% for device_id in notify_devices_list %}
          {% set device_name = device_attr(device_id, 'name') %}
          {% set device_slug = device_name | slugify %}
          {% set manufacturer = device_attr(device_id, 'manufacturer') | upper %}
          {% set is_apple = 'APPLE' in manufacturer %}
          {% set platform = 'iOS' if is_apple else 'Android' %}
          {% set service_name = 'notify.mobile_app_' ~ device_slug %}
          {% set ns.devices = ns.devices + [{
            'id': device_id,
            'name': device_name,
            'slug': device_slug,
            'platform': platform,
            'is_apple': is_apple,
            'service': service_name,
            'notified': false,
            'responded': false,
            'response_time': none,
            'response_action': none,
            'timed_out': false
          }] %}
        {% endfor %}
        {{ ns.devices }}
  
  # ==========================================
  # PHASE 3: Build Platform-Specific Payloads
  # ==========================================
  - alias: "Build notification payloads"
    variables:
      # Note: Can't use repeat in variables, so we'll use template
      # to pre-build payloads for each platform type
      ios_payload_data: >-
        {# iOS payload builder #}
        {% set payload = namespace(data={}) %}
        {% set push = namespace(d={}) %}
        
        {% set payload.data = dict(payload.data, **{ 'subtitle': subtitle }) %}
        {% set push.d = dict(push.d, **{ 'interruption-level': interruption_level }) %}
        
        {% if notification_link|length %}
          {% set payload.data = dict(payload.data, **{ 'url': notification_link }) %}
        {% endif %}
        
        {% if attachment_type == 'camera_entity' %}
          {% set payload.data = dict(payload.data, **{ 'entity_id': attachment_camera_entity }) %}
        {% endif %}
        
        {% if sound|length %}
          {% set push.d = dict(push.d, **{ 'sound': sound }) %}
        {% endif %}
        
        {% if badge is not none and badge != '' %}
          {% set payload.data = dict(payload.data, **{ 'badge': badge|int }) %}
        {% endif %}
        
        {% if thread_id|length %}
          {% set payload.data = dict(payload.data, **{ 'thread-id': thread_id }) %}
        {% endif %}
        
        {% if presentation_options|length %}
          {% set push.d = dict(push.d, **{ 'presentation-options': presentation_options }) %}
        {% endif %}
        
        {% if image_url|length %}
          {% set payload.data = dict(payload.data, **{ 'image': image_url }) %}
        {% endif %}
        
        {% if video_url|length %}
          {% set payload.data = dict(payload.data, **{ 'video': video_url }) %}
        {% endif %}
        
        {% set payload.data = dict(payload.data, **{ 'push': push.d }) %}
        
        {# Common data #}
        {% set payload.data = dict(payload.data, **{ 'actions': options }) %}
        {% set payload.data = dict(payload.data, **{ 'tag': tag }) %}
        {% if group|length %}
          {% set payload.data = dict(payload.data, **{ 'group': group }) %}
        {% endif %}
        
        {{ payload.data }}
      
      android_payload_data: >-
        {# Android payload builder #}
        {% set payload = namespace(data={}) %}
        
        {% set payload.data = dict(payload.data, **{ 'subject': subtitle }) %}
        {% set payload.data = dict(payload.data, **{ 'visibility': visibility }) %}
        {% set payload.data = dict(payload.data, **{ 'importance': importance }) %}
        
        {% if android_high_priority %}
          {% set payload.data = dict(payload.data, **{ 'priority': 'high', 'ttl': 0 }) %}
        {% endif %}
        
        {% if notification_link|length %}
          {% set payload.data = dict(payload.data, **{ 'clickAction': notification_link }) %}
        {% endif %}
        
        {% if attachment_type == 'camera_entity' and (media_url|length) %}
          {% set payload.data = dict(payload.data, **{ 'image': media_url }) %}
        {% endif %}
        
        {% if notification_icon|length %}
          {% set payload.data = dict(payload.data, **{ 'notification_icon': notification_icon }) %}
        {% endif %}
        
        {% if enable_icon_color %}
          {% set payload.data = dict(payload.data, **{ 'color': icon_color_hex }) %}
        {% endif %}
        
        {% if enable_timeout and clear_on_timeout %}
          {% set payload.data = dict(payload.data, **{ 'timeout': timeout_seconds }) %}
        {% endif %}
        
        {% if channel|length %}
          {% set payload.data = dict(payload.data, **{ 'channel': channel }) %}
        {% endif %}
        
        {% if persist %}
          {% set payload.data = dict(payload.data, **{ 'persistent': persist }) %}
        {% endif %}
        
        {% if car_ui %}
          {% set payload.data = dict(payload.data, **{ 'car_ui': car_ui }) %}
        {% endif %}
        
        {% if sound|length %}
          {% set payload.data = dict(payload.data, **{ 'sound': sound }) %}
        {% endif %}
        
        {% if sticky %}
          {% set payload.data = dict(payload.data, **{ 'sticky': sticky }) %}
        {% endif %}
        
        {% if vibration_pattern|length %}
          {% set payload.data = dict(payload.data, **{ 'vibration_pattern': vibration_pattern }) %}
        {% endif %}
        
        {% if led_color|length %}
          {% set payload.data = dict(payload.data, **{ 'led_color': led_color }) %}
        {% endif %}
        
        {% if alert_once %}
          {% set payload.data = dict(payload.data, **{ 'alert_once': alert_once }) %}
        {% endif %}
        
        {% if image_url|length %}
          {% set payload.data = dict(payload.data, **{ 'image': image_url }) %}
        {% endif %}
        
        {% if video_url|length %}
          {% set payload.data = dict(payload.data, **{ 'video': video_url }) %}
        {% endif %}
        
        {# Common data #}
        {% set payload.data = dict(payload.data, **{ 'actions': options }) %}
        {% set payload.data = dict(payload.data, **{ 'tag': tag }) %}
        {% if group|length %}
          {% set payload.data = dict(payload.data, **{ 'group': group }) %}
        {% endif %}
        
        {{ payload.data }}
  
  # ==========================================
  # PHASE 4: Send Notifications to All Devices
  # ==========================================
  - alias: "Send notifications to all selected devices"
    repeat:
      for_each: "{{ devices_info }}"
      sequence:
        - alias: "Send to {{ repeat.item.name }}"
          service: "{{ repeat.item.service }}"
          data:
            title: "{{ title }}"
            message: "{{ message }}"
            data: "{{ ios_payload_data if repeat.item.is_apple else android_payload_data }}"
  
  # ==========================================
  # PHASE 5: Wait for Response(s)
  # ==========================================
  - alias: "Determine response handling strategy"
    choose:
      # -------------------------------------
      # CASE 1: No response expected
      # -------------------------------------
      - alias: "No need for response"
        conditions: "{{ expect_response == false }}"
        sequence: []
      
      # -------------------------------------
      # CASE 2: First response only (with timeout)
      # -------------------------------------
      - alias: "First response mode with timeout"
        conditions:
          - "{{ response_mode == 'first_response' }}"
          - "{{ enable_timeout }}"
        sequence:
          - alias: "Wait for first response with timeout"
            wait_for_trigger:
              - platform: event
                event_type: mobile_app_notification_action
                event_data:
                  action: "{{ first_option }}"
                  tag: "{{ tag }}"
              - platform: event
                event_type: mobile_app_notification_action
                event_data:
                  action: "{{ second_option }}"
                  tag: "{{ tag }}"
              - platform: event
                event_type: mobile_app_notification_action
                event_data:
                  action: "{{ third_option }}"
                  tag: "{{ tag }}"
              - platform: event
                event_type: mobile_app_notification_cleared
                event_data:
                  tag: "{{ tag }}"
            timeout: "{{ timeout }}"
            continue_on_timeout: true
          
          # Store first responder info
          - alias: "Capture first responder"
            variables:
              first_responder: >-
                {% if wait.trigger %}
                  {{ wait.trigger.event.data }}
                {% else %}
                  none
                {% endif %}
              responding_device_name: >-
                {% if wait.trigger and wait.trigger.event.data.device_id %}
                  {{ device_attr(wait.trigger.event.data.device_id, 'name') }}
                {% else %}
                  "Unknown Device"
                {% endif %}
              response_action: >-
                {% if wait.trigger %}
                  {{ wait.trigger.event.data.action }}
                {% else %}
                  "timeout"
                {% endif %}
              response_timestamp: "{{ now().strftime('%I:%M %p') }}"
          
          # Clear other devices if configured
          - alias: "Clear notifications on other devices"
            if: "{{ clear_other_notifications and first_responder != none }}"
            then:
              - repeat:
                  for_each: "{{ devices_info }}"
                  sequence:
                    # Only clear if not the responding device
                    - if: >-
                        {{ 
                          first_responder.device_id is defined and
                          repeat.item.id != first_responder.device_id 
                        }}
                      then:
                        - service: "{{ repeat.item.service }}"
                          data:
                            message: "clear_notification"
                            data:
                              tag: "{{ tag }}"
          
          # Notify other devices if configured
          - alias: "Notify other devices about response"
            if: "{{ notify_other_devices and first_responder != none }}"
            then:
              - repeat:
                  for_each: "{{ devices_info }}"
                  sequence:
                    - if: >-
                        {{ 
                          first_responder.device_id is defined and
                          repeat.item.id != first_responder.device_id 
                        }}
                      then:
                        - service: "{{ repeat.item.service }}"
                          data:
                            title: "{{ title }} - Resolved"
                            message: "{{ other_devices_message }}"
                            data: "{{ {'tag': tag ~ '_resolved'} }}"
              
              # Run additional actions once
              - choose:
                  - conditions: "{{ other_devices_actions | length > 0 }}"
                    sequence: !input other_devices_actions
      
      # -------------------------------------
      # CASE 3: All responses mode (with timeout)
      # -------------------------------------
      - alias: "All responses mode with timeout"
        conditions:
          - "{{ response_mode == 'all_responses' }}"
          - "{{ enable_timeout }}"
        sequence:
          # Complex: Need to track responses from all devices
          # This requires a different approach...
          # For now, use simpler wait_for_trigger
          - alias: "Wait for responses with timeout"
            wait_for_trigger:
              - platform: event
                event_type: mobile_app_notification_action
                event_data:
                  tag: "{{ tag }}"
            timeout: "{{ timeout }}"
            continue_on_timeout: true
  
  # ==========================================
  # PHASE 6: Parse and Execute Response
  # ==========================================
  - alias: "Parse response"
    variables:
      user_response: >-
        {% set response = namespace(data={}) %}
        {% if not expect_response %}
          {% set response.data = dict(response.data, **{ 'result': "no_response" }) %}
        {% elif run_timeout_actions and wait.trigger == none %}
          {% set response.data = dict(response.data, **{ 'result': "timeout" }) %}
        {% elif run_timeout_actions and swipe_away_as_timeout and wait.trigger.event.event_type == 'mobile_app_notification_cleared' %}
          {% set response.data = dict(response.data, **{ 'result': "notification_cleared" }) %}
        {% elif wait.trigger.event.data.action == option_one['action'] %}
          {% set response.data = dict(response.data, **{ 'result': "option_one" }) %}
        {% elif wait.trigger.event.data.action == option_two['action'] %}
          {% set response.data = dict(response.data, **{ 'result': "option_two" }) %}
        {% elif wait.trigger.event.data.action == option_three['action'] %}
          {% set response.data = dict(response.data, **{ 'result': "option_three" }) %}
        {% endif %}
        
        {# Add responder info #}
        {% if wait.trigger and wait.trigger.event.data.device_id %}
          {% set response.data = dict(response.data, **{ 
            'device_id': wait.trigger.event.data.device_id,
            'device_name': device_attr(wait.trigger.event.data.device_id, 'name')
          }) %}
        {% endif %}
        
        {{ response.data }}
  
  - alias: "Execute response actions"
    default: []
    choose:
      - alias: "Timeout or Cleared"
        conditions: "{{ user_response.result in ['timeout', 'notification_cleared'] }}"
        sequence: !input timeout_action
      - alias: "Option One"
        conditions: "{{ user_response.result == 'option_one' }}"
        sequence: !input confirm_action
      - alias: "Option Two"
        conditions: "{{ user_response.result == 'option_two' }}"
        sequence: !input dismiss_action
      - alias: "Option Three"
        conditions: "{{ user_response.result == 'option_three' }}"
        sequence: !input option_three_action
  
  # ==========================================
  # PHASE 7: Final Cleanup
  # ==========================================
  - alias: "Clear notifications on timeout if configured"
    if: "{{ enable_timeout and clear_on_timeout and user_response.result in ['timeout', 'notification_cleared'] }}"
    then:
      - repeat:
          for_each: "{{ devices_info }}"
          sequence:
            - service: "{{ repeat.item.service }}"
              data:
                message: "clear_notification"
                data:
                  tag: "{{ tag }}"
  
  - stop: "Multi-device notification script completed"
    response_variable: "user_response"
```

---

## EDGE CASES AND SOLUTIONS

### Edge Case 1: Event Doesn't Contain device_id

**Problem**: Some events might not have device_id in event data.

**Solution**: 
- Use tag matching instead of device_id matching in events
- Track responses by correlation with tag and timestamp
- Add defensive checks: `if wait.trigger.event.data.device_id is defined`

### Edge Case 2: Device Service Name Invalid

**Problem**: Device name might contain special characters that break service name.

**Solution**:
- Use `slugify` filter (already in current code)
- Add validation in template
- Provide clear error message if service call fails

### Edge Case 3: Mixed Platform Devices

**Problem**: Some devices are iOS, some Android, need different payloads.

**Solution**:
- Pre-build both iOS and Android payloads
- Select correct payload in repeat loop based on `repeat.item.is_apple`
- This is already handled in revised architecture

### Edge Case 4: Simultaneous Responses

**Problem**: Two devices respond at exact same time.

**Solution**:
- `wait_for_trigger` will catch first one received by HA
- Second one is ignored (as intended for first_response mode)
- For all_responses mode, would need different handling (future enhancement)

### Edge Case 5: Device List is Empty

**Problem**: User doesn't select any devices.

**Solution**:
- Add validation: `{% if device_count == 0 %}` stop with error
- Or require at least one device in selector (if HA supports that)
- Show clear error message

### Edge Case 6: Notification Clear Event From Wrong Tag

**Problem**: User has multiple notification scripts running, events get mixed up.

**Solution**:
- Always include tag in event data filters
- Generate unique tag per notification group
- Tag already truncated to 64 bytes for iOS compatibility

### Edge Case 7: Timeout Cascade Decision

**Problem**: In individual mode with trigger_all, need to detect which device cleared first.

**Solution**:
- `wait_for_trigger` captures the first clear event
- Extract device_id from event data
- Immediately send clear to all other devices
- Mark all as timed out

### Edge Case 8: Template Variables in other_devices_message

**Problem**: Need to make responding_device_name available in template.

**Solution**:
- Set as variable before using in message
- Use same approach as current blueprint for variable passing
- Template is evaluated at execution time, variables are available

### Edge Case 9: iOS Clear After Timeout

**Problem**: iOS devices need explicit clear command.

**Solution**:
- Already handled in current code (lines 1359-1370)
- Need to loop through all iOS devices in list
- Send clear_notification message to each

### Edge Case 10: Single Device Selected (Backwards Compatibility)

**Problem**: User selects only one device, but we treat it as list.

**Solution**:
- List handling works with single item
- All loops iterate once
- No performance impact
- Response handling identical to current blueprint

---

## TESTING MATRIX

| # | Devices | Response Mode | Timeout Mode | First Timeout | Expected Result | Test Status |
|---|---------|--------------|--------------|---------------|----------------|-------------|
| 1 | 1 | first_response | global | N/A | Works like current blueprint | ⏳ Pending |
| 2 | 2 (iOS+iOS) | first_response | global | N/A | First response wins, other cleared | ⏳ Pending |
| 3 | 2 (Android+Android) | first_response | global | N/A | First response wins, other cleared | ⏳ Pending |
| 4 | 2 (iOS+Android) | first_response | global | N/A | First response wins, other cleared | ⏳ Pending |
| 5 | 3 mixed | first_response | global | N/A | First response wins, 2 others cleared | ⏳ Pending |
| 6 | 2 | first_response | individual | independent | Each device has own timeout | ⏳ Pending |
| 7 | 2 | first_response | individual | trigger_all | First clear triggers all | ⏳ Pending |
| 8 | 2 | first_response + notify | global | N/A | First responds, others get message | ⏳ Pending |
| 9 | 2 | first_response + actions | global | N/A | First responds, actions run | ⏳ Pending |
| 10 | 2 | all_responses | global | N/A | Both can respond | ⏳ Pending |
| 11 | 2 | first_response | global + no clear | N/A | First responds, others stay | ⏳ Pending |
| 12 | 2, timeout | first_response | global | N/A | Timeout clears all | ⏳ Pending |
| 13 | 0 (empty) | any | any | any | Error or graceful fail | ⏳ Pending |
| 14 | Invalid device ID | any | any | any | Service call fails gracefully | ⏳ Pending |
| 15 | 2, no options | first_response | global | N/A | Sends, doesn't wait | ⏳ Pending |

---

## IMPLEMENTATION ITERATIONS

### Iteration 1: Foundation (Input Reorganization)
**Goal**: Move device and message outside sections, make required

**Tasks**:
1. Remove device_selection section
2. Remove message from message_content section  
3. Add notify_devices as top-level input (multiple: true)
4. Add message as top-level input (no default)
5. Update field definitions
6. Test: Blueprint loads, sections work

**Validation**:
- [ ] Blueprint loads without errors
- [ ] Device selector shows multiple option
- [ ] Message is required field
- [ ] All other sections still work

**Files Changed**: `notifications.yaml`  
**Lines Changed**: ~50-100 lines  
**Risk Level**: LOW (mostly reorganization)

---

### Iteration 2: Multi-Device Variables
**Goal**: Build device info list and handle multiple devices

**Tasks**:
1. Add response_mode and timeout_mode inputs
2. Create devices_info variable with loop
3. Add platform detection for each device
4. Build service names for each device
5. Test: Device list builds correctly

**Validation**:
- [ ] devices_info list populates correctly
- [ ] Platform detection works (iOS vs Android)
- [ ] Service names are correct
- [ ] Single device still works

**Files Changed**: `notifications.yaml`  
**Lines Changed**: ~100-150 lines  
**Risk Level**: MEDIUM (new variable structure)

---

### Iteration 3: Multi-Device Sending
**Goal**: Send notifications to all devices in loop

**Tasks**:
1. Replace single service call with repeat loop
2. Send to each device with correct payload
3. Add platform-specific payload selection
4. Test: All devices receive notification

**Validation**:
- [ ] Single device receives notification
- [ ] Multiple devices all receive notification
- [ ] iOS payload correct
- [ ] Android payload correct
- [ ] Mixed platforms work

**Files Changed**: `notifications.yaml`  
**Lines Changed**: ~50-100 lines  
**Risk Level**: MEDIUM (core functionality change)

---

### Iteration 4: Response Handling (First Response)
**Goal**: Implement first response logic with clear others

**Tasks**:
1. Add wait_for_trigger with tag matching
2. Capture first responder info
3. Implement clear other notifications
4. Test: First response captured, others cleared

**Validation**:
- [ ] First device response captured
- [ ] Other devices notifications cleared
- [ ] Response actions execute correctly
- [ ] Works with timeout
- [ ] Works without timeout

**Files Changed**: `notifications.yaml`  
**Lines Changed**: ~100-150 lines  
**Risk Level**: HIGH (complex logic)

---

### Iteration 5: Notify Other Devices Feature
**Goal**: Send follow-up notifications to non-responders

**Tasks**:
1. Add conditional for notify_other_devices
2. Build loop to send to non-responders
3. Template message with variables
4. Run additional actions
5. Test: Other devices get follow-up

**Validation**:
- [ ] Other devices receive follow-up message
- [ ] Template variables resolve correctly
- [ ] Actions run once (not per device)
- [ ] Works with different message templates

**Files Changed**: `notifications.yaml`  
**Lines Changed**: ~50-100 lines  
**Risk Level**: MEDIUM (new feature)

---

### Iteration 6: Advanced Timeout Handling
**Goal**: Implement individual timeout and cascade logic

**Tasks**:
1. Add timeout_mode branching
2. Implement individual timeout tracking (future)
3. Implement first timeout cascade (future)
4. Test: Complex timeout scenarios

**Note**: This is complex and may be deferred to v2.1 if time-constrained.

**Validation**:
- [ ] Global timeout works with multiple devices
- [ ] Individual timeout TBD
- [ ] Cascade trigger TBD

**Files Changed**: `notifications.yaml`  
**Lines Changed**: ~100-200 lines  
**Risk Level**: VERY HIGH (most complex logic)

---

### Iteration 7: Final Testing and Polish
**Goal**: Test all combinations, fix bugs, polish UX

**Tasks**:
1. Run full test matrix
2. Fix any identified bugs
3. Improve error messages
4. Update documentation
5. Add examples

**Validation**:
- [ ] All test matrix cases pass
- [ ] No errors in logs
- [ ] User-friendly error messages
- [ ] Documentation complete

**Files Changed**: `notifications.yaml`, README  
**Lines Changed**: Variable  
**Risk Level**: LOW (fixes and polish)

---

## IMPLEMENTATION STRATEGY

### Phase-Based Rollout

**Phase 1: Core Multi-Device (v2.3.0)**
- Iterations 1-5
- Basic multi-device send and receive
- First response mode only
- Global timeout only
- Estimated: 12-16 hours

**Phase 2: Advanced Features (v2.4.0)**
- Iteration 6
- Individual timeouts
- Cascade triggers
- All responses mode
- Estimated: 8-12 hours

### Incremental Testing Approach

After each iteration:
1. Syntax validation
2. Load in HA and verify no errors
3. Manual testing of changed functionality
4. Document any issues found
5. Fix before proceeding to next iteration

### Rollback Plan

Each iteration creates a backup:
- `notifications_iterationN_backup.yaml`
- Can rollback to previous iteration if issues found
- Git commits allow precise rollback points

---

## EXPECTED CHALLENGES

### Challenge 1: Event Data Structure
**Issue**: Event data might not contain expected fields  
**Mitigation**: Defensive templates with `is defined` checks  
**Testing**: Create test events with missing fields

### Challenge 2: Template Complexity
**Issue**: Nested templates can be hard to debug  
**Mitigation**: Break into smaller variable blocks  
**Testing**: Test each template block independently

### Challenge 3: Performance with Many Devices
**Issue**: Sending to 10+ devices might be slow  
**Mitigation**: Currently using repeat which is sequential  
**Future**: Consider parallel service calls if HA supports

### Challenge 4: User Configuration Errors
**Issue**: Users might configure contradictory settings  
**Mitigation**: Clear documentation and validation  
**Example**: "Clear other notifications" without "First response"

---

## SUCCESS CRITERIA

✅ **Minimum Viable Product (MVP)**:
1. Can select multiple devices
2. All selected devices receive notification
3. First response mode works
4. Other notifications clear after first response
5. Backwards compatible with single device

✅ **Full Feature Set**:
6. Notify other devices after first response
7. Template variables work in messages
8. Global timeout works with multiple devices
9. All test matrix cases pass
10. Documentation complete

✅ **Quality Metrics**:
- Zero critical bugs
- User-friendly error messages
- Clear documentation
- Performance acceptable (<5s for 5 devices)

---

## TIMELINE ESTIMATE

**Conservative Estimate**: 20-24 hours total
- Iteration 1: 2 hours
- Iteration 2: 3 hours
- Iteration 3: 3 hours
- Iteration 4: 5 hours
- Iteration 5: 3 hours
- Iteration 6: 8 hours (or defer)
- Iteration 7: 4 hours

**Optimistic Estimate**: 12-16 hours total
- Skip iteration 6 (defer advanced timeout)
- Focus on core multi-device + first response

---

## FINAL RECOMMENDATION

**PROCEED WITH PHASED APPROACH**

1. Start with Iterations 1-5 (Core Multi-Device)
2. Test thoroughly after each iteration
3. Defer Iteration 6 (Advanced Timeout) to future version
4. This delivers 80% of value with 60% of effort
5. Reduces risk of complex bugs
6. Faster time to working multi-device support

**READY FOR IMPLEMENTATION**: Yes, with this revised plan

---

**END OF REVISED PLAN**
