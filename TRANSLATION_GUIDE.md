# NUAA CLI Translation Guide

> **Note**: This guide is for **contributors** who want to help translate the NUAA CLI tool itself. If you're an **end user** looking to use NUAA for your projects, see the [README](README.md) instead.

---

**Welcome to the NUAA CLI Translation Community!**

This guide will help you contribute translations to make NUAA CLI accessible to more communities.

---

## Why Translation Matters

NUAA serves diverse communities including people who use drugs, Aboriginal and Torres Strait Islander peoples, LGBTIQ+ communities, and people from culturally and linguistically diverse backgrounds. Making our tools available in multiple languages ensures everyone can access and benefit from them.

Your contribution helps:
- Remove language barriers to important harm reduction resources
- Make peer-led programs more accessible
- Demonstrate cultural safety and respect
- Empower community members to use technology in their preferred language

---

## Supported Languages

We currently support or are working on:

| Language | Code | Status | Contributors Needed |
|----------|------|--------|-------------------|
| English (Australia) | en_AU | ✅ Complete | No |
| Vietnamese | vi_VN | 🟡 In Progress | Yes |
| Thai | th_TH | 🔴 Not Started | Yes |
| Arabic | ar | 🔴 Not Started | Yes |
| Simplified Chinese | zh_CN | 🔴 Not Started | Yes |
| Spanish | es | 🔴 Not Started | Yes |

**Don't see your language?** Open an issue to request adding it!

---

## How to Contribute Translations

### Step 1: Set Up Your Environment

1. **Fork and clone the repository:**
   ```bash
   git clone https://github.com/<your-username>/nuaa-cli.git
   cd nuaa-cli
   ```

2. **Install translation tools:**
   ```bash
   pip install babel polib
   ```

### Step 2: Choose Your Language

Navigate to the locales directory:
```bash
cd locales
```

If your language folder doesn't exist yet, create it:
```bash
mkdir -p <language_code>/LC_MESSAGES
# For example: mkdir -p vi_VN/LC_MESSAGES
```

### Step 3: Get the Translation Template

The translation template (`.pot` file) contains all the strings that need translation:

```bash
# Generate/update the translation template
python scripts/i18n/extract_strings.py
```

This creates `locales/nuaa_cli.pot` with all translatable strings.

### Step 4: Create or Update Your Translation File

**For a new language:**
```bash
msginit --input=locales/nuaa_cli.pot \
        --output=locales/<language_code>/LC_MESSAGES/nuaa_cli.po \
        --locale=<language_code>
```

**For an existing language:**
```bash
msgmerge --update \
         locales/<language_code>/LC_MESSAGES/nuaa_cli.po \
         locales/nuaa_cli.pot
```

### Step 5: Translate the Strings

Open the `.po` file in your language folder. You'll see entries like:

```po
#: src/nuaa_cli/__init__.py:45
msgid "Welcome to NUAA Project Kit"
msgstr ""
```

Add your translation in the `msgstr` field:

```po
#: src/nuaa_cli/__init__.py:45
msgid "Welcome to NUAA Project Kit"
msgstr "Chào mừng đến với Bộ công cụ Dự án NUAA"
```

**Translation Tools:**
- **Poedit** (recommended for beginners): https://poedit.net/
- **Lokalize** (for Linux/KDE users)
- **Any text editor** (for advanced users)

### Step 6: Translation Guidelines

Follow these important guidelines:

#### 1. Cultural Appropriateness
- Use culturally appropriate language for your community
- Adapt metaphors and idioms (don't translate literally)
- Consider local terminology for harm reduction concepts

#### 2. Plain Language
- Use simple, clear language
- Target reading level: Year 8-10 equivalent
- Avoid jargon and technical terms where possible

#### 3. Consistency
- Use consistent terminology throughout
- Refer to the glossary: `nuaa-kit/glossary.md`
- Key terms to keep consistent:
  - "peer-led" / "peer worker"
  - "harm reduction"
  - "people who use drugs" (never "addicts")
  - "consumer" (person with lived experience)

#### 4. Person-First Language
- Always use person-first, non-stigmatizing language
- Examples:
  - ✅ "người sử dụng ma túy" (people who use drugs)
  - ❌ "người nghiện" (addicts)

#### 5. Gender Inclusivity
- Use gender-neutral language where possible
- Include non-binary options in forms
- Respect diverse gender expressions

#### 6. Format Preservation
- Keep placeholders like `{variable}` unchanged
- Preserve newlines (`\n`) and special characters
- Maintain formatting codes (e.g., `[bold]text[/bold]`)

#### 7. Context Matters
- Read the code comments (`#:` lines) for context
- If unclear, ask for clarification in the PR
- Test your translations in the actual CLI

### Step 7: Test Your Translations

1. **Compile the translations:**
   ```bash
   msgfmt locales/<language_code>/LC_MESSAGES/nuaa_cli.po \
          -o locales/<language_code>/LC_MESSAGES/nuaa_cli.mo
   ```

2. **Set your language:**
   ```bash
   export LANGUAGE=<language_code>
   # For example: export LANGUAGE=vi_VN
   ```

3. **Run the CLI:**
   ```bash
   nuaa --help
   nuaa version
   ```

4. **Check that:**
   - Text displays correctly
   - No garbled characters
   - Formatting is preserved
   - Messages make sense in context

### Step 8: Submit Your Translation

1. **Commit your changes:**
   ```bash
   git add locales/<language_code>/
   git commit -m "Add <language_name> translation"
   ```

2. **Push to your fork:**
   ```bash
   git push origin main
   ```

3. **Create a pull request:**
   - Go to https://github.com/zophiezlan/nuaa-cli
   - Click "New Pull Request"
   - Describe your translation work
   - Mention if you're a native speaker or community member

4. **In your PR description, include:**
   - Which language you translated
   - Your connection to the community (if comfortable sharing)
   - Any cultural adaptations you made
   - Whether you'd like to be listed as a maintainer for that language

---

## Translation Priority

Not all strings are equally important. Here's the priority order:

### High Priority (Translate First)
1. Main menu and command names
2. Help messages and descriptions
3. Error messages
4. Interactive prompts
5. Success/confirmation messages

### Medium Priority
6. Documentation strings
7. Progress indicators
8. Warning messages
9. Informational messages

### Low Priority (Can Wait)
10. Debug messages
11. Developer-facing strings
12. Advanced feature descriptions

---

## Glossary of Key Terms

| English | Translation Notes |
|---------|------------------|
| peer-led | Use culturally appropriate term for community-led by people with lived experience |
| harm reduction | Evidence-based, non-judgmental approach to drug use |
| people who use drugs | NEVER translate as "addicts" or stigmatizing terms |
| consumer | Person with lived experience (in NUAA context) |
| naloxone | Opioid overdose reversal medication (may use local brand name like Narcan) |
| NSP | Needle and Syringe Program |
| BBV | Blood-borne virus (HIV, HCV) |
| stigma | Negative attitudes and discrimination |

For more terms, see: `nuaa-kit/glossary.md`

---

## Special Considerations for Different Languages

### Vietnamese (vi_VN)
- Use Southern dialect (standard in NSW Vietnamese community)
- Consider refugee background and trauma-informed language
- Use respectful forms of address

### Thai (th_TH)
- Use polite particles (ครับ/ค่ะ) appropriately
- Consider formality levels in community health context
- Respect hierarchy while maintaining peer-led approach

### Arabic (ar)
- Ensure RTL (right-to-left) text displays correctly
- Use Modern Standard Arabic for broad accessibility
- Consider cultural sensitivity around drug use topics
- Test carefully with RTL terminal/console

### Simplified Chinese (zh_CN)
- Use simplified characters (not traditional)
- Consider mainland Chinese vs. diaspora terminology preferences
- Be sensitive to stigma around drug use in Chinese communities

### Spanish (es)
- Use Latin American Spanish (not European)
- Consider which regional variant (Mexican, Colombian, etc.) based on NSW demographics
- Gender-inclusive language is important

---

## Recognition and Compensation

### Recognition:
- All translators are listed in CONTRIBUTORS.md
- Language maintainers listed in each language file
- Special thanks in release notes

### Compensation:
Following NUAA principles of fair consumer remuneration:
- **Major translation contributions** (>50% of a language): $300 honorarium
- **Language maintenance** (ongoing updates): $100 per release cycle
- **Community review sessions**: $300 per session

To receive compensation:
1. Complete your translation contribution
2. Contact maintainers with your invoice details
3. Provide your connection to NUAA community (for verification)

---

## Getting Help

### Questions About Translation?
- Open an issue: https://github.com/zophiezlan/nuaa-cli/issues
- Tag it with `translation` and `question`
- Maintainers will respond within 3 business days

### Need Context or Clarification?
- Comment on your PR with specific questions
- Join our community discussion (link in README)
- Ask in your pull request description

### Technical Issues?
- Check the troubleshooting section in README
- Ask in GitHub issues with `translation` and `bug` tags

---

## Translation Workflow Summary

```
┌─────────────────────────────────────────────┐
│ 1. Fork & Clone Repository                 │
└────────────────┬────────────────────────────┘
                 │
┌────────────────▼────────────────────────────┐
│ 2. Extract Strings (generate .pot file)    │
└────────────────┬────────────────────────────┘
                 │
┌────────────────▼────────────────────────────┐
│ 3. Create/Update .po File for Language     │
└────────────────┬────────────────────────────┘
                 │
┌────────────────▼────────────────────────────┐
│ 4. Translate Strings Following Guidelines  │
└────────────────┬────────────────────────────┘
                 │
┌────────────────▼────────────────────────────┐
│ 5. Compile .mo File & Test                 │
└────────────────┬────────────────────────────┘
                 │
┌────────────────▼────────────────────────────┐
│ 6. Submit Pull Request                     │
└────────────────┬────────────────────────────┘
                 │
┌────────────────▼────────────────────────────┐
│ 7. Review & Merge                          │
└─────────────────────────────────────────────┘
```

---

## Thank You!

Your translation work makes NUAA CLI accessible to more people and demonstrates our commitment to cultural safety and inclusivity. Every string you translate helps someone access important harm reduction resources in their own language.

**Together, we're building technology that serves all our communities.**

---

## Resources

- **NUAA Accessibility Guidelines**: `nuaa-kit/accessibility-guidelines.md`
- **NUAA Glossary**: `nuaa-kit/glossary.md`
- **Code of Conduct**: `CODE_OF_CONDUCT.md`
- **Gettext Documentation**: https://www.gnu.org/software/gettext/manual/
- **Poedit Tutorial**: https://poedit.net/support

---

For questions or support, contact the maintainers or open an issue.

**Building accessible, inclusive tools together! 🌍**
