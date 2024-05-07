from pyinfra.operations import apt, files, server

dict = [
    {
        "name": "Obsidian",
        "src": "https://github.com/obsidianmd/obsidian-releases/releases/download/v1.5.12/obsidian_1.5.12_amd64.deb",
    },
    {
        "name": "1password",
        "src": "https://downloads.1password.com/linux/debian/amd64/stable/1password-latest.deb",
    },
    {
        "name": "Code",
        "src": "https://code.visualstudio.com/sha/download?build=stable&os=linux-deb-x64",
    },
    {
        "name": "keybase",
        "src": "https://prerelease.keybase.io/keybase_amd64.deb",
    },
    {
        "name": "session-manager-plugin",
        "src": "https://s3.amazonaws.com/session-manager-downloads/plugin/latest/ubuntu_64bit/session-manager-plugin.deb",
    },
    {
        "name": "slack",
        "src": "https://downloads.slack-edge.com/desktop-releases/linux/x64/4.37.101/slack-desktop-4.37.101-amd64.deb",
    },
]

for item in dict:
    apt.deb(
        name=f"Install {item['name']}",
        src=item["src"],
        present=True,
        _sudo=True,
    )

files.download(
    name="Download brave key",
    src="https://brave-browser-apt-release.s3.brave.com/brave-browser-archive-keyring.gpg",
    dest="/usr/share/keyrings/brave-browser-archive-keyring.gpg",
    _sudo=True,
)
apt.repo(
    name="Install Brave repo",
    src="deb [signed-by=/usr/share/keyrings/brave-browser-archive-keyring.gpg] https://brave-browser-apt-release.s3.brave.com/ stable main",
    present=True,
    filename="brave-browser-release",
    _sudo=True,
)

# ESET
files.download(
    name="Download eset",
    src="https://download.eset.com/com/eset/apps/business/eea/linux/g2/latest/eeau_x86_64.bin",
    dest="/tmp/eeau_x86_64.bin",
    mode="755",
)
server.shell(
    name="Extract eset deb",
    commands=["/tmp/eeau_x86_64.bin --accept-license --no-install"],
)
apt.deb(
    name="Install eset",
    src="/tmp/eea-10.2.2.0-ubuntu18.x86_64.deb",
    present=True,
    _sudo=True,
)

apt.packages(
    name="Install packages",
    packages=[
        "libnss3-tools",
        "clangd",
        "clang-format",
        "bzip2",
        "cmake",
        "make",
        "ffmpeg",
        "jq",
        "jc",
        "tmux",
        "vim",
        "neovim",
        "git",
        "htop",
        "zsh",
        "vlc",
        "shellcheck",
        "build-essential",
        "flameshot",
        "1password-cli",
        "brave-browser",
        "ruby-licensee",
        "wireshark",
        "graphviz",
        "hexdiff",
        "hexyl",
    ],
    present=True,
    _sudo=True,
)
