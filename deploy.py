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
                "curl -L https://sw.kovidgoyal.net/kitty/installer.sh | sh /dev/stdin launch=n dest=/home/ale/.local/bin"
            ],
        )

    if context.host.get_fact(Which, "docker") is None:
        server.shell(
            name="Install docker",
            commands=[
                "curl -fsSL https://get.docker.com -o /tmp/get-docker.sh",
                "sh /tmp/get-docker.sh",
                "groupadd docker",
                "usermod -aG docker ale",
                "systemctl enable docker.service",
                "systemctl enable containerd.service",
            ],
            _sudo=True,
        )


def setup_go_install():
    server.shell(
        name="Install go applications",
        commands=[
            "go install github.com/google/addlicense@latest",
            "go install github.com/itchyny/bed/cmd/bed@latest",
            "go install golang.org/x/perf/cmd/benchstat@latest",
            "go install github.com/bufbuild/buf/cmd/buf@latest",
            "go install github.com/KyleBanks/depth/cmd/depth@latest",
            "go install github.com/go-delve/delve/cmd/dlv@latest",
            "go install github.com/mailru/easyjson/easyjson@latest",
            "go install 4d63.com/embedfiles@latest",
            "go install goa.design/goa/v3/cmd/goa@v3",
            "go install github.com/loov/goda@latest",
            "go install github.com/kisielk/godepgraph@latest",
            "go install golang.org/x/lint/golint@latest",
            "go install golang.org/x/vuln/cmd/govulncheck@latest",
            "go install github.com/nao1215/gup@latest",
            "go install github.com/bufbuild/buf/cmd/protoc-gen-buf-breaking@latest",
            "go install github.com/bufbuild/buf/cmd/protoc-gen-buf-lint@latest",
            "go install github.com/pseudomuto/protoc-gen-doc/cmd/protoc-gen-doc@latest",
            "go install google.golang.org/protobuf/cmd/protoc-gen-go@latest",
            "go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest",
        ],
        _env={
            "GOPATH": "$HOME/go",
            "PATH": "$PATH:$HOME/.asdf/shims",
        },
    )


if context.host.get_fact(LinuxName) == "Fedora":
    local.include("tasks/fedora.py")
elif context.host.get_fact(LinuxName) == "Ubuntu":
    local.include("tasks/ubuntu.py")

setup_common()
setup_go_install()
