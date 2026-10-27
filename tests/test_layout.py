"""Structural checks: every file the crew references exists and is well-formed."""
import json
import re

import pytest

from conftest import ROOT

AGENTS = sorted((ROOT / "agents").glob("*.md"))
COMMANDS = sorted((ROOT / "commands").glob("*.md"))


def frontmatter(path):
    m = re.match(r"---\n(.*?)\n---\n", path.read_text(), re.S)
    assert m, f"{path.name}: missing frontmatter"
    return dict(line.split(":", 1) for line in m.group(1).splitlines() if ":" in line)


@pytest.mark.parametrize("path", AGENTS, ids=lambda p: p.name)
def test_agent_frontmatter(path):
    fm = frontmatter(path)
    assert fm["name"].strip() == path.stem
    assert len(fm["description"].strip()) > 40
    assert fm.get("tools")


@pytest.mark.parametrize("path", COMMANDS, ids=lambda p: p.name)
def test_command_frontmatter(path):
    assert frontmatter(path).get("description")


@pytest.mark.parametrize("path", AGENTS + COMMANDS, ids=lambda p: p.name)
def test_references_resolve(path):
    text = path.read_text()
    for agent in re.findall(r"`build-crew:([a-z-]+)`", text):
        assert (ROOT / "agents" / f"{agent}.md").exists(), f"{path.name} references missing agent {agent}"
    for gate in re.findall(r"gates/([a-z_]+\.py)", text):
        assert (ROOT / "gates" / gate).exists(), f"{path.name} references missing gate {gate}"
    # shell variables don't survive between Claude's Bash calls: gates must be called by full path
    for call in re.findall(r"python3 \"?([^\s\"`]+\.py)", text):
        assert call.startswith("${CLAUDE_PLUGIN_ROOT}/gates/"), f"{path.name}: gate called as {call}"


def test_non_editing_agents_have_no_write_tools():
    for name in ("pr-reviewer", "researcher", "deployer"):
        tools = frontmatter(ROOT / "agents" / f"{name}.md")["tools"]
        assert "Write" not in tools and "Edit" not in tools, f"{name} must be read-only"


def test_plugin_manifests():
    plugin = json.loads((ROOT / ".claude-plugin/plugin.json").read_text())
    market = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text())
    assert plugin["name"] == "build-crew" == market["plugins"][0]["name"]
    hooks = json.loads((ROOT / "hooks/hooks.json").read_text())["hooks"]
    for entries in hooks.values():
        for e in entries:
            for h in e["hooks"]:
                rel = re.search(r"/(hooks/[\w.]+)", h["command"]).group(1)
                assert (ROOT / rel).exists()
