# NUAA CLI Internationalization (i18n)

This directory contains translation files for NUAA CLI in 6 languages.

## Supported Languages

- **en_AU** - English (Australia) - Default language
- **es** - Español (Spanish)
- **vi_VN** - Tiếng Việt (Vietnamese)
- **zh_CN** - 简体中文 (Simplified Chinese)
- **th_TH** - ไทย (Thai)
- **ar** - العربية (Arabic)

## Directory Structure

```
locales/
├── en_AU/LC_MESSAGES/
│   ├── nuaa_cli.po     # English (Australia) translations
│   └── nuaa_cli.mo     # Compiled translations (generated)
├── es/LC_MESSAGES/
│   ├── nuaa_cli.po     # Spanish translations
│   └── nuaa_cli.mo     # Compiled translations (generated)
├── vi_VN/LC_MESSAGES/
│   ├── nuaa_cli.po     # Vietnamese translations
│   └── nuaa_cli.mo     # Compiled translations (generated)
├── zh_CN/LC_MESSAGES/
│   ├── nuaa_cli.po     # Simplified Chinese translations
│   └── nuaa_cli.mo     # Compiled translations (generated)
├── th_TH/LC_MESSAGES/
│   ├── nuaa_cli.po     # Thai translations
│   └── nuaa_cli.mo     # Compiled translations (generated)
├── ar/LC_MESSAGES/
│   ├── nuaa_cli.po     # Arabic translations
│   └── nuaa_cli.mo     # Compiled translations (generated)
└── nuaa_cli.pot        # Translation template file
```

## Compiling Translations

### Method 1: Using msgfmt (Recommended)

If you have gettext installed:

```bash
# Compile all translations
for lang in en_AU es vi_VN zh_CN th_TH ar; do
    msgfmt locales/$lang/LC_MESSAGES/nuaa_cli.po \
           -o locales/$lang/LC_MESSAGES/nuaa_cli.mo
done
```

Or compile a single language:

```bash
msgfmt locales/es/LC_MESSAGES/nuaa_cli.po \
       -o locales/es/LC_MESSAGES/nuaa_cli.mo
```

### Method 2: Using Python Script

Run the provided compilation script:

```bash
python scripts/compile_translations.py
```

### Method 3: Install gettext

**Ubuntu/Debian:**
```bash
sudo apt-get install gettext
```

**macOS:**
```bash
brew install gettext
```

**Windows:**
Download from: https://mlocati.github.io/articles/gettext-iconv-windows.html

## Usage

The i18n module will automatically detect the system language and load the appropriate translations.

### In Python Code

```python
from nuaa_cli.i18n import _, set_language

# Use the translation function
print(_("Welcome"))  # Will print in the user's system language

# Explicitly set language
set_language("es")
print(_("Welcome"))  # Prints "Bienvenido"
```

### Setting Language via Environment Variables

```bash
# Set language to Spanish
export LANG=es.UTF-8
nuaa init

# Set language to Vietnamese
export LANG=vi_VN.UTF-8
nuaa init

# Set language to Simplified Chinese
export LANG=zh_CN.UTF-8
nuaa init
```

## Adding New Translations

### 1. Extract Translatable Strings

Run the extraction script to update the template file:

```bash
xgettext --language=Python \
         --keyword=_ \
         --output=locales/nuaa_cli.pot \
         src/nuaa_cli/**/*.py
```

### 2. Update Existing Translations

Merge new strings into existing .po files:

```bash
for lang in en_AU es vi_VN zh_CN th_TH ar; do
    msgmerge --update \
             locales/$lang/LC_MESSAGES/nuaa_cli.po \
             locales/nuaa_cli.pot
done
```

### 3. Translate the Strings

Edit the .po files and add translations for any untranslated strings.

### 4. Compile

Recompile the .mo files after making changes (see "Compiling Translations" above).

## Translation Guidelines

### Person-First Language

NUAA CLI uses person-first language to reduce stigma. When translating:

- ✅ "person who uses drugs"
- ❌ "drug user" or "addict"

- ✅ "person experiencing homelessness"
- ❌ "homeless person"

### Cultural Sensitivity

- Ensure translations respect local cultural norms
- Avoid direct literal translations that may be awkward
- Consider regional variations (e.g., Spanish varies by country)

### Technical Terms

Some terms should remain in English or use accepted technical translations:

- "MCP tools" - keep as-is or use local equivalent
- "Agent" - translate as appropriate for context
- "Template" - translate to local equivalent

### Testing Translations

1. Set the language:
   ```bash
   export LANG=es.UTF-8
   ```

2. Run NUAA CLI commands:
   ```bash
   nuaa init
   nuaa help
   ```

3. Verify that messages appear in the correct language

## Contributing Translations

We welcome contributions to improve translations!

### For Translators

1. Review the .po file for your language
2. Look for untranslated strings (marked with `msgstr ""`)
3. Add translations following the guidelines above
4. Test your translations
5. Submit a pull request

### Adding a New Language

1. Add the language code to `src/nuaa_cli/i18n/__init__.py`:
   ```python
   SUPPORTED_LANGUAGES = {
       # ... existing languages ...
       "de_DE": "Deutsch (German)",
   }
   ```

2. Create directory structure:
   ```bash
   mkdir -p locales/de_DE/LC_MESSAGES
   ```

3. Initialize the .po file:
   ```bash
   msginit --input=locales/nuaa_cli.pot \
           --output=locales/de_DE/LC_MESSAGES/nuaa_cli.po \
           --locale=de_DE
   ```

4. Translate the strings in the new .po file
5. Compile and test
6. Submit a pull request

## Translation Status

| Language | Code | Completion | Last Updated |
|----------|------|------------|--------------|
| English (Australia) | en_AU | 100% | 2025-11-25 |
| Spanish | es | 100% | 2025-11-25 |
| Vietnamese | vi_VN | 100% | 2025-11-25 |
| Simplified Chinese | zh_CN | 100% | 2025-11-25 |
| Thai | th_TH | 100% | 2025-11-25 |
| Arabic | ar | 100% | 2025-11-25 |

## Resources

- **GNU gettext**: https://www.gnu.org/software/gettext/
- **Python gettext**: https://docs.python.org/3/library/gettext.html
- **Poedit** (GUI editor): https://poedit.net/
- **Translation guidelines**: See `docs/translation-guidelines.md`

## Support

For translation questions or issues:
- Open an issue: https://github.com/zophiezlan/nuaa-cli/issues
- Tag with: `i18n`, `translation`, `localization`

## License

Translations are distributed under the same license as NUAA CLI.
