import json
from pathlib import Path


LICENSE_PARAGRAPHS = (
    "ExtPicknPlace exports custom formatted pick and place fabrication data.",
    "Copyright (C) 2026 Heronitec Solutions GmbH",
    (
        "This program is free software: you can redistribute it and/or modify "
        "it under the terms of the GNU General Public License as published by "
        "the Free Software Foundation, either version 3 of the License, or "
        "(at your option) any later version."
    ),
    (
        "This program is distributed in the hope that it will be useful, "
        "but WITHOUT ANY WARRANTY; without even the implied warranty of "
        "MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the "
        "GNU General Public License for more details."
    ),
    (
        "You should have received a copy of the GNU General Public License "
        "along with this program. If not, see"
    ),
)

GPL_URL = "https://www.gnu.org/licenses/"

CONTACT = (
    ("Heronitec Solutions GmbH", None),
    ("Kreuzdelle 18", None),
    ("63872 Heimbuchenthal", None),
    ("Germany", None),
    ("info@heronitec-solutions.de", "mailto:info@heronitec-solutions.de"),
    (
        "https://github.com/heronitec-solutions/extpicknplace",
        "https://github.com/heronitec-solutions/extpicknplace",
    ),
)


def plugin_version():
    try:
        meta_path = Path(__file__).resolve().parent / "metadata.json"
        with open(meta_path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
        return data["versions"][0]["version"]
    except Exception:
        return ""


def _show(value):
    if value is None or value == "":
        return "—"
    return str(value)


def version_fields(plugin, kicad):
    """Plugin release and the KiCad version it is running in."""
    return (
        ("Plugin", _show(plugin)),
        ("KiCad", _show(kicad)),
    )
