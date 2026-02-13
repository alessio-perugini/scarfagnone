from pyinfra.operations import pacman, server

# Install packages from AUR using yay (AUR helper)
# First, ensure yay is installed
server.shell(
    name="Install yay AUR helper",
    commands=[
        "if ! command -v yay &> /dev/null; then "
        "cd /tmp && "
        "sudo pacman -S --needed --noconfirm git base-devel && "
        "git clone https://aur.archlinux.org/yay.git && "
        "cd yay && "
        "makepkg -si --noconfirm; "
        "fi"
    ],
)

# Install packages from AUR using yay
server.shell(
    name="Install AUR packages",
    commands=[
        "yay -S --noconfirm --needed 1password 1password-cli brave-bin visual-studio-code-bin keybase-bin rofimoji"
    ],
)

pacman.packages(
    name="Install packages",
    packages=[
        "shellcheck",
        "flameshot",
        "git",
        "graphviz",
        "htop",
        "mise",
        "nss",
        "tmux",
        "vim",
        "vlc",
        "wireshark-qt",
        "zsh",
    ],
    present=True,
    _sudo=True,
)
