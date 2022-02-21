import subprocess
from subprocess import PIPE
import json
KATEX_RENDERER = subprocess.Popen(["node", "renderer/renderer.js"], stdin=PIPE, stdout=PIPE,
                                  bufsize=1, universal_newlines=True)


def render_equation(latex, is_display):
    KATEX_RENDERER.stdin.write(f'{json.dumps({"equation": latex, "is_display": is_display})}\n')
    return json.loads(KATEX_RENDERER.stdout.readline())["html"]


if __name__ == "__main__":
    print(render_equation(r"\frac{a}{b}", True))
