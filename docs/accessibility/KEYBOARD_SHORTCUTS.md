# NUAA CLI Keyboard Shortcuts & Accessibility Guide

**Complete keyboard navigation reference for accessible use of NUAA CLI**

---

## Table of Contents

- [Overview](#overview)
- [Global Shortcuts](#global-shortcuts)
- [Interactive Menu Navigation](#interactive-menu-navigation)
- [Command Input](#command-input)
- [Alternative Input Methods](#alternative-input-methods)
- [Screen Reader Compatibility](#screen-reader-compatibility)
- [Customizing Shortcuts](#customizing-shortcuts)
- [Accessibility Modes](#accessibility-modes)
- [Troubleshooting](#troubleshooting)

---

## Overview

NUAA CLI is fully keyboard-accessible and does not require a mouse. This guide covers all keyboard shortcuts and navigation patterns.

**Accessibility Principle**: Every function can be accessed via keyboard alone.

---

## Global Shortcuts

These work anywhere in NUAA CLI:

| Shortcut    | Action         | Notes                                      |
| ----------- | -------------- | ------------------------------------------ |
| `Ctrl+C`    | Cancel/Exit    | Works in all contexts, safe to use anytime |
| `Ctrl+D`    | Exit (EOF)     | Alternative to Ctrl+C at prompts           |
| `?`         | Show help      | Context-sensitive help for current screen  |
| `Esc`       | Go back/Cancel | In menus and dialogs                       |
| `Tab`       | Next field     | In forms and multi-field inputs            |
| `Shift+Tab` | Previous field | In forms and multi-field inputs            |

---

## Interactive Menu Navigation

When NUAA CLI shows a menu (like AI assistant selection):

### Basic Navigation

| Shortcut           | Action                           |
| ------------------ | -------------------------------- |
| `↑` or `k`         | Move up one item                 |
| `↓` or `j`         | Move down one item               |
| `Enter` or `Space` | Select current item              |
| `Esc`              | Cancel menu                      |
| `Home` or `g`      | Jump to first item               |
| `End` or `G`       | Jump to last item                |
| `Ctrl+N`           | Next item (alternative to ↓)     |
| `Ctrl+P`           | Previous item (alternative to ↑) |

### Vim-Style Navigation

For users familiar with Vim:

| Shortcut | Action     |
| -------- | ---------- |
| `j`      | Move down  |
| `k`      | Move up    |
| `g`      | First item |
| `G`      | Last item  |
| `Enter`  | Select     |

### Quick Jump (Large Lists)

| Shortcut    | Action                                       |
| ----------- | -------------------------------------------- |
| Type letter | Jump to first item starting with that letter |
| `PgUp`      | Jump up 10 items                             |
| `PgDn`      | Jump down 10 items                           |

---

## Command Input

When entering text at a prompt:

### Text Editing

| Shortcut     | Action                      | Platform  |
| ------------ | --------------------------- | --------- |
| `Ctrl+A`     | Move to start of line       | All       |
| `Ctrl+E`     | Move to end of line         | All       |
| `Ctrl+K`     | Delete from cursor to end   | All       |
| `Ctrl+U`     | Delete from cursor to start | All       |
| `Ctrl+W`     | Delete word backward        | All       |
| `Alt+D`      | Delete word forward         | Linux/Mac |
| `Ctrl+Left`  | Move word backward          | Windows   |
| `Ctrl+Right` | Move word forward           | Windows   |
| `Alt+B`      | Move word backward          | Linux/Mac |
| `Alt+F`      | Move word forward           | Linux/Mac |

### History Navigation

| Shortcut | Action                                |
| -------- | ------------------------------------- |
| `↑`      | Previous command in history           |
| `↓`      | Next command in history               |
| `Ctrl+R` | Search command history (if supported) |

### Auto-Complete

| Shortcut  | Action                       |
| --------- | ---------------------------- |
| `Tab`     | Auto-complete (if available) |
| `Tab Tab` | Show all completions         |

---

## Alternative Input Methods

NUAA CLI supports various alternative input methods:

### Voice Control

For users using voice control software (Dragon, Voice Control):

**Recommended voice commands:**

- "Press Enter" → Submit
- "Press Escape" → Cancel
- "Press Down Arrow" → Navigate down
- "Press Up Arrow" → Navigate up
- "Type [text]" → Enter text

**Dictation Mode**: Most voice control software supports dictation for text input.

### Switch Control

For users using switch control:

**Navigation Tips:**

- Use single switch to scan through menu items
- Second switch to select
- Most systems support "step scanning" (auto-advance)

**Recommended Settings:**

- Set scan speed to comfortable rate (2-3 seconds)
- Enable audio feedback if available
- Use simple mode: `nuaa onboard` → enable simple mode

### One-Handed Operation

NUAA CLI can be used one-handed:

**Left-Hand Shortcuts:**

- Use `Ctrl+N` and `Ctrl+P` instead of arrow keys
- Use `Ctrl+C` instead of Esc
- Use `Tab` for navigation

**Right-Hand Shortcuts:**

- Use `j` and `k` for navigation (Vim-style)
- Use `Enter` for selection
- Arrow keys are right-hand friendly

---

## Screen Reader Compatibility

NUAA CLI works with major screen readers:

### Tested Screen Readers

| Screen Reader | Platform | Compatibility | Notes                           |
| ------------- | -------- | ------------- | ------------------------------- |
| **NVDA**      | Windows  | ✅ Full       | Enable terminal mode            |
| **JAWS**      | Windows  | ✅ Full       | Use version 2020+               |
| **VoiceOver** | macOS    | ✅ Full       | Enable "Use screen flash"       |
| **Orca**      | Linux    | ✅ Full       | Configure terminal profile      |
| **Narrator**  | Windows  | ⚠️ Partial    | Basic support, NVDA recommended |

### Screen Reader Mode

Enable screen reader optimizations:

```bash
export NUAA_SCREEN_READER=1
nuaa --help
```

Or set permanently in your shell profile:

```bash
echo 'export NUAA_SCREEN_READER=1' >> ~/.bashrc  # Linux/Mac
```

**Screen Reader Mode Features:**

- No spinners or animations
- Verbose descriptions of all actions
- Clear status announcements
- Structured navigation hints
- No reliance on color or visual formatting

### Reading Output

**Best Practices:**

1. Use "read all" command to hear full output
2. Use line-by-line reading for menus
3. Enable "speak typed characters" for input confirmation
4. Use "find" function to search output

**NVDA Specific:**

```
Insert+Down Arrow: Read next line
Insert+Up Arrow: Read previous line
Insert+Home: Start reading from top
Numpad Plus: Read current line
```

**VoiceOver Specific:**

```
Ctrl+Option+A: Start reading
Ctrl+Option+Left/Right: Navigate word by word
Ctrl+Option+Up/Down: Navigate line by line
Ctrl: Stop reading
```

---

## Customizing Shortcuts

While NUAA CLI uses standard shortcuts, you can customize them via terminal settings:

### Windows (Windows Terminal)

Edit `settings.json`:

```json
{
  "actions": [{ "command": "paste", "keys": "ctrl+v" }]
}
```

### macOS (Terminal.app)

**Preferences → Profiles → Keyboard**:

- Map custom key combinations
- Create shortcuts for common commands

### Linux (GNOME Terminal)

**Edit → Preferences → Shortcuts**:

- Customize terminal shortcuts
- Map function keys
- Create custom keybindings

---

## Accessibility Modes

NUAA CLI offers several accessibility modes:

### Simple Mode

**One question at a time, clear instructions:**

```bash
export NUAA_SIMPLE_MODE=1
nuaa onboard
```

**Features:**

- No complex menus
- Step-by-step guidance
- Clear "back" and "cancel" options
- Progress indicator (Step X of Y)

### High Contrast Mode

**Enhanced visibility:**

```bash
export NUAA_HIGH_CONTRAST=1
nuaa --help
```

**Features:**

- Bolder symbols
- Clearer visual separation
- Enhanced success/error indicators

### No Color Mode

**For color blindness:**

```bash
export NO_COLOR=1
# or
export NUAA_NO_COLOR=1
nuaa --help
```

**Features:**

- Text-based indicators only
- Symbols instead of colors
- Pattern-based distinctions

### Dyslexia-Friendly Mode

**Extra spacing and shorter lines:**

```bash
export NUAA_DYSLEXIA_FRIENDLY=1
nuaa --help
```

**Features:**

- Increased letter spacing
- 60-character line length
- Sans-serif font recommendation
- No justified text

---

## Troubleshooting

### Arrow Keys Don't Work

**Problem**: Arrow keys print characters like `^[[A`

**Solution**:

1. Check your terminal emulator supports ANSI escape codes
2. Try Vim-style navigation (`j`/`k`) instead
3. Use `Ctrl+N`/`Ctrl+P` as alternatives

### Tab Key Doesn't Navigate

**Problem**: Tab key types a tab character instead of navigating

**Solution**:

1. Tab only works in multi-field forms
2. In menus, use arrow keys or `j`/`k`
3. In single text inputs, Tab has no special function

### Screen Reader Reads Too Much

**Problem**: Screen reader reads formatting codes or extra text

**Solution**:

1. Enable screen reader mode: `export NUAA_SCREEN_READER=1`
2. Use "read by line" instead of "read all"
3. Configure screen reader to ignore certain patterns

### Shortcuts Conflict with Terminal

**Problem**: Shortcuts are intercepted by terminal emulator

**Solution**:

1. Disable terminal-level shortcuts for those keys
2. Use alternative shortcuts (e.g., `j`/`k` instead of arrows)
3. Remap terminal shortcuts in terminal settings

### Can't Cancel Interactive Prompts

**Problem**: `Ctrl+C` or `Esc` don't work

**Solution**:

1. Try `Ctrl+D` (EOF)
2. Check if terminal has "Ctrl+C" disabled
3. Try clicking terminal and pressing shortcut again
4. Force quit terminal if necessary

---

## Keyboard-Only Workflow Example

**Complete workflow without mouse:**

```bash
# 1. Launch CLI
nuaa init my-project

# 2. Navigate menu with arrow keys
↓ ↓ ↓ (move to desired AI assistant)
Enter (select)

# 3. Interactive onboarding
nuaa onboard
↓ (navigate options)
Enter (select)
Type: "My Project Name"
Enter (confirm)

# 4. Use commands
nuaa design "Peer Support Program" "people experiencing homelessness" "12 months"

# 5. Get help
nuaa --help
? (context help)

# 6. Cancel anytime
Ctrl+C or Esc
```

---

## Quick Reference Card

**Print this section for easy reference:**

```
┌─────────────────────────────────────────────┐
│       NUAA CLI Keyboard Quick Reference     │
├─────────────────────────────────────────────┤
│ GLOBAL                                      │
│  Ctrl+C ........ Exit/Cancel               │
│  ? ............. Help                       │
│  Esc ........... Go Back                    │
│                                             │
│ NAVIGATION                                  │
│  ↑/k ........... Up                         │
│  ↓/j ........... Down                       │
│  Enter ......... Select                     │
│  Tab ........... Next Field                 │
│                                             │
│ EDITING                                     │
│  Ctrl+A ........ Start of Line              │
│  Ctrl+E ........ End of Line                │
│  Ctrl+K ........ Delete to End              │
│  Ctrl+W ........ Delete Word                │
│                                             │
│ ACCESSIBILITY                               │
│  NUAA_SCREEN_READER=1 .. Screen Reader Mode │
│  NUAA_HIGH_CONTRAST=1 .. High Contrast      │
│  NO_COLOR=1 ............ No Color Mode      │
│  NUAA_SIMPLE_MODE=1 .... Simple Mode        │
└─────────────────────────────────────────────┘
```

---

## Additional Resources

- **Accessibility Guidelines**: `nuaa-kit/accessibility-guidelines.md`
- **Onboarding Wizard**: `nuaa onboard`
- **Screen Reader Guide**: `docs/accessibility/screen-reader-guide.md`
- **Support**: https://github.com/zophiezlan/nuaa-cli/issues

---

**Questions?** Open an issue with the `accessibility` label.

**Making NUAA CLI accessible for everyone! ♿**
