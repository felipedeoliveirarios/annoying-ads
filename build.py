#!/usr/bin/env python3
"""Empacota o Annoying Popups em um executável single-file com PyInstaller.

Descobre as bibliotecas Tcl/Tk do interpretador atual e as inclui
explicitamente. Isso é necessário para o Python gerenciado do uv, que traz
Tcl/Tk 9 e não é empacotado automaticamente pelo hook padrão do PyInstaller.
Funciona em Linux, macOS e Windows, tanto com Tcl/Tk 9 quanto 8.6.

Uso:  uv run python build.py     (ou: python build.py)
"""
import sys
from pathlib import Path

import PyInstaller.__main__

NAME = "annoying-popups"
ENTRY = "annoying_popups.py"


def tcltk_extras():
    """Args --add-data/--add-binary para embutir Tcl/Tk do interpretador atual."""
    base = Path(sys.base_prefix)
    sep = ";" if sys.platform == "win32" else ":"
    extras = []

    # Diretórios de script Tcl/Tk (identificados por init.tcl e tk.tcl).
    for marker in ("init.tcl", "tk.tcl"):
        for f in base.rglob(marker):
            d = f.parent
            extras += ["--add-data", f"{d}{sep}{d.name}"]
            break  # o primeiro match basta

    # Bibliotecas compartilhadas do Tcl/Tk (nomes variam por SO/versão).
    seen = set()
    for pat in ("libtcl*.so*", "libtk*.so*", "libtcl*.dylib", "libtk*.dylib",
                "tcl*.dll", "tk*.dll"):
        for lib in base.rglob(pat):
            if lib.is_file() and lib not in seen:
                seen.add(lib)
                extras += ["--add-binary", f"{lib}{sep}."]
    return extras


def main():
    args = [ENTRY, "--onefile", "--clean", "--noconfirm", "--name", NAME,
            # ImageTk precisa deste módulo, que o PyInstaller não detecta sozinho.
            "--hidden-import", "PIL._tkinter_finder"]
    if sys.platform == "win32":
        args.append("--windowed")  # sem janela de console no Windows
    args += tcltk_extras()
    print("PyInstaller args:", " ".join(args))
    PyInstaller.__main__.run(args)


if __name__ == "__main__":
    main()
