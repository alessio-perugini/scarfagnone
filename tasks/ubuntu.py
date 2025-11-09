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
        "name": "session-manager-plugin",
        "src": "https://s3.amazonaws.com/session-manager-downloads/plugin/latest/ubuntu_64bit/session-manager-plugin.deb",
    },
]

for item in dict:
    apt.deb(
        name=f"Install {item['name']}",
        src=item["src"],
        present=True,
        _sudo=True,
    )

# brave
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

# pritunl
#apt.repo(
#    name="Install pritunl",
#    src="deb https://repo.pritunl.com/stable/apt noble main",
#    present=True,
#    filename="pritunl",
#    _sudo=True,
#)
#apt.packages(
#    name="Install gnupg",
#    packages=["gnupg"],
#    present=True,
#    _sudo=True,
#)
#server.shell(
#    name="Install pritunl gpg key",
#    commands=[
#        "gpg --keyserver hkp://keyserver.ubuntu.com --recv-keys 7568D9BB55FF9E5287D586017AE645C0CF8E292A",
#        "gpg --armor --export 7568D9BB55FF9E5287D586017AE645C0CF8E292A | sudo tee /etc/apt/trusted.gpg.d/pritunl.asc",
#    ],
#    _sudo=True,
#)

# mise
server.shell(
    name="Download mise key",
    commands=[
        "wget -qO - https://mise.jdx.dev/gpg-key.pub | gpg --dearmor | sudo tee /etc/apt/keyrings/mise-archive-keyring.gpg 1> /dev/null",
    ],
    _sudo=True,
)
apt.repo(
    name="Install mise",
    src="deb [signed-by=/etc/apt/keyrings/mise-archive-keyring.gpg arch=amd64] https://mise.jdx.dev/deb stable main",
    present=True,
    filename="mise",
    _sudo=True,
)

apt.update(
    name="Update apt repositories",
    cache_time=3600,
    _sudo=True,
)

apt.packages(
    name="Install packages",
    packages=[
        "1password-cli",
        "brave-browser",
        "build-essential",
        "bzip2",
        "clang-format",
        "clangd",
        "cmake",
        "ffmpeg",
        "flameshot",
        "git",
        "graphviz",
        "hexdiff",
        "htop",
        "jc",
        "jq",
        "libnss3-tools",
        "make",
        "mise",
        #"pritunl-client-electron",
        "shellcheck",
        "tmux",
        "vim",
        "vlc",
        "wireshark",
        "zsh",
        "wl-clipboard",
        "parallel",
    ],
    present=True,
    _sudo=True,
)
