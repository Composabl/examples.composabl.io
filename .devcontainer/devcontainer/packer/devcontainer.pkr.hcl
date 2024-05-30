packer {
  required_plugins {
    docker = {
      source  = "github.com/hashicorp/docker"
      version = "~> 1"
    }
  }
}

locals {
  image_folder            = "/packer"
  helper_script_folder    = "/packer/helpers"
  installer_script_folder = "/packer/installers"
  imagedata_file          = "/packer/imagedata.json"
}

variables {
    ssh_username = "composabl"
    ssh_password = "composabl"

    version_python = "3.11.8"
    version_pip_composabl = "0.8.0"

    docker_repository = ""
    docker_username = ""
    docker_password = ""
}

source "docker" "ubuntu" {
    # https://hub.docker.com/_/python
    # https://www.debian.org/releases/
    # bookworm = 12
    # bullseye = 11
    # buster = 10
    image = "python:3.11-bookworm"
    commit = true

    # Run the bash terminal as default (it's a devcontainer)
    changes = [
        "CMD [\"sleep\", \"infinity\"]",
        "ENTRYPOINT [\"/docker-entrypoint.sh\"]",
    ]
}

build {
    sources = [
        "source.docker.ubuntu"
    ]

    // Create a folder to store temporary data
    provisioner "shell" {
        inline          = ["mkdir ${local.image_folder}", "chmod 777 ${local.image_folder}"]
    }

    // Add base packages
    provisioner "shell" {
        script          = "${path.root}/scripts/base/apt.sh"
    }

    // Configure User and set is as the active user
    provisioner "shell" {
        environment_vars = ["HELPER_SCRIPTS=${local.helper_script_folder}", "SSH_USER=${var.ssh_username}"]
        script          = "${path.root}/scripts/base/configure-user.sh"
    }

    // Configure limits
    provisioner "shell" {
        script          = "${path.root}/scripts/base/limits.sh"
    }

    // Configure Environment
    provisioner "shell" {
        environment_vars = ["HELPER_SCRIPTS=${local.helper_script_folder}"]
        script           = "${path.root}/scripts/base/configure-environment.sh"
    }

    // Install Entrypoint
    provisioner "file" {
        source      = "${path.root}/scripts/docker-entrypoint.sh"
        destination = "/docker-entrypoint.sh"
    }

    provisioner "shell" {
        inline = [
            "chmod +x /docker-entrypoint.sh"
        ]
    }

    // Install helpers and installer scripts
    provisioner "file" {
        source      = "${path.root}/scripts/helpers"
        destination = "${local.helper_script_folder}"
    }

    provisioner "file" {
        source      = "${path.root}/scripts/installers"
        destination = "${local.installer_script_folder}"
    }

    // Run installers (as root)
    provisioner "shell" {
        execute_command = "sudo sh -c '{{ .Vars }} {{ .Path }}'" // Switch to the sudo user
        environment_vars = [
            "DEBIAN_FRONTEND=noninteractive",
            "HELPER_SCRIPTS=${local.helper_script_folder}",
            "INSTALLER_SCRIPT_FOLDER=${local.installer_script_folder}", "SSH_USER=${var.ssh_username}",
        ]
        scripts         = [
            "${path.root}/scripts/installers/root/motd.sh",
            "${path.root}/scripts/installers/root/python.sh",
            "${path.root}/scripts/installers/root/docker.sh",
            "${path.root}/scripts/installers/root/kubernetes-tools.sh",
        ]
    }

    // Run installers (as user)
    provisioner "shell" {
        execute_command = "sudo -u ${var.ssh_username} sh -c '{{ .Vars }} {{ .Path }}'" // Switch to the sudo user
        environment_vars = [
            "DEBIAN_FRONTEND=noninteractive",
            "HELPER_SCRIPTS=${local.helper_script_folder}",
            "INSTALLER_SCRIPT_FOLDER=${local.installer_script_folder}",
            "SSH_USER=${var.ssh_username}",
            "VERSION_PYTHON=${var.version_python}",
            "VERSION_PIP_COMPOSABL=${var.version_pip_composabl}",
        ]
        scripts         = [
            "${path.root}/scripts/installers/user/zsh.sh",
            "${path.root}/scripts/installers/user/devcontainer.sh",
            "${path.root}/scripts/installers/user/composabl.sh",
            "${path.root}/scripts/installers/user/bashrc.sh",
        ]
    }

    post-processors {
        post-processor "docker-tag" {
            repository = "${var.docker_repository}"
            tags       = ["latest"]
        }

        post-processor "docker-push" {
            login = true
            login_username = "${var.docker_username}"
            login_password = "${var.docker_password}"
            login_server = "docker.io"
        }
    }
}
