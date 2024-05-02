from pyinfra.operations import dnf, yum


# TODO probably I can cleanup those because I can pick up the .rpm packages
# that should contain the installation of key and repo
def install_dnf_package(name, keyurl, baseurl):
    dnf.key(
        src=keyurl,
        _sudo=True,
    )
    dnf.repo(
        name=name,
        present=True,
        src=name,
        gpgcheck=True,
        baseurl=baseurl,
        gpgkey=keyurl,
        _sudo=True,
    )


install_dnf_package(
    "1password",
    "https://downloads.1password.com/linux/keys/1password.asc",
    "https://downloads.1password.com/linux/rpm/stable/$basearch",
)
install_dnf_package(
    "brave-browser",
    "https://brave-browser-rpm-release.s3.brave.com/brave-core.asc",
    "https://brave-browser-rpm-release.s3.brave.com/$basearch",
)
install_dnf_package(
    "code",
    "https://packages.microsoft.com/keys/microsoft.asc",
    "https://packages.microsoft.com/yumrepos/vscode",
)
yum.rpm(
    name="keybase",
    src="https://prerelease.keybase.io/keybase_amd64.rpm",
    present=True,
)

dnf.packages(
    name="Install packages",
    packages=[
        "nss-tools",
        "tmux",
        "vim",
        "neovim",
        "git",
        "htop",
        "zsh",
        "vlc",
        "rofimoji",
        "flameshot",
        "1password",
        "ShellCheck",
        "1password-cli",
        "brave-browser",
        "code",
        "keybase",
        "wireshark",
        "graphviz",
        "hexyl",
    ],
    present=True,
    _sudo=True,
)
