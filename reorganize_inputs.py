#!/usr/bin/env python3
import re

# Read the backup file
with open('notifications.yaml.backup', 'r', encoding='utf-8') as f:
    content = f.read()

# Split into before input, input section, and after input
before_input = content.split('  input:\n')[0] + '  input:\n'
rest_after_input_start = content.split('  input:\n')[1]
input_and_after = rest_after_input_start.split('\nfields:\n')
old_input_content = input_and_after[0]
after_fields = '\nfields:\n' + input_and_after[1]

# Parse the old input section to extract all fields
lines = old_input_content.split('\n')
fields_dict = {}
current_field = None
current_field_lines = []

for line in lines:
    # Check if this starts a new field (4 spaces + fieldname + colon)
    if re.match(r'^    [a-z_]+:$', line):
        # Save previous field
        if current_field:
            fields_dict[current_field] = '\n'.join(current_field_lines)
        
        current_field = line.strip()[:-1]  # Remove the :
        current_field_lines = [line]
    elif current_field:
        current_field_lines.append(line)

# Save the last field
if current_field:
    fields_dict[current_field] = '\n'.join(current_field_lines)

print(f"Extracted {len(fields_dict)} fields")

# Define the new structure with grouped fields
new_structure = '''    ##############################
    # Section 1: Device & Notification Content
    ##############################
    notification_content:
      name: "📲 Device & Notification Content"
      icon: mdi:cellphone-message
      collapsed: true
      input:
{notify_device}
{title}
{subtitle}
{message}
{icon}
{enable_icon_color}
{icon_color}

    ##############################
    # Section 2: Action Buttons
    ##############################
    action_buttons:
      name: "🔘 Action Buttons"
      icon: mdi:gesture-tap-button
      collapsed: true
      input:
        ## Option 1
{confirm_enabled}
{confirm_text}
{confirm_option_mode}
{confirm_action}
{confirm_uri}
{confirm_icon}
{confirm_is_destructive}
{confirm_authentication_required}

        ## Option 2
{dismiss_enabled}
{dismiss_text}
{dismiss_option_mode}
{dismiss_action}
{dismiss_uri}
{dismiss_icon}
{dismiss_is_destructive}
{dismiss_authentication_required}

        ## Option 3
{option_three_enabled}
{option_three_text}
{option_three_option_mode}
{option_three_action}
{option_three_uri}
{option_three_icon}
{option_three_is_destructive}
{option_three_authentication_required}

    ##############################
    # Section 3: Timeout Settings
    ##############################
    timeout_settings:
      name: "⏱️ Timeout Settings"
      icon: mdi:timer-outline
      collapsed: true
      input:
{enable_timeout}
{timeout}
{run_timeout_actions}
{timeout_action}
{swipe_away_as_timeout}
{clear_on_timeout}

    ##############################
    # Section 4: Attachments
    ##############################
    attachments:
      name: "📸 Attachments"
      icon: mdi:camera
      collapsed: true
      input:
{attachment_type}
{attachment_camera_entity}

    ##############################
    # Section 5: Links & Behavior
    ##############################
    links_and_behavior:
      name: "🔗 Links & Behavior"
      icon: mdi:cog-outline
      collapsed: true
      input:
{notification_link}
{tag}
{group}
{persist}
{car_ui}

    ##############################
    # Section 6: Priority & Importance
    ##############################
    priority_settings:
      name: "🔔 Priority & Importance"
      icon: mdi:bell-alert
      collapsed: true
      input:
{channel}
{importance}
{android_high_priority}
{interruption_level}
{visibility}

'''

# Fill in the placeholders with actual field definitions
# Need to indent each field by 4 more spaces (total 8 spaces for fields inside sections)
formatted_fields = {}
for field_name, field_content in fields_dict.items():
    # Add 4 spaces to each line of the field
    indented_lines = []
    for line in field_content.split('\n'):
        if line.strip():  # Don't indent empty lines more
            indented_lines.append('    ' + line)
        else:
            indented_lines.append(line)
    formatted_fields[field_name] = '\n'.join(indented_lines)

# Apply the fields to the template
try:
    new_input_section = new_structure.format(**formatted_fields)
    
    # Assemble the complete file
    new_content = before_input + new_input_section + after_fields
    
    # Write the new file
    with open('notifications.yaml', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("✅ Successfully reorganized inputs into collapsed sections!")
    print(f"   New file size: {len(new_content)} bytes")
    
except KeyError as e:
    print(f"❌ Missing field: {e}")
    print(f"Available fields: {sorted(fields_dict.keys())}")

