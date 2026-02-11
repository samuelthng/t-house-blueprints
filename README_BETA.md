# Notifications BETA Blueprint

This is a beta/testing version of the Notifications blueprint with the following improvements:

## What's New in v2.1.1 Beta

### Critical Fix
- **iOS Tag Truncation Fix**: Resolves iOS notification failures by truncating tags to 64 bytes
  - Fixes Issue #47 where iOS users couldn't receive notifications in v2.0+
  - Tags are now: `| truncate(64, killwords=True, end='')`

### Improvements
- Platform organization preparation
- Version updated to 2.1.1
- Comprehensive changelog

## Import URL

```
https://github.com/samuelthng/t-house-blueprints/blob/main/notifications_beta.yaml
```

## Testing Alongside Current Blueprint

This beta version can be imported alongside your current notifications blueprint. They have different names:
- Main: "🔔 Notifications (Version 2.0.2 Beta)"
- Beta: "🔔 Notifications BETA (v2.1.1 - Platform Separated)"

You can test the new features without replacing your existing working blueprint.

## Features

Same as the main notifications blueprint, plus:
- iOS fix for tag length issues
- Foundation for platform-specific organization
- Updated changelog and documentation

## Feedback

Please report any issues or feedback in the main repository issues.

