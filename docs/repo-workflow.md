# Repository Workflow

OASIS is the ISA source-of-truth repository. Implementation repositories should
consume a pinned OASIS version or commit.

Recommended dependency options:

- Git submodule for early development
- Git subtree for vendors that dislike submodules
- Release archive for stable versions
- CI checkout of both repositories for active co-development

Implementation README files should report:

- OASIS version or profile
- OASIS commit hash
- Implemented instruction set subset
- Compliance test status

Example:

```text
Targets: OASIS Base-16 v0.1
Spec commit: abc1234
Status: partial implementation, compliance in progress
```

## Versioning

Use explicit compatibility labels:

- `OASIS v0.1`
- `OASIS Base-16 v0.1`
- `DungV v0.1 implements partial OASIS v0.1`
- `DungV v0.2 implements full OASIS Base-16 v0.1`

Instruction status should use:

- `Specified`
- `Implemented`
- `Tested`
