packer {
  required_plugins {
    docker = {
      source  = "github.com/hashicorp/docker"
      version = "~> 1"
    }
  }
}


source "docker" "ubuntu" {
    image = "python:3.8-bullseye"
    export_path = "composabl.tar" # This is the path where the image will be exported as a tar file
}

build {
    sources = [
        "source.docker.ubuntu"
    ]

    // Update Sources
    provisioner "shell" {
        inline = [
            "apt-get update"
        ]
    }

    // Make the Docker Image suitable for WSL Usage
    provisioner "shell" {
        inline = [
            // Install required applications
            "apt-get install -y iputils-ping iproute2 curl wget vim passwd sudo apt-transport-https ca-certificates software-properties-common",

            // Add the 'composabl' user and add it to the sudoers group
            "useradd -m composabl",
            "echo \"composabl\" ALL=(ALL) NOPASSWD:ALL >> /etc/sudoers",

            // Add WSL Settings to change the mount point and default user
            "echo \"[user]\ndefault=composabl\" >> /etc/wsl.conf",
        ]
    }



    // Install screenfetch
    provisioner "shell" {
        inline = [
            "apt-get update",
            "apt-get install -y screenfetch"
        ]
    }

    // Create a script /etc/updated-motd.d/01-custom that runs screenfetch and add +x permissions
    provisioner "file" {
        source      = "./scripts/motd.sh"
        destination = "/etc/update-motd.d/01-custom"
    }

    provisioner "shell" {
        inline = [
            "chmod +x /etc/update-motd.d/01-custom"
        ]
    }

    // Install docker
    provisioner "shell" {
        inline = [
            "apt-get update",
            "apt-get install -y apt-transport-https ca-certificates curl gnupg-agent software-properties-common",
            "curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -",
            "add-apt-repository \"deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable\"",
            "apt-get update",
            "apt-get install -y docker-ce docker-ce-cli containerd.io"
        ]
    }

    // Install composabl as a pip library
    provisioner "shell" {
        inline = [
            "pip3 install composabl"
        ]
    }



//   // Create a MOTD from the ./first-run-notice.txt file
//     provisioner "file" {
//         source      = "./first-run-notice.txt"
//         destination = "/etc/motd"
//     }

//   provisioner "shell" {
//     inline = [
//       "sudo apt-get update",
//       "sudo apt-get install -y python3-pip git"
//     ]
//   }

//   provisioner "shell" {
//     inline = [
//       "pip3 install pyenv",
//       "pyenv install 3.8.0",
//       "pyenv global 3.8.0"
//     ]
//   }

//   provisioner "shell" {
//     inline = [
//       "sudo apt-get install -y apt-transport-https ca-certificates curl gnupg-agent software-properties-common",
//       "curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -",
//       "sudo add-apt-repository \"deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable\"",
//       "sudo apt-get update",
//       "sudo apt-get install -y docker-ce docker-ce-cli containerd.io"
//     ]
//   }

//   provisioner "shell" {
//     inline = [
//       "sudo tar -C / -cvf /composabl.tar --exclude=/composabl.tar ."
//     ]
//   }
}
