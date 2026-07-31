# 😈 Annoying Popups

Trollagem **inofensiva** estilo "computador que pegou vírus": gera pop-ups de
anúncios falsos + memes em posições e monitores aleatórios, rodando em segundo
plano. Inspirado no espírito do lendário *Desktop Goose*.

Feito para a brincadeira de escritório: quem deixa a estação **desbloqueada**
ganha uma chuva de pop-ups. 😏

## 🔒 O que ele NÃO faz (garantias de "inofensivo")
- Não lê, escreve ou apaga nenhum arquivo do usuário.
- Não altera configurações, wallpaper, registro ou nada do sistema.
- Não persiste: fechou, acabou (não instala serviço, não sobe no boot).
- Não captura teclas/senhas — o `pynput` só observa o **ESC** para o kill switch.
- Failsafe: encerra sozinho depois de 2 horas (configurável).

## 🛑 Como fechar
**Segure a tecla ESC por 5 segundos.** Aparece uma contagem regressiva no topo;
soltar o ESC cancela. Isso fecha todos os pop-ups e encerra o app.

## ▶️ Como rodar

Pré-requisito: **[uv](https://docs.astral.sh/uv/)**. O uv cuida de tudo — baixa
um Python gerenciado (que já inclui **tkinter**), cria o `.venv` e instala as
dependências na primeira execução. Não precisa instalar Python nem tkinter à mão.

```bash
# instalar o uv (se ainda não tiver):
curl -LsSf https://astral.sh/uv/install.sh | sh   # Linux/macOS
# Windows (PowerShell): irm https://astral.sh/uv/install.ps1 | iex
```

### Linux / macOS
```bash
./run.sh
# ou, direto:
uv run python annoying_popups.py
```
> **Linux:** funciona em sessão **X11**. No **Wayland**, o `pynput` pode não
> capturar o ESC globalmente — troque a sessão para "Xorg" na tela de login,
> ou rode com o app em foco.
>
> **macOS:** na 1ª execução o sistema pede permissão de **Acessibilidade** para
> o Terminal (Ajustes → Privacidade e Segurança → Acessibilidade). É necessário
> para o kill switch ESC funcionar globalmente.

### Windows
Duplo clique em **`run.bat`** (ou `uv run pythonw annoying_popups.py` no
terminal). O `pythonw` evita abrir janela de console.

## 🕹️ Rodar em segundo plano
Desanexado do terminal (pode fechar o terminal que segue rodando):
```bash
./run-bg.sh          # Linux/macOS  (salva o PID em .annoying.pid)
run-bg.bat           # Windows      (usa pythonw, sem console)
```
Botão de pânico — encerra tudo mesmo que o ESC falhe:
```bash
./stop.sh            # Linux/macOS
stop.bat             # Windows
```
No Windows, o executável (`--windowed`) já roda sem console, então é background por natureza.

## ⚙️ Opções
```
uv run python annoying_popups.py --help

--interval 1.2       intervalo médio entre pop-ups (segundos)
--max-popups 25      máximo de pop-ups simultâneos
--hold 5             segundos segurando ESC para fechar tudo
--auto-stop 120     encerra sozinho após N minutos (0 desativa)
--ads-dir ./ads      pasta com imagens de anúncios falsos
--memes-dir ./memes  pasta com imagens de memes
--no-sound           desativa o beep
```

## 🖼️ Imagens (anúncios + memes)
O app **só exibe imagens** — não desenha mais anúncios de texto. Você fornece:
- **`ads/`** — os anúncios falsos, que você gera como imagem (ex.: exportando
  um HTML/CSS para PNG, ou em qualquer editor).
- **`memes/`** — suas imagens de memes.

Formatos: `.png .jpg .jpeg .gif .bmp .webp`. O app sorteia de ambas as pastas e
mistura tudo. Se não houver nenhuma imagem, ele avisa e encerra.

## 📦 Dependências
Gerenciadas pelo **uv** (`pyproject.toml` + `uv.lock`):
- **pynput** (obrigatório) — kill switch ESC.
- **Pillow** (obrigatório) — exibir as imagens.
- **screeninfo** (recomendado) — multi-monitor; há fallback sem ele.
- **tkinter** — GUI, já incluído no Python gerenciado pelo uv.

## 📦➡️ Executável (sem instalar nada)
Dá pra gerar um binário **single-file** (não precisa de Python/uv na máquina-alvo).

Local:
```bash
./build.sh      # Linux/macOS  -> dist/annoying-popups
build.bat       # Windows      -> dist\annoying-popups.exe
```
O `build.py` descobre e embute o Tcl/Tk automaticamente.

Release automática por SO: um push de **tag `v*`** dispara o GitHub Actions
(`.github/workflows/release.yml`), que builda em Linux, macOS e Windows e anexa
os binários na Release:
```bash
git tag v0.1.0 && git push origin v0.1.0
```
Cada SO é buildado no seu próprio runner (não dá para cross-compilar).
No macOS o binário ainda pede permissão de Acessibilidade na 1ª execução.

## ⚠️ Use com bom senso
Ferramenta de brincadeira consentida entre colegas. Não use em máquinas de
terceiros sem permissão.
