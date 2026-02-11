#!/usr/bin/env python3
"""
Reorganize notification blueprint:
1. Remove emojis
2. Separate iOS and Android specific settings
3. Add missing practical fields
"""

import re

# Read the current file
with open('notifications.yaml', 'r', encoding='utf-8') as f:
    content = f.read()

# Function to remove emojis from text
def remove_emojis(text):
    # Remove emoji patterns but keep the text
    # Common emojis in the blueprint
    emoji_map = {
        '🔔': '',
        '📲': '',
        '🏷️': '',
        '💬': '',
        '🙂': '',
        '🎨': '',
        '��': '',
        '1️⃣': 'Option 1',
        '2️⃣': 'Option 2', 
        '3️⃣': 'Option 3',
        '⏱️': '',
        '⌛️': '',
        '🧹': '',
        '📸': '',
        '🔗': '',
        '🔔': '',
        '🍎': 'iOS',
        '🤖': 'Android',
        '❔': '',
        '👍🏻': '',
        '⚠️': 'Warning:',
        '✅': '',
        '❌': '',
    }
    
    result = text
    for emoji, replacement in emoji_map.items():
        result = result.replace(emoji, replacement)
    
    # Clean up extra spaces
    result = re.sub(r'\s+', ' ', result)
    result = result.strip()
    
    return result

# Update blueprint name (remove emojis)
content = content.replace(
    'name: 🔔 Notifications (Version 2.1.0 - UI Improved)',
    'name: Notifications (Version 2.1.0 - Platform Organized)'
)

# Update description title
content = content.replace(
    '<h2>🔔 Notifications</h2>',
    '<h2>Notifications</h2>'
)

# Update the version in description
content = content.replace(
    '<b>Version 2.1.0 - UI Improved - UI Improved</b>',
    '<b>Version 2.1.0 - Platform Organized</b>'
)

# Save
with open('notifications.yaml', 'w', encoding='utf-8') as f:
    f.write(content)

print("Step 1: Updated blueprint name and version")
print("Next: Will reorganize sections...")

