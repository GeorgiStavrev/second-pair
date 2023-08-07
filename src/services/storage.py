from typing import List

import json
from os import walk


SKILLS_TABLE = "skills"
SKILLS_FILE_EXT = "skill.json"
AGENTS_TABLE = "agents"
AGENTS_FILE_EXT = "agent.json"

ALLOWED_SKILL_EXTENSIONS = [
    f".py.{SKILLS_FILE_EXT}",
    f".{SKILLS_FILE_EXT}",
    f".{AGENTS_FILE_EXT}"
]


def get_extension(filename: str) -> str:
    ext = ".".join(filename.split(".")[1:])
    return f".{ext}"


def read_from_file(table: str, filename: str) -> dict:
    with open(f"./db/{table}/{filename}", "r") as f:
        skill = json.loads(f.read())
    return skill


def read(table: str) -> List[str]:
    filenames = next(walk(f"./db/{table}"), (None, None, []))[2]
    filenames = [fn for fn in filenames if get_extension(
        fn) in ALLOWED_SKILL_EXTENSIONS]
    items = [read_from_file(table, fn) for fn in filenames]
    return items


def read_item(table: str, item_name: str) -> dict:
    try:
        with open(f"./db/{table}/{item_name}", "r") as f:
            return json.loads(f.read())
    except Exception:
        return None


def write(table: str, item: dict, name: str):
    with open(f"./db/{table}/{name}", "w") as f:
        f.write(json.dumps(item))


def read_skills() -> List[str]:
    return read(SKILLS_TABLE)


def read_skill(skill_name: str) -> List[str]:
    return read_item(SKILLS_TABLE, skill_name)


def write_skill(name: str, description: str, code: str):
    item = {
        "name": name,
        "description": description,
        "code": code
    }
    write(SKILLS_TABLE, item, f"{name}.py.{SKILLS_FILE_EXT}")


def read_agents():
    return read(AGENTS_TABLE)


def read_agent(agent_name: str) -> dict:
    filename = f"{agent_name}.{AGENTS_FILE_EXT}"
    return read_item(AGENTS_TABLE, filename)


def write_agent(name: str, skills: List[str]):
    item = {
        "name": name,
        "skills": skills
    }
    write(AGENTS_TABLE, item, f"{name}.{AGENTS_FILE_EXT}")
