#!/usr/bin/env python3
"""
Complete reorganization of notifications blueprint:
1. Remove emojis
2. Separate iOS and Android specific settings
3. Restructure sections properly
"""

import re

# Read the backup file (original with emojis and current structure)
with open('notifications_v2.1.0_backup.yaml', 'r', encoding='utf-8') as f:
    content = f.read()

print("Step 1: Removing emojis from names and descriptions...")

# Remove emojis but keep meaningful text
def clean_text(text):
    """Remove emojis from text"""
    # Map emojis to replacements
    replacements = {
        '🔔 ': '',
        '📲 ': '',
        '🏷️ ': '',
        '💬 ': '',
        '🙂 ': '',
        '🎨 ': '',
        '🔘 ': '',
        '1️⃣ ': 'Option 1 - ',
        '2️⃣ ': 'Option 2 - ',
        '3️⃣ ': 'Option 3 - ',
        '⏱️ ': '',
        '⌛️ ': '',
        '🧹 ': '',
        '📸 ': '',
        '🔗 ': '',
        '🔔 ': '',
        '🍎 ': 'iOS: ',
        '🤖 ': 'Android: ',
        '❔ ': '',
        '👍🏻 ': '',
        '⚠️ ': 'Warning: ',
        '✅ ': '',
        '❌ ': '',
        '` iOS Only`': '(iOS Only)',
        '`iOS Only`': '(iOS Only)',
        '`🤖 Android Only`': '(Android Only)',
        '` Android Only`': '(Android Only)',
        '`Android Only`': '(Android Only)',
    }
    
    result = text
    for emoji, replacement in replacements.items():
        result = result.replace(emoji, replacement)
    
    return result

# Update blueprint name
content = content.replace(
    'name: 🔔 Notifications (Version 2.1.0 - UI Improved)',
    'name: Notifications v2.1.0 - Platform Organized'
)

# Update description header
content = content.replace(
    '<h2>🔔 Notifications</h2>',
    '<h2>Notifications</h2>'
)

# Update version string
content = content.replace(
    '<b>Version 2.1.0 - UI Improved</b>',
    '<b>Version 2.1.0 - Platform Organized</b>'
)

# Clean section names
content = content.replace('name: "📲 Device & Notification Content"', 'name: "Device & Notification Content"')
content = content.replace('name: "🔘 Action Buttons"', 'name: "Action Buttons"')
content = content.replace('name: "⏱️ Timeout Settings"', 'name: "Timeout Settings"')
content = content.replace('name: "📸 Attachments"', 'name: "Attachments"')
content = content.replace('name: "🔗 Links & Behavior"', 'name: "Links & Behavior"')
content = content.replace('name: "🔔 Priority & Importance"', 'name: "Priority & Importance"')

# Clean field names (remove emoji prefixes)
field_name_patterns = [
    (r'name: "📲 (.*?)"', r'name: "\1"'),
    (r'name: "🏷️ (.*?)"', r'name: "\1"'),
    (r'name: "💬 (.*?)"', r'name: "\1"'),
    (r'name: "🙂 (.*?)"', r'name: "\1"'),
    (r'name: "🎨 (.*?)"', r'name: "\1"'),
    (r'name: "1️⃣ (.*?)"', r'name: "Option 1 - \1"'),
    (r'name: "2️⃣ (.*?)"', r'name: "Option 2 - \1"'),
    (r'name: "3️⃣ (.*?)"', r'name: "Option 3 - \1"'),
    (r'name: "⌛️ (.*?)"', r'name: "\1"'),
    (r'name: "🧹 (.*?)"', r'name: "\1"'),
    (r'name: "📸 (.*?)"', r'name: "\1"'),
    (r'name: "🔗 (.*?)"', r'name: "\1"'),
    (r'name: "🚘 (.*?)"', r'name: "\1"'),
    (r'name: "🔖 (.*?)"', r'name: "\1"'),
    (r'name: "📣 (.*?)"', r'name: "\1"'),
    (r'name: "❕ (.*?)"', r'name: "\1"'),
    (r'name: "🔏 (.*?)"', r'name: "\1"'),
    (r'name: "🚩 (.*?)"', r'name: "\1"'),
]

for pattern, replacement in field_name_patterns:
    content = re.sub(pattern, replacement, content)

# Clean emoji markers in descriptions
content = re.sub(r'`🤖 Android Only`', '(Android Only)', content)
content = re.sub(r'` iOS Only`', '(iOS Only)', content)
content = re.sub(r'`iOS Only`', '(iOS Only)', content)
content = re.sub(r'`🍎 iOS`', 'iOS:', content)
content = re.sub(r'`🤖 Android`', 'Android:', content)
content = re.sub(r'🍎 iOS', 'iOS', content)
content = re.sub(r'🤖 Android', 'Android', content)
content = re.sub(r'❔ ', '', content)
content = re.sub(r'👍🏻 ', '', content)
content = re.sub(r'⚠️ ', 'Warning: ', content)

# Save the cleaned version
with open('notifications.yaml', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Step 1 complete: Emojis removed")
print(f"   File size: {len(content)} bytes")

