import os
import sys
import importlib
import uuid

import logger_factory

from services import storage, run_service

PARENT_MODULE = "exec_env"


class Agent:
    def __init__(self, agent_definition: dict):
        self.logger = logger_factory.get_logger(__name__)
        self.agent_id = uuid.uuid4()
        self.module_name = f"{PARENT_MODULE}.{str(self.agent_id)}"
        self.module_path = f"{PARENT_MODULE}/{str(self.agent_id)}.py"
        self.skills = agent_definition.get("skills")
        self.code = "from skill_decorator import skill"

    def query(self, query: str):
        result = None
        try:
            for skill in self.skills:
                self._load_skill(skill.get("path"))
            self._flush()
            my_module = importlib.import_module(self.module_name)
            result = run_service.run(my_module, query)
            del sys.modules[self.module_name]
            self._delete_module_file()
            return result
        except Exception:
            self.logger.error("Unable to query agent.")
        return result

    def _load_skill(self, skill_name: str):
        skill = storage.read_skill(skill_name)
        self._add_to_module(skill.get("code"))

    def _add_to_module(self, code: str):
        self.code = self.code + f"\n{code}"

    def _flush(self):
        with open(self.module_path, "w+") as f:
            f.write(self.code)

    def _delete_module_file(self):
        if os.path.exists(self.module_path):
            os.remove(self.module_path)
        else:
            self.logger.error("The file does not exist")
