# Multi-Device Notification Blueprint - Implementation Plan

## Executive Summary

This plan outlines the implementation of multi-device support for the notification blueprint, allowing users to send actionable notifications to multiple devices with sophisticated response handling, timeout management, and notification clearing capabilities.

---

## Research Findings

### Key Insights from Community Research

1. **Device Selection**: Use `device` selector with `multiple: true` and `integration: mobile_app` filter
2. **Service Calls**: Must loop through devices and construct service names dynamically (e.g., `notify.mobile_app_<device_name>`)
3. **Event Handling**: Use `wait_for_trigger` with event type `mobile_app_notification_action` to capture responses
4. **Notification Clearing**: Use same `tag` across all devices to enable synchronized clearing
5. **First Response Pattern**: `wait_for_trigger` naturally stops on first event received

### Reference Blueprints
- RuedigerMueller's Confirmable Multi-Device Notification Blueprint (Gist)
- Unified Notification Blueprint with Optional Actions (Community)
- Various multi-phone actionable notification examples

---

## Requirements Breakdown

### 1. Mandatory Fields Outside Sections (No Defaults)
- **Devices to Notify**: Multiple device selector
- **Message**: Message content (required field)

### 2. Multi-Device Support
- Allow selection of multiple devices
- Build correct iOS and Android payloads per device
- Send notifications to all selected devices
- Track which devices were notified

### 3. Response Handling Modes

#### Mode 1: Single Response (First Response Wins)
- Listen for first response from any device
- Ignore subsequent responses from other devices
- Options after first response:
  - Clear notifications on all other devices
  - Run actions on behalf of other devices
  - Send follow-up notifications to other devices

#### Mode 2: Multi Response (All Devices Can Respond)
- Continue listening for responses from all devices
- Each device's response triggers its own actions
- Use notification tag to track related notifications

### 4. Timeout Handling

#### Individual Device Timeout
- Each device tracks its own timeout independently
- First device to timeout can:
  - Trigger timeout for all devices
  - Allow other devices to continue independently

#### Global Timeout
- Single timeout applies to all devices
- When global timeout triggers, all devices are considered timed out

---

## Architecture Design

### Input Structure

```yaml
# OUTSIDE SECTIONS (Required, no defaults)
notify_devices:
  name: Devices to Notify
  selector:
    device:
      integration: mobile_app
      multiple: true

message:
  name: Message
  selector:
    text:
      multiline: true

# NEW SECTION: Response Handling
response_mode:
  - single_response (first response wins)
  - multi_response (all can respond)

# For single_response mode:
after_first_response:
  - clear_other_notifications (boolean)
  - run_timeout_actions_for_others (boolean)
  - notify_other_devices (boolean)
  - other_devices_message (text, conditional)
  - other_devices_actions (action selector, conditional)

# NEW SECTION: Timeout Behavior
timeout_mode:
  - individual_device (each device independent)
  - global_timeout (one timeout for all)

# For individual_device mode:
first_timeout_behavior:
  - trigger_all (first timeout triggers for all)
  - independent (devices timeout independently)
```

### Workflow Logic

```
1. PREPARE PHASE
   - Get list of selected devices
   - Build device-specific notification data
   - Determine device platform (iOS/Android)
   - Generate unique tag for this notification group

2. SEND PHASE
   - Loop through each device
   - Build platform-specific payload
   - Send notification with shared tag
   - Store device info in variables

3. LISTEN PHASE
   Mode: Single Response
     - Wait for first event with matching tag
     - Store responding device info
     - Execute action based on response
     - If configured:
       - Clear notifications on other devices
       - Run timeout actions for other devices
       - Send follow-up to other devices
   
   Mode: Multi Response
     - Wait for events with matching tag
     - Track which devices have responded
     - Execute actions per response
     - Continue until timeout or all responded

4. TIMEOUT PHASE
   Individual Mode:
     - Each device can timeout independently
     - First timeout can trigger cascade if configured
   
   Global Mode:
     - Single timeout for entire notification group
     - All devices treated as timed out
```

### Data Structure

```yaml
variables:
  # Generate unique tag for this notification group
  notification_tag: "{{ 'notify_' ~ now().timestamp() | int }}"
  
  # Store device information
  notified_devices: >
    {% set devices = notify_devices %}
    {% set ns = namespace(list=[]) %}
    {% for device in devices %}
      {% set device_name = device_attr(device, 'name') | lower | replace(' ', '_') %}
      {% set platform = 'ios' if 'iphone' in device_name or 'ipad' in device_name else 'android' %}
      {% set ns.list = ns.list + [{
        'id': device,
        'name': device_name,
        'platform': platform,
        'notified': true,
        'responded': false
      }] %}
    {% endfor %}
    {{ ns.list }}
  
  # Track responses
  responded_devices: []
  response_count: 0
```

---

## New Sections and Inputs

### Section 1: Response Handling Configuration
**Name**: "Response Handling"  
**Icon**: mdi:reply-all  
**Description**: Configure how responses from multiple devices are handled

**Inputs**:

1. `response_mode`
   - **Type**: select
   - **Options**: 
     - `single_response`: "First Response Only (others ignored)"
     - `multi_response`: "All Responses (each device can respond)"
   - **Default**: `single_response`
   - **Description**: 
     ```
     Choose how to handle responses when multiple devices are notified:
     
     - First Response Only: The first device to respond triggers the action. All other responses are ignored.
       Useful for: Family notifications where only one person needs to respond.
     
     - All Responses: Each device can respond independently and trigger its own action.
       Useful for: Survey-style notifications where each person's response matters.
     ```

2. `clear_other_notifications` (conditional: response_mode == 'single_response')
   - **Type**: boolean
   - **Default**: true
   - **Description**: "Automatically clear notifications on all other devices after first response is received"

3. `run_actions_for_others` (conditional: response_mode == 'single_response')
   - **Type**: boolean
   - **Default**: false
   - **Description**: "Run timeout actions on behalf of devices that didn't respond"

4. `notify_other_devices` (conditional: response_mode == 'single_response')
   - **Type**: boolean
   - **Default**: false
   - **Description**: "Send a follow-up notification to devices that didn't respond"

5. `other_devices_message` (conditional: notify_other_devices == true)
   - **Type**: text (multiline)
   - **Default**: "{{ responding_device_name }} has already responded"
   - **Description**: "Message to send to other devices. Available variables: responding_device_name, response_action"

6. `other_devices_actions` (conditional: notify_other_devices == true)
   - **Type**: action
   - **Description**: "Additional actions to perform after notifying other devices"

### Section 2: Timeout Configuration
**Name**: "Timeout Configuration"  
**Icon**: mdi:timer-off  
**Description**: Configure how timeouts are handled across multiple devices

**Inputs**:

1. `timeout_mode`
   - **Type**: select
   - **Options**:
     - `individual`: "Individual Device Timeouts"
     - `global`: "Single Global Timeout"
   - **Default**: `individual`
   - **Description**:
     ```
     Choose timeout behavior for multiple devices:
     
     - Individual Device Timeouts: Each device tracks its own timeout. Useful when devices 
       might be checked at different times (e.g., one person at home, one traveling).
     
     - Single Global Timeout: One timeout for all devices together. Simpler and clearer 
       when all devices should timeout together.
     ```

2. `first_timeout_behavior` (conditional: timeout_mode == 'individual')
   - **Type**: select
   - **Options**:
     - `trigger_all`: "Trigger Timeout for All Devices"
     - `independent`: "Let Devices Timeout Independently"
   - **Default**: `independent`
   - **Description**:
     ```
     What happens when the first device times out:
     
     - Trigger All: If any device clears the notification (triggering timeout), all devices 
       timeout immediately. Useful when clearing means "done" for everyone.
     
     - Independent: Each device waits for its full timeout period independently. Useful when 
       each person should have full time to respond.
     ```

---

## Implementation Phases

### Phase 1: Input Reorganization (Foundation)
- [ ] Move `notify_device` outside sections (change to `notify_devices` with multiple)
- [ ] Move `message` outside sections
- [ ] Remove defaults from these fields
- [ ] Update field definitions accordingly

### Phase 2: Multi-Device Infrastructure
- [ ] Update device selector to `multiple: true`
- [ ] Create device info variable structure
- [ ] Implement device loop for sending notifications
- [ ] Add platform detection logic
- [ ] Implement dynamic service name construction

### Phase 3: Response Handling Section
- [ ] Create new "Response Handling" section
- [ ] Add response_mode selector
- [ ] Add conditional inputs for single_response mode
- [ ] Implement first-response-only logic
- [ ] Implement clear-other-notifications feature
- [ ] Implement notify-other-devices feature

### Phase 4: Timeout Configuration Section
- [ ] Create new "Timeout Configuration" section
- [ ] Add timeout_mode selector
- [ ] Add first_timeout_behavior selector (conditional)
- [ ] Implement individual timeout tracking
- [ ] Implement global timeout logic
- [ ] Implement cascade timeout trigger

### Phase 5: Integration and Testing
- [ ] Update action sequences for multi-device
- [ ] Update event listeners for response tracking
- [ ] Implement response counter
- [ ] Add device response tracking
- [ ] Test all permutations of settings
- [ ] Update changelog and documentation

---

## Technical Challenges and Solutions

### Challenge 1: Dynamic Service Names
**Problem**: Service names are device-specific (e.g., `notify.mobile_app_pixel_5`)

**Solution**: Use template to construct service name:
```yaml
service: "notify.mobile_app_{{ device_attr(repeat.item, 'name') | lower | replace(' ', '_') }}"
```

### Challenge 2: Platform Detection
**Problem**: Need to build different payloads for iOS vs Android

**Solution**: Detect platform from device name or use integration info:
```yaml
{% set platform = 'ios' if 'iphone' in device_name or 'ipad' in device_name else 'android' %}
```

### Challenge 3: Tracking Multiple Responses
**Problem**: Need to know which devices have responded

**Solution**: Maintain a list variable that gets updated with each response:
```yaml
{% set responded_devices = responded_devices + [wait.trigger.event.data.device_id] %}
```

### Challenge 4: Clearing Notifications on Specific Devices
**Problem**: Can't selectively clear on some devices but not others

**Solution**: Send clear command to each device individually in a loop:
```yaml
- repeat:
    for_each: "{{ other_devices }}"
    sequence:
      - service: "notify.mobile_app_{{ repeat.item.name }}"
        data:
          message: "clear_notification"
          data:
            tag: "{{ notification_tag }}"
```

### Challenge 5: First Timeout Detection
**Problem**: Determining which device timed out first

**Solution**: Use wait_for_trigger with multiple triggers, one per device:
```yaml
wait_for_trigger:
  - platform: event
    event_type: mobile_app_notification_cleared
    event_data:
      tag: "{{ notification_tag }}"
timeout: "{{ timeout_duration }}"
```

---

## User Experience Considerations

### Simplified Defaults
- Default to "First Response Only" mode (most common use case)
- Default to clearing other notifications (reduces clutter)
- Default to individual timeouts with independent behavior (most flexible)

### Clear Documentation
- Each input has examples showing real-world scenarios
- Platform differences clearly marked (🍎/🤖)
- Visual separators between related groups of settings

### Progressive Disclosure
- Basic options visible by default
- Advanced options only shown when relevant mode is selected
- Collapsible sections to reduce overwhelm

### Practical Examples
```yaml
# Example 1: Family Security Alert (First Response Only)
# - Send to all family members' phones
# - First person to acknowledge dismisses for everyone
# - Others get "John acknowledged the alert" notification

# Example 2: Household Chore Acceptance (All Responses)
# - Send to all household members
# - Each person can accept or decline
# - Track who accepted and who declined

# Example 3: Critical Alert with Escalation (Individual Timeouts)
# - Send to on-call staff
# - If first person clears (asleep?), trigger timeout for all
# - Escalate to next level immediately
```

---

## Backwards Compatibility

### Breaking Changes
- `notify_device` (singular) → `notify_devices` (plural, multiple)
- Field moved outside section
- No default value (now required)

### Migration Path
Users will need to:
1. Re-select their device(s) in the new input
2. Message field stays the same (just moved)
3. All other settings remain compatible

### Version Bump
- Current: 2026.2.0
- New: 2026.3.0 (major feature addition)

---

## Testing Strategy

### Test Matrix

| Devices | Response Mode | Timeout Mode | First Timeout | Expected Behavior |
|---------|--------------|--------------|---------------|-------------------|
| 1 | Single | Individual | Independent | Works like current version |
| 2 | Single | Individual | Independent | First response wins, others ignored |
| 2 | Single | Individual | Trigger All | First response or timeout triggers all |
| 2 | Single | Global | N/A | First response or global timeout |
| 3 | Multi | Individual | Independent | All can respond independently |
| 3 | Multi | Global | N/A | All can respond until global timeout |

### Edge Cases to Test
1. All devices respond simultaneously
2. No devices respond (global timeout)
3. Some devices respond, some timeout
4. First device times out immediately
5. Response received after timeout started but before completed
6. Device responds multiple times (should ignore duplicates)
7. Mix of iOS and Android devices
8. Invalid device ID in selection

---

## Documentation Updates

### Changelog Entry
```markdown
### Version 2026.3.0 - Multi-Device Support - *[Date]*

**Major Features**:
- ✨ NEW: Multi-device notification support
- ✨ NEW: Response handling modes (first-only or all-devices)
- ✨ NEW: Sophisticated timeout management for multiple devices
- ✨ NEW: Automatic notification clearing across devices
- 🔄 CHANGED: Device selection moved outside sections (required field)
- 🔄 CHANGED: Message moved outside sections (required field)

**Breaking Changes**:
- Device selector now supports multiple devices
- Device and Message fields are now required (no defaults)
- Users must re-configure these fields when updating

**Features**:
- Send to multiple devices simultaneously
- Choose "first response wins" or "all can respond" modes
- Clear notifications on other devices after first response
- Notify other devices about who responded
- Individual or global timeout modes
- Cascade timeout trigger options
```

### FAQ Additions
```markdown
**Q: Can I send to multiple devices?**
A: Yes! Select multiple devices in the "Devices to Notify" field.

**Q: What happens when I send to multiple devices?**
A: You can choose:
- First Response Only: First device to respond triggers the action
- All Responses: Each device can respond and trigger its own action

**Q: Can I clear notifications on other devices?**
A: Yes, enable "Clear other notifications after first response"

**Q: How do timeouts work with multiple devices?**
A: You can choose:
- Individual: Each device has its own timeout
- Global: One timeout for all devices together
```

---

## Implementation Estimate

### Time Breakdown
- Phase 1 (Input Reorg): 2 hours
- Phase 2 (Multi-Device Infra): 4 hours
- Phase 3 (Response Handling): 4 hours
- Phase 4 (Timeout Config): 4 hours
- Phase 5 (Integration & Testing): 6 hours
- **Total**: ~20 hours

### Risk Factors
- **Medium Risk**: Device platform detection may not be 100% accurate
- **Low Risk**: Template complexity in service name construction
- **Low Risk**: Event handling order with multiple devices

---

## Next Steps

1. ✅ Complete research and planning
2. Get user approval on plan
3. Begin Phase 1 implementation
4. Iterate through phases with testing
5. Update documentation
6. Release version 2026.3.0

---

## Appendix: Sample Code Snippets

### Device Loop for Sending
```yaml
- repeat:
    for_each: !input notify_devices
    sequence:
      - variables:
          device_name: "{{ device_attr(repeat.item, 'name') | lower | replace(' ', '_') }}"
          is_ios: "{{ 'iphone' in device_name or 'ipad' in device_name }}"
      - service: "notify.mobile_app_{{ device_name }}"
        data:
          title: !input title
          message: !input message
          data:
            tag: "{{ notification_tag }}"
            # iOS specific
            {% if is_ios %}
            push:
              interruption-level: !input interruption_level
            {% endif %}
            # Android specific
            {% if not is_ios %}
            channel: !input channel
            importance: !input importance
            {% endif %}
```

### First Response Detection
```yaml
- wait_for_trigger:
    - platform: event
      event_type: mobile_app_notification_action
      event_data:
        tag: "{{ notification_tag }}"
  timeout: !input timeout
  continue_on_timeout: true

- variables:
    first_responder: "{{ wait.trigger.event.data.device_id if wait.trigger else none }}"
    response_action: "{{ wait.trigger.event.data.action if wait.trigger else none }}"
```

### Clear Other Devices
```yaml
{% if clear_other_notifications and first_responder %}
- repeat:
    for_each: !input notify_devices
    sequence:
      - condition: template
        value_template: "{{ repeat.item != first_responder }}"
      - service: "notify.mobile_app_{{ device_attr(repeat.item, 'name') | lower | replace(' ', '_') }}"
        data:
          message: "clear_notification"
          data:
            tag: "{{ notification_tag }}"
{% endif %}
```

---

**End of Implementation Plan**
