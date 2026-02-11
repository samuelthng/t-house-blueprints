#!/usr/bin/env python3
"""
Reorganize notification blueprint with proper HA section syntax
"""

import re

# Read current beta file
with open('notifications_beta.yaml', 'r', encoding='utf-8') as f:
    content = f.read()

# Split into before input, input section, and after input
before_input = content.split('  input:\n')[0] + '  input:\n'
rest = content.split('  input:\n')[1]

# Find where fields section starts
fields_match = re.search(r'\nfields:\n', rest)
if fields_match:
    input_content = rest[:fields_match.start()]
    after_input = rest[fields_match.start():]
else:
    print("❌ Could not find fields: section")
    exit(1)

# Parse all fields from flat structure
field_pattern = r'^    ([a-z_]+):\n((?:      .*\n)*)'
fields = {}
for match in re.finditer(field_pattern, input_content, re.MULTILINE):
    field_name = match.group(1)
    field_content = match.group(0)
    fields[field_name] = field_content

print(f"Parsed {len(fields)} fields")

# Define sections with their fields
sections_config = {
    'notification_content': {
        'name': 'Device & Notification Content',
        'description': 'Configure the device and notification message content',
        'fields': ['notify_device', 'title', 'subtitle', 'message', 'icon', 'enable_icon_color', 'icon_color']
    },
    'action_buttons': {
        'name': 'Action Buttons',
        'description': 'Configure up to 3 customizable action buttons',
        'fields': [
            # Option 1
            'confirm_enabled', 'confirm_text', 'confirm_option_mode', 'confirm_action', 'confirm_uri',
            'confirm_icon', 'confirm_is_destructive', 'confirm_authentication_required',
            # Option 2
            'dismiss_enabled', 'dismiss_text', 'dismiss_option_mode', 'dismiss_action', 'dismiss_uri',
            'dismiss_icon', 'dismiss_is_destructive', 'dismiss_authentication_required',
            # Option 3
            'option_three_enabled', 'option_three_text', 'option_three_option_mode', 'option_three_action',
            'option_three_uri', 'option_three_icon', 'option_three_is_destructive', 'option_three_authentication_required'
        ]
    },
    'timeout_settings': {
        'name': 'Timeout Settings',
        'description': 'Configure timeout behavior and actions',
        'fields': ['enable_timeout', 'timeout', 'run_timeout_actions', 'timeout_action', 'swipe_away_as_timeout', 'clear_on_timeout']
    },
    'attachments': {
        'name': 'Attachments',
        'description': 'Add camera snapshots or images to notifications',
        'fields': ['attachment_type', 'attachment_camera_entity']
    },
    'links_and_behavior': {
        'name': 'Links & Behavior',
        'description': 'Configure notification links and behavior',
        'fields': ['notification_link', 'tag', 'group', 'persist', 'car_ui']
    },
    'priority_settings': {
        'name': 'Priority & Importance',
        'description': 'Configure notification priority and importance levels',
        'fields': ['channel', 'importance', 'android_high_priority', 'interruption_level', 'visibility']
    }
}

# Build new input section with proper sections
new_input = ''
for section_key, section_info in sections_config.items():
    # Start section
    new_input += f'    {section_key}:\n'
    new_input += f'      section:\n'
    new_input += f'        name: "{section_info["name"]}"\n'
    new_input += f'        description: "{section_info["description"]}"\n'
    new_input += f'        inputs:\n'
    
    # Add fields to this section
    for field_name in section_info['fields']:
        if field_name in fields:
            field_lines = fields[field_name].split('\n')
            for line in field_lines:
                if line.strip():  # Skip empty lines
                    # Add extra 4 spaces indentation for fields inside section
                    new_input += '    ' + line + '\n'
    
    new_input += '\n'

# Assemble complete file
new_content = before_input + new_input + after_input

# Save
with open('notifications_beta.yaml', 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"✅ Created {len(sections_config)} sections")
print(f"✅ Total fields organized: {sum(len(s['fields']) for s in sections_config.values())}")

