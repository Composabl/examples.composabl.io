packer {
  required_plugins {
    azure = {
      source  = "github.com/hashicorp/azure"
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
    ssh_password = "composabl123!"

    version_nvm = "0.39.7"
    version_python = "3.11.8"
}

# https://developer.hashicorp.com/packer/integrations/hashicorp/azure/latest/components/builder/arm
source "azure-arm" "ubuntu" {
    client_id       = "your_client_id"
    client_secret   = "your_client_secret"
    subscription_id = "your_subscription_id"
    tenant_id       = "your_tenant_id"

    managed_image_resource_group_name = "your_resource_group"
    managed_image_name                = "your_image_name"

    # The resource group to create the temporary resources in
    # we use the same as else we need a new SP
    build_resource_group_name          = "your_resource_group"

    os_type            = "Linux"
    image_publisher    = "Canonical"
    image_offer        = "0001-com-ubuntu-server-jammy"
    image_sku          = "22_04-lts-gen2"

    vm_size           = "Standard_D8_v5"

    ssh_username      = "${var.ssh_username}"
}

build {
    sources = [
        "source.azure-arm.ubuntu"
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
            "${path.root}/scripts/installers/root/wsl.sh",
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
}
