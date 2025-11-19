"""
Interactive onboarding wizard for NUAA CLI.

Provides a beginner-friendly setup experience with accessibility options.
"""

import typer
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm

from ..i18n import get_available_languages, set_language
from ..accessibility import get_config, OutputMode, set_output_mode

app = typer.Typer()
console = Console()


def onboard_command(
    skip_accessibility: bool = typer.Option(
        False, "--skip-accessibility", help="Skip accessibility setup"
    ),
    skip_language: bool = typer.Option(False, "--skip-language", help="Skip language selection"),
) -> None:
    """Interactive onboarding wizard for new NUAA CLI users.

    This command launches a friendly, step-by-step setup wizard that helps new users
    configure the NUAA CLI for their specific needs, preferences, and context. The
    onboarding process ensures all users can access NUAA's tools effectively,
    regardless of technical background, accessibility requirements, or language.

    The wizard guides users through:
    - **Accessibility Preferences**: Screen reader support, visual modes (high contrast,
      no color, dyslexia-friendly), simple mode for cognitive accessibility
    - **Language Selection**: Choose from available languages for CLI output and
      documentation (supports internationalization)
    - **Skill Level Assessment**: Self-identify as beginner, intermediate, or advanced
      to receive appropriate guidance, examples, and documentation depth
    - **Learning Style**: Select preferred learning approach (visual, text, hands-on,
      or mixed) to customize tutorial recommendations
    - **AI Assistant Selection**: Specify which AI assistant you'll use (Claude Code,
      GitHub Copilot, Cursor, etc.) for tailored integration tips
    - **Next Steps Guidance**: Customized recommendations for first commands, resources,
      and learning paths based on your configuration

    The wizard is interactive, allowing you to exit at any time (Ctrl+C) and rerun
    whenever you need to adjust settings. All preferences are saved to your local
    configuration, persisting across CLI sessions.

    NUAA's onboarding emphasizes inclusivity and accessibility, ensuring the CLI
    works for everyone - including people with disabilities, those new to command-line
    tools, and users from diverse linguistic and cultural backgrounds.

    Args:
        skip_accessibility: If True, skips the accessibility setup section and proceeds
            directly to language selection. Default is False. Useful for users who
            have already configured accessibility or are re-running the wizard.
        skip_language: If True, skips language selection and proceeds to skill level
            assessment. Default is False. Useful when re-running the wizard to update
            other preferences without changing language.

    Raises:
        typer.Exit: Not explicitly raised - users can exit gracefully with Ctrl+C at
            any prompt. Configuration errors are handled with friendly error messages.

    Examples:
        Run full onboarding wizard (first-time setup):
            $ nuaa onboard

        Re-run wizard but skip accessibility (already configured):
            $ nuaa onboard --skip-accessibility

        Update settings but keep existing language:
            $ nuaa onboard --skip-language

        Quick re-run skipping both accessibility and language:
            $ nuaa onboard --skip-accessibility --skip-language
    """
    console.clear()

    # Welcome message
    console.print(
        Panel.fit(
            "[bold green]Welcome to NUAA Project Kit![/bold green]\n\n"
            "This wizard will help you get started.\n"
            "We'll ask a few questions to customize your experience.\n\n"
            "[dim]You can exit anytime by pressing Ctrl+C[/dim]",
            title="🌱 NUAA Onboarding",
            border_style="green",
        )
    )
    console.print()

    # Step 1: Accessibility preferences
    if not skip_accessibility:
        setup_accessibility()

    # Step 2: Language selection
    if not skip_language:
        setup_language()

    # Step 3: Skill level assessment
    skill_level = assess_skill_level()

    # Step 4: Learning path selection
    learning_style = select_learning_path()

    # Step 5: AI assistant setup
    ai_assistant = select_ai_assistant()

    # Step 6: Summary and next steps
    show_summary(skill_level, learning_style, ai_assistant)


def setup_accessibility() -> None:
    """Set up accessibility preferences."""
    console.print("[bold]Step 1: Accessibility Preferences[/bold]\n")

    console.print("NUAA CLI works for everyone! Let's customize the interface for your needs.\n")

    # Screen reader
    use_screen_reader = Confirm.ask(
        "Do you use a screen reader (NVDA, JAWS, VoiceOver, Orca)?", default=False
    )

    if use_screen_reader:
        set_output_mode(OutputMode.SCREEN_READER)
        console.print(
            "[green]✓ Screen reader mode enabled - output optimized for clear announcements[/green]\n"
        )

    # Visual preferences
    if not use_screen_reader:
        console.print("\n[bold]Visual Preferences:[/bold]")
        console.print("1. Standard (default colors and formatting)")
        console.print("2. High contrast (enhanced visibility)")
        console.print("3. No color (for color blindness)")
        console.print("4. Dyslexia-friendly (extra spacing, shorter lines)")

        visual_choice = Prompt.ask(
            "Choose your preferred mode", choices=["1", "2", "3", "4"], default="1"
        )

        mode_map = {
            "1": OutputMode.STANDARD,
            "2": OutputMode.HIGH_CONTRAST,
            "3": OutputMode.NO_COLOR,
            "4": OutputMode.DYSLEXIA_FRIENDLY,
        }

        set_output_mode(mode_map[visual_choice])
        console.print("[green]✓ Visual mode set[/green]\n")

    # Simple mode (cognitive accessibility)
    use_simple_mode = Confirm.ask(
        "Would you like simple mode? (one question at a time, clear instructions)",
        default=False,
    )

    if use_simple_mode:
        config = get_config()
        config.simple_mode = True
        console.print("[green]✓ Simple mode enabled[/green]\n")

    console.print("[dim]Press Enter to continue...[/dim]")
    input()


def setup_language() -> None:
    """Set up language preference."""
    console.print("[bold]Step 2: Language Selection[/bold]\n")

    languages = get_available_languages()

    console.print("Available languages:")
    lang_list = list(languages.items())
    for i, (code, name) in enumerate(lang_list, start=1):
        console.print(f"{i}. {name} ({code})")

    console.print()

    choice = Prompt.ask(
        "Choose your preferred language (number)",
        choices=[str(i) for i in range(1, len(lang_list) + 1)],
        default="1",
    )

    selected_lang_code = lang_list[int(choice) - 1][0]
    set_language(selected_lang_code)

    console.print(f"[green]✓ Language set to {languages[selected_lang_code]}[/green]\n")
    console.print("[dim]Press Enter to continue...[/dim]")
    input()


def assess_skill_level() -> str:
    """Assess user's technical skill level."""
    console.print("[bold]Step 3: Skill Level Assessment[/bold]\n")

    console.print("This helps us provide appropriate guidance and examples.\n")

    console.print("[bold]Which best describes you?[/bold]")
    console.print("1. Beginner - New to command-line tools and AI assistants")
    console.print("2. Intermediate - Comfortable with basic commands, learning advanced features")
    console.print("3. Advanced - Experienced with CLI tools and want full customization")

    choice = Prompt.ask("Your skill level", choices=["1", "2", "3"], default="1")

    skill_map = {"1": "beginner", "2": "intermediate", "3": "advanced"}
    skill_level = skill_map[choice]

    console.print(f"[green]✓ Skill level: {skill_level.capitalize()}[/green]\n")

    return skill_level


def select_learning_path() -> str:
    """Select preferred learning style."""
    console.print("[bold]Step 4: Learning Style[/bold]\n")

    console.print("[bold]How do you prefer to learn?[/bold]")
    console.print("1. Visual - Diagrams, screenshots, video tutorials")
    console.print("2. Text - Written guides, documentation, examples")
    console.print("3. Hands-on - Interactive tutorials, try things yourself")
    console.print("4. Mixed - Combination of all approaches")

    choice = Prompt.ask("Your learning style", choices=["1", "2", "3", "4"], default="3")

    style_map = {"1": "visual", "2": "text", "3": "hands-on", "4": "mixed"}
    learning_style = style_map[choice]

    console.print(f"[green]✓ Learning style: {learning_style.capitalize()}[/green]\n")

    return learning_style


def select_ai_assistant() -> str:
    """Select AI assistant preference."""
    console.print("[bold]Step 5: AI Assistant[/bold]\n")

    console.print("NUAA CLI works with many AI assistants. Which one will you use?\n")

    console.print("Popular options:")
    console.print("1. Claude Code (Anthropic)")
    console.print("2. GitHub Copilot")
    console.print("3. Cursor")
    console.print("4. Other / Not sure yet")

    choice = Prompt.ask("Your AI assistant", choices=["1", "2", "3", "4"], default="1")

    assistant_map = {
        "1": "Claude Code",
        "2": "GitHub Copilot",
        "3": "Cursor",
        "4": "Other",
    }

    ai_assistant = assistant_map[choice]

    console.print(f"[green]✓ AI assistant: {ai_assistant}[/green]\n")

    return ai_assistant


def show_summary(skill_level: str, learning_style: str, ai_assistant: str) -> None:
    """Show setup summary and next steps."""
    console.print("\n[bold green]🎉 Setup Complete![/bold green]\n")

    console.print(
        Panel.fit(
            f"[bold]Your Configuration:[/bold]\n\n"
            f"Skill Level: {skill_level.capitalize()}\n"
            f"Learning Style: {learning_style.capitalize()}\n"
            f"AI Assistant: {ai_assistant}\n",
            title="Summary",
            border_style="green",
        )
    )

    console.print("\n[bold]Next Steps:[/bold]\n")

    if skill_level == "beginner":
        console.print("1. Read the Quick Start Guide:")
        console.print("   [cyan]cat nuaa-kit/QUICKSTART.md[/cyan]\n")
        console.print("2. Try your first command:")
        console.print("   [cyan]nuaa init my-first-project[/cyan]\n")
        console.print("3. Get help anytime:")
        console.print("   [cyan]nuaa --help[/cyan]\n")
    elif skill_level == "intermediate":
        console.print("1. Explore available commands:")
        console.print("   [cyan]nuaa --help[/cyan]\n")
        console.print("2. Review the workflow diagram:")
        console.print("   [cyan]cat nuaa-kit/docs/workflow-diagram.md[/cyan]\n")
        console.print("3. Try creating a program design:")
        console.print("   [cyan]/nuaa.design[/cyan] (in your AI assistant)\n")
    else:
        console.print("1. Review advanced features:")
        console.print("   [cyan]cat nuaa-kit/README.md[/cyan]\n")
        console.print("2. Check out customization options:")
        console.print("   [cyan]cat docs/nuaa-cli-extension.md[/cyan]\n")
        console.print("3. Contribute to the project:")
        console.print("   [cyan]cat CONTRIBUTING.md[/cyan]\n")

    console.print("\n[bold]Resources:[/bold]")
    console.print("- Documentation: [cyan]docs/[/cyan]")
    console.print("- Templates: [cyan]nuaa-kit/templates/[/cyan]")
    console.print("- Examples: [cyan]nuaa-kit/examples/[/cyan]")
    console.print("- Support: [cyan]https://github.com/zophiezlan/nuaa-cli/issues[/cyan]")

    console.print("\n[dim]Tip: You can run this wizard again anytime with: nuaa onboard[/dim]\n")
