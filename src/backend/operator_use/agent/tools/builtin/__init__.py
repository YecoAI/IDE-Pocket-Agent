from operator_use.agent.tools.builtin.filesystem import read_file, write_file, edit_file, list_dir
from operator_use.agent.tools.builtin.patch import patch_file
from operator_use.agent.tools.builtin.terminal import terminal

AGENT_TOOLS = [
    read_file,
    write_file,
    edit_file,
    list_dir,
    patch_file,
    terminal,
]

NON_AGENT_TOOLS = []
CLI_TOOLS = AGENT_TOOLS
