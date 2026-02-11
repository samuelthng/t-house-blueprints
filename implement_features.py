"""
Add Phase 1 high-priority features to notifications blueprint
- Maintains backwards compatibility
- Adds inputs to appropriate sections
- Adds fields for runtime override
- Updates notification data payload
"""

import yaml
import re

class CustomLoader(yaml.SafeLoader):
    pass

def input_constructor(loader, node):
    return loader.construct_scalar(node)

CustomLoader.add_constructor('!input', input_constructor)

# Read current blueprint
with open('notifications.yaml', 'r', encoding='utf-8') as f:
    content = f.read()

# Split into parts: before input, input section, fields section, action section
before_input = content.split('  input:\n', 1)[0] + '  input:\n'
rest_after_input = content.split('  input:\n', 1)[1]

# Find where fields starts
if '\nfields:\n' in rest_after_input:
    input_section = rest_after_input.split('\nfields:\n')[0]
    after_input_before_fields = '\nfields:\n'
    rest_after_fields = rest_after_input.split('\nfields:\n')[1]
    
    # Split fields from sequence
    if '\nsequence:\n' in rest_after_fields:
        fields_section = rest_after_fields.split('\nsequence:\n')[0]
        after_fields = '\nsequence:\n' + rest_after_fields.split('\nsequence:\n')[1]
    else:
        fields_section = rest_after_fields
        after_fields = ''
else:
    # No fields section yet
    input_section = rest_after_input.split('\nsequence:\n')[0]
    after_input_before_fields = '\n'
    fields_section = ''
    after_fields = '\nsequence:\n' + rest_after_input.split('\nsequence:\n')[1]

print("✅ Parsed blueprint structure")
print(f"  - Input section: {len(input_section)} chars")
print(f"  - Fields section: {len(fields_section)} chars")
print(f"  - Sequence section: {len(after_fields)} chars")

# Parse current sections
data = yaml.load(before_input + '  input:\n' + input_section, Loader=CustomLoader)
current_sections = data['blueprint']['input']

print(f"\n✅ Found {len(current_sections)} existing sections:")
for key in current_sections.keys():
    print(f"  - {key}")

# Define new features to add
new_features = {
    'notification_content': [
        {
            'name': 'sound',
            'yaml': '''        sound:
          name: "🔊 Sound"
          description: >
            Custom notification sound.
            
            **🍎 iOS**: Use sound file name (e.g., `bell.caf`) from the app or `default` for system sound.
            
            **🤖 Android**: Use sound file name or `default`. 
            
            **Example**: `default`, `bell.caf`, `mysound.mp3`
            
            `Optional`
          default: ""
          selector:
            text:'''
        }
    ],
    'attachments': [
        {
            'name': 'image_url',
            'yaml': '''        image_url:
          name: "🖼️ Image URL"
          description: >
            Direct URL to an image to attach to the notification.
            
            Alternative to camera entity snapshots. Use publicly accessible URLs or local media.
            
            **Example**: `https://example.com/image.jpg` or `/local/image.png`
            
            `Optional`
          default: ""
          selector:
            text:'''
        },
        {
            'name': 'video_url',
            'yaml': '''        video_url:
          name: "🎥 Video URL"
          description: >
            URL to a video file to attach to the notification.
            
            **🍎 iOS**: Supports MP4, MOV formats. Video must be accessible.
            
            **🤖 Android**: Displays thumbnail with play button.
            
            **Example**: `https://example.com/video.mp4`
            
            `Optional`
          default: ""
          selector:
            text:'''
        }
    ],
    'ios_settings': [
        {
            'name': 'badge',
            'yaml': '''        badge:
          name: "🔴 App Badge"
          description: >
            Number to display on the app icon badge.
            
            Set to `0` to clear badge. Leave empty to not change badge.
            
            **Example**: `1` for one unread notification, `0` to clear
            
            `🍎 iOS Only`, `Optional`
          default: ""
          selector:
            number:
              min: 0
              max: 999
              mode: box'''
        },
        {
            'name': 'thread_id',
            'yaml': '''        thread_id:
          name: "�� Thread ID"
          description: >
            Group notifications into conversation threads.
            
            Notifications with the same thread-id appear grouped together.
            
            **Example**: `doorbell-alerts`, `security-cameras`
            
            `🍎 iOS Only`, `Optional`
          default: ""
          selector:
            text:'''
        },
        {
            'name': 'presentation_options',
            'yaml': '''        presentation_options:
          name: "📱 Presentation Options"
          description: >
            Control how notification is presented when app is in foreground.
            
            Select which alerts to show: banner, sound, badge, or list.
            
            Leave empty to use system defaults.
            
            `🍎 iOS Only`, `Optional`
          default: []
          selector:
            select:
              multiple: true
              options:
                - label: "Show banner"
                  value: "banner"
                - label: "Play sound"
                  value: "sound"
                - label: "Update badge"
                  value: "badge"
                - label: "Show in notification list"
                  value: "list"'''
        }
    ],
    'android_settings': [
        {
            'name': 'sticky',
            'yaml': '''        sticky:
          name: "📌 Sticky Notification"
          description: >
            Make notification non-dismissible (user cannot swipe away).
            
            Useful for critical notifications that require action.
            
            **Example use**: Alarm notifications, security alerts
            
            `🤖 Android Only`, `Optional`
          default: false
          selector:
            boolean:'''
        },
        {
            'name': 'vibration_pattern',
            'yaml': '''        vibration_pattern:
          name: "📳 Vibration Pattern"
          description: >
            Custom vibration pattern as comma-separated durations in milliseconds.
            
            Pattern alternates: wait, vibrate, wait, vibrate, etc.
            
            **Example**: `100,1000,100,1000` (short-long-short-long)
            
            `🤖 Android Only`, `Optional`
          default: ""
          selector:
            text:'''
        },
        {
            'name': 'led_color',
            'yaml': '''        led_color:
          name: "💡 LED Color"
          description: >
            Color of the notification LED (for devices with LED).
            
            Use color name or hex code.
            
            **Example**: `red`, `blue`, `#FF5733`
            
            `🤖 Android Only`, `Optional`
          default: ""
          selector:
            text:'''
        },
        {
            'name': 'alert_once',
            'yaml': '''        alert_once:
          name: "🔕 Alert Once"
          description: >
            Play sound and vibrate only when notification is first shown.
            
            Updates to the same tag won't make noise again.
            
            **Example use**: Status updates, progress notifications
            
            `🤖 Android Only`, `Optional`
          default: false
          selector:
            boolean:'''
        }
    ]
}

print(f"\n✅ Defined {sum(len(v) for v in new_features.values())} new features to add")

# Now let's add them to the appropriate sections
# This will be done by reconstructing each section

