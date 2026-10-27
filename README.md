# Software Engineering

This repository contains the results of the Software Engineering module at [Hochschule Karlsruhe (HKA)](https://www.h-ka.de).

## Library Skills

[Library Skills](https://github.com/tiangolo/library-skills) copies the agent skills shipped with FastAPI into `.agents/skills` and `.claude/skills`. Both are ignored by Git, so run this after `uv sync`:

```powershell
uvx library-skills --all --claude --copy --yes
```

`--copy` is needed because symlinks on Windows require Developer Mode. After updating FastAPI, delete both folders and run the command again.
