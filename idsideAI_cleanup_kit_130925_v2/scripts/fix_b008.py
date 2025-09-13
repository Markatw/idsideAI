"""
Auto-fix B008 patterns across a codebase.
- Rewrites mutable or call expression defaults to None-sentinel pattern.
- Only touches .py files.
- Creates a backup file with .bak suffix for each modified file.
Usage:
    python scripts/fix_b008.py .
"""
import ast
import sys
from pathlib import Path
from typing import List

class B008Rewriter(ast.NodeTransformer):
    def __init__(self):
        super().__init__()
        self.changed = False

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self._rewrite_defaults(node)
        return self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        self._rewrite_defaults(node)
        return self.generic_visit(node)

    def _is_mutable_or_call(self, default: ast.AST) -> bool:
        return isinstance(default, (ast.List, ast.Dict, ast.Set, ast.Call))

    def _rewrite_defaults(self, node):
        if not node.args.defaults:
            return
        new_defaults = []
        param_names: List[str] = []
        for arg in node.args.args[-len(node.args.defaults):]:
            param_names.append(arg.arg)

        # Map param -> default
        pairs = list(zip(param_names, node.args.defaults))
        sentinel_params = [name for name, d in pairs if self._is_mutable_or_call(d)]
        if not sentinel_params:
            return

        for name, d in pairs:
            if self._is_mutable_or_call(d):
                new_defaults.append(ast.Constant(value=None))
                self.changed = True
            else:
                new_defaults.append(d)

        node.args.defaults = new_defaults

        # Ensure body has the sentinel initializers at top
        inits = []
        for name, d in pairs:
            if self._is_mutable_or_call(d):
                # if name is None: name = <original>
                test = ast.Compare(
                    left=ast.Name(id=name, ctx=ast.Load()),
                    ops=[ast.Is()],
                    comparators=[ast.Constant(value=None)],
                )
                assign = ast.Assign(
                    targets=[ast.Name(id=name, ctx=ast.Store())],
                    value=d,
                    type_comment=None,
                )
                stmt = ast.If(test=test, body=[assign], orelse=[])
                inits.append(stmt)

        node.body = inits + node.body

def process_file(path: Path) -> bool:
    try:
        src = path.read_text(encoding="utf-8")
    except Exception:
        return False
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return False
    rewriter = B008Rewriter()
    new_tree = rewriter.visit(tree)
    if rewriter.changed:
        import astor  # type: ignore
        try:
            new_src = astor.to_source(new_tree)
        except Exception:
            # Fallback: keep formatting via ast.unparse if available (Py3.9+)
            try:
                new_src = ast.unparse(new_tree)  # type: ignore[attr-defined]
            except Exception:
                return False
        backup = path.with_suffix(path.suffix + ".bak")
        backup.write_text(src, encoding="utf-8")
        path.write_text(new_src, encoding="utf-8")
        return True
    return False

def main():
    try:
        base = Path(sys.argv[1])
    except IndexError:
        base = Path(".")
    changed = 0
    for p in base.rglob("*.py"):
        if any(seg.startswith(".") for seg in p.parts):
            continue
        if p.name == "fix_b008.py":
            continue
        if process_file(p):
            changed += 1
    print(f"[fix_b008] Modified files: {changed}")

if __name__ == "__main__":
    main()