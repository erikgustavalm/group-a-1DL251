import os

import graphics
from color import Color


def main():
    name = os.name
    print(f"hello, world from OS='{name}'")

    gh = graphics.GraphicsHandler()
    gh.display_game([Color.White, Color.Black, Color.Empty] * 10)


if __name__ == "__main__":
    main()
