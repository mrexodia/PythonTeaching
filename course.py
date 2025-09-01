import os
import ast
import sys
import traceback

class CourseChecker(ast.NodeVisitor):
    def __init__(self):
        self.errors = []

    def report_error(self, line: int, message: str):
        self.errors.append((line, message))

class ForElseChecker(CourseChecker):
    def visit_For(self, node):
        if node.orelse:
            self.report_error(node.orelse[0].lineno - 1, "Found for-else construct")
        self.generic_visit(node)

class WalrusChecker(CourseChecker):
    def visit_NamedExpr(self, node):
        self.report_error(node.lineno, "Found walrus (:=) operator")
        self.generic_visit(node)

class DefaultParamChecker(CourseChecker):
   def visit_FunctionDef(self, node):
       self._check_defaults(node)
       self.generic_visit(node)

   def visit_AsyncFunctionDef(self, node):
       self._check_defaults(node)
       self.generic_visit(node)

   def _check_defaults(self, node):
       args_with_defaults = node.args.args[-len(node.args.defaults):] if node.args.defaults else []
       for arg, default in zip(args_with_defaults, node.args.defaults):
           if not self._is_basic_type(default):
               self.report_error(default.lineno, f"Parameter '{arg.arg}' has non-basic type as default")

   def _is_basic_type(self, node):
       if isinstance(node, ast.Constant):
           return isinstance(node.value, (int, bool, str))
       elif isinstance(node, ast.Num):
           return isinstance(node.n, (int, float))
       elif isinstance(node, ast.Str):
           return True
       elif isinstance(node, ast.NameConstant):
           return node.value in (True, False, None)
       return False

def check_file(filename: str):
    with open(filename, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename)

    failed = False
    for name, obj in globals().items():
        if isinstance(obj, type) and issubclass(obj, CourseChecker) and obj is not CourseChecker:
            checker = obj()
            checker.visit(tree)
            for line, message in checker.errors:
                print(f"  File \"{filename}\", line {line}, in <module>")
                print(f"CourseError: {message}")
                failed = True

    if failed:
        sys.exit(1)

files = [frame.filename for frame in traceback.extract_stack()[:-1] if os.path.exists(frame.filename)]
for file in files:
    check_file(file)
