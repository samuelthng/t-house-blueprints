# Jinja2 Template Examples Guide

This document provides comprehensive examples of using Jinja2 templates in the Notifications Blueprint.

## Overview

The following fields support Jinja2 templating in Home Assistant:
- Title
- Subtitle
- Message
- Sound
- Notification Link
- Most text-based fields

## Field-by-Field Examples

### 📝 Title

**Static Example:**
```yaml
title: "Front Door Motion Detected"
```

**Template Examples:**
```yaml
# Use entity friendly name
title: "{{ trigger.to_state.attributes.friendly_name }} Alert"

# Include timestamp
title: "Motion at {{ now().strftime('%I:%M %p') }}"

# Combine multiple elements
title: "{{ trigger.to_state.name }} - {{ states('sensor.temperature') }}°F"
```

### 📝 Subtitle (iOS Only)

**Static Example:**
```yaml
subtitle: "Person detected at 3:45 PM"
```

**Template Examples:**
```yaml
# Show sensor state
subtitle: "{{ states('sensor.front_door_last_detection') }}"

# Current time
subtitle: "Detected at {{ now().strftime('%I:%M %p') }}"

# Entity attribute
subtitle: "{{ state_attr('sensor.motion_sensor', 'last_changed') }}"
```

### 💬 Message

**Static Example:**
```yaml
message: "Motion detected at front door"
```

**Template Examples:**
```yaml
# Basic entity state
message: "{{ trigger.to_state.attributes.friendly_name }} is {{ trigger.to_state.state }}"

# Conditional message
message: >
  {% if is_state('binary_sensor.front_door', 'on') %}
    Door is open
  {% else %}
    Door is closed
  {% endif %}

# Multi-line with multiple sensors
message: |
  Temperature: {{ states('sensor.bedroom_temp') }}°F
  Humidity: {{ states('sensor.bedroom_humidity') }}%
  
# Complex conditional
message: >
  {% if states('lock.front_door') == 'unlocked' %}
    ⚠️ Front door is unlocked!
  {% elif states('binary_sensor.front_door') == 'on' %}
    🚪 Front door is open
  {% else %}
    ✅ Front door is secure
  {% endif %}
```

### 🔊 Sound

**Static Example:**
```yaml
sound: "alarm.mp3"
```

**Template Examples:**
```yaml
# Conditional sound based on sensor
sound: >
  {% if is_state('binary_sensor.motion_front_door', 'on') %}
    alarm.mp3
  {% else %}
    notification.mp3
  {% endif %}

# Based on time of day
sound: >
  {% if now().hour >= 22 or now().hour < 7 %}
    silent.mp3
  {% else %}
    default
  {% endif %}

# Based on priority
sound: >
  {% if is_state('alarm_control_panel.home', 'triggered') %}
    alarm.mp3
  {% elif is_state('binary_sensor.smoke_detector', 'on') %}
    fire_alarm.mp3
  {% else %}
    default
  {% endif %}
```

### 🔗 Notification Link

**Static Examples:**
```yaml
# View cameras dashboard
notification_link: "/lovelace/cameras"

# View security dashboard
notification_link: "/lovelace/security"

# Entity view
notification_link: "entityId:camera.front_door"
```

**Template Examples:**
```yaml
# Dynamic dashboard based on trigger
notification_link: "/lovelace/{{ trigger.entity_id.split('.')[1] }}"

# Conditional link
notification_link: >
  {% if 'camera' in trigger.entity_id %}
    entityId:{{ trigger.entity_id }}
  {% else %}
    /lovelace/home
  {% endif %}

# Link to specific entity based on area
notification_link: >
  entityId:camera.{{ trigger.to_state.attributes.area_id }}_camera
```

## Common Template Patterns

### Access Entity State
```jinja2
{{ states('sensor.temperature') }}
{{ states('binary_sensor.motion') }}
```

### Access Entity Attributes
```jinja2
{{ state_attr('sensor.weather', 'temperature') }}
{{ trigger.to_state.attributes.friendly_name }}
```

### Conditionals
```jinja2
{% if condition %}
  text if true
{% else %}
  text if false
{% endif %}
```

### Time Formatting
```jinja2
{{ now().strftime('%I:%M %p') }}  # 03:45 PM
{{ now().strftime('%Y-%m-%d') }}  # 2024-02-11
{{ as_timestamp(now()) | timestamp_custom('%H:%M') }}  # 15:45
```

### Multi-line Text
```jinja2
{{ states('sensor.temp') }}°F
{{ states('sensor.humidity') }}%
Status: {{ states('binary_sensor.motion') }}
```

## Real-World Examples

### Security Alert
```yaml
title: "🚨 {{ trigger.to_state.attributes.friendly_name }}"
message: >
  Motion detected at {{ now().strftime('%I:%M %p') }}
  
  Location: {{ trigger.to_state.attributes.area_id }}
  {% if is_state('alarm_control_panel.home', 'armed_away') %}
  ⚠️ System is armed!
  {% endif %}
sound: >
  {% if is_state('alarm_control_panel.home', 'armed_away') %}
    alarm.mp3
  {% else %}
    notification.mp3
  {% endif %}
notification_link: "entityId:camera.{{ trigger.to_state.attributes.area_id }}"
```

### Temperature Alert
```yaml
title: "🌡️ Temperature Alert"
message: >
  {{ trigger.to_state.attributes.friendly_name }} is {{ trigger.to_state.state }}°F
  
  {% if trigger.to_state.state | float > 80 %}
    ⚠️ Temperature is too high!
  {% elif trigger.to_state.state | float < 60 %}
    ❄️ Temperature is too low!
  {% endif %}
notification_link: "/lovelace/climate"
```

### Door Left Open
```yaml
title: "🚪 Door Alert"
message: >
  {{ trigger.to_state.attributes.friendly_name }} has been open for 
  {{ relative_time(trigger.to_state.last_changed) }}
  
  {% if states('lock.' + trigger.entity_id.split('.')[1]) == 'unlocked' %}
  🔓 Door is also unlocked!
  {% endif %}
notification_link: >
  entityId:{{ trigger.entity_id }}
```

## Tips

1. **Test Templates**: Use Developer Tools → Template to test your templates before using them
2. **Handle None Values**: Use `| default('Unknown')` to handle missing states
3. **Type Conversion**: Use `| float` or `| int` when doing math operations
4. **Keep it Simple**: Start with simple templates and build complexity gradually
5. **Escape Characters**: Use quotes properly to avoid YAML parsing issues

## Resources

- [Home Assistant Templating Documentation](https://www.home-assistant.io/docs/configuration/templating/)
- [Jinja2 Template Designer Documentation](https://jinja.palletsprojects.com/en/latest/templates/)
- [Template Editor in Developer Tools](https://www.home-assistant.io/docs/tools/dev-tools/#template-editor)
