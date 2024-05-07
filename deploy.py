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
        name="Clone asdf",
        pull=False,
        src="https://github.com/asdf-vm/asdf.git",
        dest="/home/ale/.asdf",
        branch="v0.14.0",
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
                "curl -L https://sw.kovidgoyal.net/kitty/installer.sh | sh /dev/stdin"
            ],
        )
    if context.host.get_fact(Which, "rustup") is None:
        server.shell(
            name="Install rust",
            commands=["curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh"],
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

    # Probably to use Cargo operations index
    status, _, _ = context.host.run_shell_command("cargo binstall --help")
    if not status:
        server.shell(
            name="Install cargo-binstall",
            commands=[
                "curl -L --proto '=https' --tlsv1.2 -sSf https://raw.githubusercontent.com/cargo-bins/cargo-binstall/main/install-from-binstall-release.sh | bash"
            ],
        )


def setup_asdf():
    apps = [
        "age",
        "awscli",
        "chezmoi",
        "dive",
        "editorconfig-checker",
        "fx",
        "github-cli",
        "golang",
        "golangci-lint",
        "helm",
        "k6",
        "k9s",
        "kind",
        "kubeconform",
        "kubectl",
        "kubectx",
        "minikube",
        "mkcert",
        "nodejs",
        "task",
        "terraform",
        "yq",
    ]

    for app in apps:
        server.shell(
            name=f"Install asdf {app}",
            commands=[
                f"asdf plugin-add {app}",
                f"asdf install {app} latest",
                f"asdf global {app} latest",
            ],
        )


def setup_cargo():
    apps = [
        "ripgrep",
        "eza",
        "fd-find",
    ]
    for app in apps:
        if context.host.get_fact(Which, app) is None:
            server.shell(
                name=f"Install cargo {app}",
                commands=[f"cargo binstall -y {app}"],
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
    )


if context.host.get_fact(LinuxName) == "Fedora":
    local.include("tasks/fedora.py")
elif context.host.get_fact(LinuxName) == "Ubuntu":
    local.include("tasks/ubuntu.py")

setup_common()
setup_asdf()
setup_cargo()
setup_go_install()
