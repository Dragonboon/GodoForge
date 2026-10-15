# GodoForge branding and publishing

**Project name:** GodoForge

**Tagline:** Build Godot plugins, not boilerplate.

The name is used for this *repository template*, not for addons created from it. `scripts/init_plugin.py` replaces the template's branded README with `docs/PLUGIN_README_TEMPLATE.md`, renaming the plugin identity. README links currently point to the canonical source repository URL, which remains unchanged until the maintainer explicitly renames it.

## Recommended GitHub repository settings

If you rename the repository, the suggested slug is **`godoforge`** (GitHub: `sempitern0/godoforge`). Rename the actual repository separately via GitHub Settings; GitHub provides repository redirects, but review clone remotes, CI badges and integrations afterwards.

- Description: `GodoForge — minimal Godot 4.7 plugin starter with an interactive setup wizard, practical recipes and CI.`
- Topics: `godot`, `godot-engine`, `godot4`, `gdscript`, `editor-plugin`, `plugin-template`, `gamedev`, `python`, `starter-template`
- Enable **Template repository**.
- Decide whether to make the repository public before advertising the **Use this template** button.
- Consider publishing a tagged release when the generated projects and clean-install walkthrough are manually verified.

Use releases/tags for template milestones, not as the generated addons' own version guarantees. Avoid marketing badges that assert unverified platform or engine compatibility.
