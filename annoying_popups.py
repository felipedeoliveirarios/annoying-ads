#!/usr/bin/env python3
"""
Annoying Popups - trollagem inofensiva estilo "computador com vírus".

Exibe pop-ups de imagens (anúncios falsos + memes) em posições e monitores
aleatórios. NÃO toca em arquivos, não altera configurações do sistema, não
persiste após fechar. Kill switch: segure ESC por 5 segundos para fechar tudo.

Requisitos: Python 3.8+, tkinter, pynput, Pillow. Opcional: screeninfo.
"""
from __future__ import annotations

import argparse
import os
import random
import sys
import threading
import time
from pathlib import Path

# Quando empacotado (PyInstaller), o Tcl/Tk 9 embutido precisa que
# TCL_LIBRARY/TK_LIBRARY apontem para os scripts dentro do bundle, senão o
# import de tkinter falha. Precisa ser feito ANTES de importar tkinter.
if getattr(sys, "frozen", False):
    _meipass = Path(getattr(sys, "_MEIPASS", Path(sys.executable).parent))
    for _var, _cands in (("TCL_LIBRARY", ("tcl9.0", "tcl8.6")),
                         ("TK_LIBRARY", ("tk9.0", "tk8.6"))):
        for _c in _cands:
            if (_meipass / _c).is_dir():
                os.environ[_var] = str(_meipass / _c)
                break

import tkinter as tk

# --- dependências opcionais -------------------------------------------------
try:
    from screeninfo import get_monitors
except Exception:  # pragma: no cover - fallback
    get_monitors = None

try:
    from PIL import Image, ImageTk
except Exception:  # pragma: no cover - memes viram opcionais
    Image = None
    ImageTk = None

# pynput é obrigatório: é ele que garante o kill switch global (ESC 5s)
try:
    from pynput import keyboard
except Exception:
    keyboard = None


# Diretório base: ao lado do executável quando empacotado (PyInstaller onefile),
# senão ao lado deste .py. Garante que a pasta memes/ seja encontrada nos dois casos.
if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys.executable).parent
else:
    BASE_DIR = Path(__file__).parent


# --- constantes -------------------------------------------------------------
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp"}

HINT_TEXT = "segure ESC por 5s p/ fechar tudo"


def get_screens():
    """Retorna lista de (x, y, w, h) para cada monitor."""
    if get_monitors:
        try:
            mons = get_monitors()
            if mons:
                return [(m.x, m.y, m.width, m.height) for m in mons]
        except Exception:
            pass
    # fallback: monitor único (usa a tela do tkinter)
    root = tk._get_default_root() if hasattr(tk, "_get_default_root") else tk._default_root
    if root is not None:
        return [(0, 0, root.winfo_screenwidth(), root.winfo_screenheight())]
    return [(0, 0, 1920, 1080)]


class PrankApp:
    def __init__(self, args):
        self.args = args
        self.root = tk.Tk()
        self.root.withdraw()  # a janela raiz fica invisível
        self.screens = get_screens()
        self.images = self._load_images()
        self.popups = []
        self.start_time = time.time()
        self.should_quit = False

        # estado do kill switch (compartilhado com a thread do pynput)
        self.lock = threading.Lock()
        self.esc_down = False
        self.esc_press_start = 0.0
        self.last_press = 0.0

        self.overlay = None  # overlay de contagem regressiva

    # -- imagens (anúncios + memes) -----------------------------------------
    def _load_images(self):
        if Image is None:
            return []
        imgs = []
        for d in (self.args.ads_dir, self.args.memes_dir):
            p = Path(d)
            if p.is_dir():
                imgs += [f for f in p.iterdir() if f.suffix.lower() in IMAGE_EXTS]
        return imgs

    # -- criação de pop-ups --------------------------------------------------
    def _place_on_random_screen(self, win, w, h):
        sx, sy, sw, sh = random.choice(self.screens)
        x = sx + random.randint(0, max(0, sw - w))
        y = sy + random.randint(0, max(0, sh - h))
        win.geometry(f"{w}x{h}+{x}+{y}")

    def make_popup(self):
        if self.should_quit or len(self.popups) >= self.args.max_popups:
            return
        win = tk.Toplevel(self.root)
        win.overrideredirect(True)          # sem barra de título -> cara de anúncio
        win.attributes("-topmost", True)
        win.configure(bg="#000000")
        self.popups.append(win)

        self._build_image(win)

        if not self.args.no_sound and random.random() < 0.35:
            try:
                win.bell()
            except Exception:
                pass

    def _close_popup(self, win, multiply=0):
        if win in self.popups:
            self.popups.remove(win)
        try:
            win.destroy()
        except Exception:
            pass
        # comportamento clássico: fechar um anúncio abre outros
        for _ in range(multiply):
            self.root.after(random.randint(80, 400), self.make_popup)

    def _add_hint_and_close(self, win):
        bar = tk.Frame(win, bg="#333333")
        bar.pack(side="bottom", fill="x")
        tk.Label(bar, text=HINT_TEXT, bg="#333333", fg="#bbbbbb",
                 font=("TkDefaultFont", 7)).pack(side="left", padx=4)
        # X falso: fecha este e abre 1-2 novos
        x_btn = tk.Label(win, text="✕", bg="#cc0000", fg="#ffffff",
                         font=("TkDefaultFont", 10, "bold"), padx=6)
        x_btn.place(relx=1.0, rely=0.0, anchor="ne")
        x_btn.bind("<Button-1>",
                   lambda e: self._close_popup(win, multiply=random.randint(1, 2)))

    def _build_image(self, win):
        path = random.choice(self.images)
        try:
            img = Image.open(path)
        except Exception:
            self._close_popup(win)  # imagem inválida: descarta este pop-up
            return
        target_w = random.randint(240, 460)
        ratio = target_w / img.width
        target_h = int(img.height * ratio)
        try:
            img = img.resize((target_w, target_h), Image.LANCZOS)
        except Exception:
            img = img.resize((target_w, target_h))
        photo = ImageTk.PhotoImage(img)

        lbl = tk.Label(win, image=photo, bd=0)
        lbl.image = photo  # evita coleta de lixo
        lbl.pack()

        self._add_hint_and_close(win)
        self._place_on_random_screen(win, target_w, target_h + 16)

    # -- agendamento ---------------------------------------------------------
    def schedule_spawn(self):
        if self.should_quit:
            return
        self.make_popup()
        base = self.args.interval * 1000
        delay = random.randint(int(base * 0.4), int(base * 1.4))
        self.root.after(max(50, delay), self.schedule_spawn)

    # -- kill switch (ESC 5s) ------------------------------------------------
    def on_press(self, key):
        if key == keyboard.Key.esc:
            now = time.time()
            with self.lock:
                self.last_press = now
                if not self.esc_down:
                    self.esc_down = True
                    self.esc_press_start = now

    def on_release(self, key):
        # A liberação real é detectada por "gap" em check_esc, para lidar com
        # o auto-repeat do X11 (que emite release+press a cada repetição).
        pass

    def check_esc(self):
        if self.should_quit:
            return
        now = time.time()
        held = 0.0
        with self.lock:
            if self.esc_down:
                if now - self.last_press > 0.2:
                    self.esc_down = False  # soltou de verdade
                else:
                    held = now - self.esc_press_start
        if held >= self.args.hold:
            self.quit()
            return
        self._update_overlay(held)

        # failsafe: encerra sozinho depois de auto_stop minutos
        if self.args.auto_stop and (now - self.start_time) >= self.args.auto_stop * 60:
            self.quit()
            return
        self.root.after(100, self.check_esc)

    def _update_overlay(self, held):
        if held >= 0.4:
            remaining = max(0, self.args.hold - held)
            if self.overlay is None:
                self.overlay = tk.Toplevel(self.root)
                self.overlay.overrideredirect(True)
                self.overlay.attributes("-topmost", True)
                self.overlay.configure(bg="#000000")
                self._ov_label = tk.Label(self.overlay, bg="#000000", fg="#00ff66",
                                          font=("TkDefaultFont", 16, "bold"), padx=16, pady=8)
                self._ov_label.pack()
                sx, sy, sw, sh = self.screens[0]
                self.overlay.geometry(f"+{sx + sw // 2 - 120}+{sy + 40}")
            self._ov_label.config(text=f"Fechando tudo… solte para cancelar ({remaining:.1f}s)")
            try:
                self.overlay.deiconify()
                self.overlay.lift()
            except Exception:
                pass
        elif self.overlay is not None:
            try:
                self.overlay.withdraw()
            except Exception:
                pass

    def quit(self):
        if self.should_quit:
            return
        self.should_quit = True
        try:
            if getattr(self, "listener", None):
                self.listener.stop()
        except Exception:
            pass
        try:
            self.root.destroy()
        except Exception:
            pass

    # -- loop principal ------------------------------------------------------
    def run(self):
        self.listener = keyboard.Listener(on_press=self.on_press,
                                          on_release=self.on_release)
        self.listener.start()
        self.schedule_spawn()
        self.check_esc()
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.quit()


def parse_args(argv=None):
    p = argparse.ArgumentParser(
        description="Annoying Popups - trollagem inofensiva (segure ESC 5s para sair).")
    p.add_argument("--interval", type=float, default=1.2,
                   help="intervalo médio entre pop-ups em segundos (padrão: 1.2)")
    p.add_argument("--max-popups", type=int, default=25,
                   help="máximo de pop-ups simultâneos (padrão: 25)")
    p.add_argument("--hold", type=float, default=5.0,
                   help="segundos segurando ESC para fechar tudo (padrão: 5)")
    p.add_argument("--auto-stop", type=float, default=120.0,
                   help="failsafe: encerra sozinho após N minutos (0 desativa; padrão: 120)")
    p.add_argument("--ads-dir", default=str(BASE_DIR / "ads"),
                   help="pasta com imagens de anúncios falsos (padrão: ./ads)")
    p.add_argument("--memes-dir", default=str(BASE_DIR / "memes"),
                   help="pasta com imagens de memes (padrão: ./memes)")
    p.add_argument("--no-sound", action="store_true", help="desativa o beep")
    return p.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    if keyboard is None:
        sys.exit("ERRO: 'pynput' não está instalado. Rode: pip install pynput\n"
                 "(é ele que garante o kill switch ESC — sem ele o app não inicia.)")
    if Image is None:
        sys.exit("ERRO: 'Pillow' não está instalado (necessário para exibir as imagens).\n"
                 "Rode: pip install pillow")
    app = PrankApp(args)
    if not app.images:
        sys.exit(f"Nenhuma imagem encontrada em '{args.ads_dir}' ou '{args.memes_dir}'.\n"
                 "Gere os anúncios/memes como imagem (.png/.jpg/...) e coloque nessas pastas.")
    print("Annoying Popups rodando 😈  — segure ESC por 5s para fechar tudo.")
    app.run()
    print("Encerrado. 👋")


if __name__ == "__main__":
    main()
