from pyinfra import context, local
from pyinfra.facts.files import Directory
from pyinfra.facts.server import LinuxName, Which
from pyinfra.operations import files, git, server


def setup_common():
    if context.host.get_fact(Directory, path="/home/ale/.oh-my-zsh") is None:
        files.download(
            name="Download oh-my-zsh install script",
            src="https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh",
            dest="/tmp/install-oh-my-zsh.sh",
        )
        server.shell(
            name="Install oh-my-zsh",
            commands=["sh /tmp/install-oh-my-zsh.sh --unattended"],
        )

    git.repo(
        name="Clone Powerlevel10k",
        pull=False,
        src="https://github.com/romkatv/powerlevel10k.git",
        dest="/home/ale/.oh-my-zsh/custom/themes/powerlevel10k",
    )

    git.repo(
        name="Clone tpm",
        pull=False,
        src="https://github.com/tmux-plugins/tpm",
        dest="/home/ale/.tmux/plugins/tpm",
    )

    if context.host.get_fact(Which, "kitty") is None:
        server.shell(
            name="Install kitty",
            commands=[
                "curl -L https://sw.kovidgoyal.net/kitty/installer.sh | sh /dev/stdin launch=n dest=/home/ale/.local",
                # Create symbolic links to add kitty and kitten to PATH (assuming ~/.local/bin is in
                # your system-wide PATH)
                "ln -sf ~/.local/kitty.app/bin/kitty ~/.local/kitty.app/bin/kitten ~/.local/bin/",
                # Place the kitty.desktop file somewhere it can be found by the OS
                "cp ~/.local/kitty.app/share/applications/kitty.desktop ~/.local/share/applications/",
                # If you want to open text files and images in kitty via your file manager also add the kitty-open.desktop file
                "cp ~/.local/kitty.app/share/applications/kitty-open.desktop ~/.local/share/applications/",
                # Update the paths to the kitty and its icon in the kitty desktop file(s)
                'sed -i "s|Icon=kitty|Icon=$(readlink -f ~)/.local/kitty.app/share/icons/hicolor/256x256/apps/kitty.png|g" ~/.local/share/applications/kitty*.desktop',
                'sed -i "s|Exec=kitty|Exec=$(readlink -f ~)/.local/kitty.app/bin/kitty|g" ~/.local/share/applications/kitty*.desktop',
                # Make xdg-terminal-exec (and hence desktop environments that support it use kitty)
                "echo 'kitty.desktop' > ~/.config/xdg-terminals.list",
            ],
        )

    if context.host.get_fact(Which, "docker") is None:
        server.shell(
            name="Install docker",
            commands=[
                "curl -fsSL https://get.docker.com -o /tmp/get-docker.sh",
                "sh /tmp/get-docker.sh",
                "groupadd docker || true",
                "usermod -aG docker ale",
                "systemctl enable docker.service",
                "systemctl enable containerd.service",
            ],
            _sudo=True,
        )


if context.host.get_fact(LinuxName) == "Fedora":
    local.include("tasks/fedora.py")
elif context.host.get_fact(LinuxName) == "Ubuntu":
    local.include("tasks/ubuntu.py")

setup_common()
