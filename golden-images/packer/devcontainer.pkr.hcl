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

    version_nvm = "0.39.5"
    version_python = "3.8.17"
}


source "docker" "ubuntu" {
    image = "ubuntu:22.04"
    commit = true
    // export_path = "composabl.tar" # This is the path where the image will be exported as a tar file
}

build {
    sources = [
        "source.docker.ubuntu"
    ]

    // Add base packages
    provisioner "shell" {
        script          = "${path.root}/scripts/base/apt.sh"
    }

    // Configure User and set is as the active user
    provisioner "shell" {
        environment_vars = ["HELPER_SCRIPTS=${local.helper_script_folder}", "SSH_USER=${var.ssh_username}"]
        script          = "${path.root}/scripts/base/configure-user.sh"
    }

    // Create a folder to store temporary data
    provisioner "shell" {
        inline          = ["mkdir ${local.image_folder}", "chmod 777 ${local.image_folder}"]
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

    // Install helpers and installer scripts
    provisioner "file" {
        destination = "${local.helper_script_folder}"
        source      = "${path.root}/scripts/helpers"
    }

    provisioner "file" {
        destination = "${local.installer_script_folder}"
        source      = "${path.root}/scripts/installers"
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
            // "${path.root}/scripts/installers/root/wsl.sh",
            "${path.root}/scripts/installers/root/motd.sh",
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
            "INSTALLER_SCRIPT_FOLDER=${local.installer_script_folder}", "SSH_USER=${var.ssh_username}",
            "VERSION_PYTHON=${var.version_python}",
        ]
        scripts         = [
            "${path.root}/scripts/installers/user/zsh.sh",
            "${path.root}/scripts/installers/user/pyenv.sh",
            "${path.root}/scripts/installers/user/composabl.sh",
            "${path.root}/scripts/installers/user/bashrc.sh",
        ]
    }

    post-processors {
        post-processor "docker-tag" {
            repository = "composabl/golden-image-devcontainer"
            tags       = ["latest"]
        }

        post-processor "docker-tag" {
            repository = "ghcr.io/composabl/golden-image-devcontainer"
            tags       = ["latest"]
        }

        post-processor "docker-push" {}
    }
}
