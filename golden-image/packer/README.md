# README

## Building

### Installing Packer

Install Packer: https://developer.hashicorp.com/packer/tutorials/docker-get-started/get-started-install-cli

On Ubuntu:

```bash
curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -
sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
sudo apt-get update && sudo apt-get install packer
```

### Creating the image

https://developer.hashicorp.com/packer/plugins/builders/docker

```bash
# Install all required plugins required
packer init wsl.pkr.hcl

# Build the image
packer build wsl.pkr.hcl
```

TODO
Examples

- https://github.com/lucagez/box/blob/10cc3d8edbca61ebd13cfc632ee3c6857c7daedc/packer.pkr.hcl#L2
- https://github.com/hashicorp/packer-plugin-ansible/blob/92833f237a068b88c0d3484db7f4dadfdcd74c83/example/docker.json.pkr.hcl#L6
- https://github.com/ecshreve/dev-env/blob/07e0df5e02c39d43cb510ddc20a66f784ea5ff13/packer/base/image.pkr.hcl#L3

### Importing in WSL

```bash
# import the golden image
wsl --import Composabl E:\wsl-composabl .\composabl.tar

# check if it was installed
wsl --list --verbose

# open it
wsl -d Composabl

# remove it
wsl --unregister Composabl
```

> More info: https://learn.microsoft.com/en-us/windows/wsl/use-custom-distro

### Creating

We can easily unregister and import through the following:

```bash
wsl --unregister Composabl; wsl --import Composabl E:\wsl-composabl .\composabl.tar; wsl -d Composabl
```
