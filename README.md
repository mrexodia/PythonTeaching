# Python For Teaching

Just a simple example for the discussion [Pyret: A programming language for programming education](https://lobste.rs/s/uiekig/pyret_programming_language_for). It shows a simple Python module that checks the AST of the importing module for constructs that often confuse beginners.

Currently this is done by adding `import course` to the beginning of your file, but this can be automated in a few ways:
- `sitecustomize.py`
- `usercustomize.py`
- `.pth` files
- `PYTHONSTARTUP` environment variable

The [hatch-autorun](https://github.com/ofek/hatch-autorun) package wraps this and you could publish a `course-checker` package that will automatically install the checker in the student's environment.

## Detect mutable default parameters

```py
import course

def foo(x: int, y: str = "hello"):
    print(x, y)

def bar(x: int, y = [1, 2, 3]): # CourseError: Parameter 'y' has non-basic type as default
    print(x, y)
```

## Walrus operator (:=)

```py
import course
import re

if match := re.match(r"^(\d+)-(\d+)$", "12-34"): # CourseError: Found walrus (:=) operator
    # Use match
    print(match.group(1), match.group(2))
```

## For-else

```py
import course

for i in range(10):
    print(i)

    raise Exception("Something went wrong")
    if i == 9:
        print("Too big - I'm giving up!")
        break
else: # CourseError: Found for-else construct
    print("Completed successfully")
```