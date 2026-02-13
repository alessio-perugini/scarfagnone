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
        "makepkg -si --noconfirm && "
        "cd .. && "
        "rm -rf yay; "
        "fi"
    ],
)

# Install packages from AUR using yay
aur_packages = [
    "1password",
    "1password-cli",
    "brave-bin",
    "visual-studio-code-bin",
    "keybase-bin",
    "rofimoji",
]

server.shell(
    name="Install AUR packages",
    commands=[
        f"yay -S --noconfirm --needed {' '.join(aur_packages)}"
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
