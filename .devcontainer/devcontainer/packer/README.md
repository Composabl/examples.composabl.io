# Golden Image - Packer

This outputs a WSL image that can be imported in WSL

## Installing Packer

Install Packer: https://developer.hashicorp.com/packer/tutorials/docker-get-started/get-started-install-cli

On Ubuntu:

```bash
curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -
sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
sudo apt-get update && sudo apt-get install packer
```

## Running

```bash
# Install all required plugins required
packer init wsl.pkr.hcl

# Build the image
packer build wsl.pkr.hcl
```

## Importing in WSL

```bash
# import the golden image
# wsl --import <Name> <InstallLocation> <FileName>
wsl --import Composabl E:\wsl-composabl .\composabl.tar

# check if it was installed
wsl --list --verbose

# open it
wsl -d Composabl

# remove it
wsl --unregister Composabl
```

> More info: https://learn.microsoft.com/en-us/windows/wsl/use-custom-distro

> You can easily unregister and import through the following: `wsl --unregister Composabl; wsl --import Composabl E:\wsl-composabl .\composabl.tar; wsl -d Composabl`
