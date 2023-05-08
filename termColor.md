### termcolor

Demo
To see demo output, run:

```
import termcolor
termcolor.demo()
```

Example

```
import sys

from termcolor import colored, cprint

text = colored("Hello, World!", "red", attrs=["reverse", "blink"])
print(text)
cprint("Hello, World!", "green", "on_red")

print_red_on_cyan = lambda x: cprint(x, "red", "on_cyan")
print_red_on_cyan("Hello, World!")
print_red_on_cyan("Hello, Universe!")

for i in range(10):
    cprint(i, "magenta", end=" ")

cprint("Attention!", "red", attrs=["bold"], file=sys.stderr)
```


| Text colors     | Text highlights    | Attributes  |
| ----------------- | -------------------- | ------------- |
| `black`         | `on_black`         | `bold`      |
| -               | -                  | -           |
| `red`           | `on_red`           | `dark`      |
| `green`         | `on_green`         | `underline` |
| `yellow`        | `on_yellow`        | `blink`     |
| `blue`          | `on_blue`          | `reverse`   |
| `magenta`       | `on_magenta`       | `concealed` |
| `cyan`          | `on_cyan`          |             |
| `white`         | `on_white`         |             |
| `light_grey`    | `on_light_grey`    |             |
| `dark_grey`     | `on_dark_grey`     |             |
| `light_red`     | `on_light_red`     |             |
| `light_green`   | `on_light_green`   |             |
| `light_yellow`  | `on_light_yellow`  |             |
| `light_blue`    | `on_light_blue`    |             |
| `light_magenta` | `on_light_magenta` |             |
| `light_cyan`    | `on_light_cyan`    |             |
