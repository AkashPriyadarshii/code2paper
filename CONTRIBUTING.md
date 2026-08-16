# Contributing to code2paper

Thank you for your interest in contributing to `code2paper`!

## Guidelines
1. **Stdlib-first**: Keep `code2paper.py` lightweight with Python 3.10+ standard library. Avoid heavy dependencies.
2. **Minimal Diffs**: Keep code additions focused and concise (Ponytail principles).

## Workflow
1. Fork and clone the repository.
2. Create your feature branch (`git checkout -b feature/amazing-feature`).
3. Verify your changes manually or via unit tests:
   ```bash
   python code2paper.py . --keep-typst
   ```
4. Commit your changes following conventional commits (`feat: add custom template support`).
5. Push to the branch and submit a Pull Request.
