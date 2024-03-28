#!/bin/bash -e
################################################################################
##  File:  zsh.sh
##  Desc:  Installs zsh and oh-my-zsh
################################################################################
echo "Running zsh.sh"

echo "Installing zsh..."
sudo apt-get install -y zsh
sudo chsh -s /bin/zsh $SSH_USER

# Install Oh-My-Zsh and enable the "gnzh" theme
echo "Installing Oh-My-Zsh..."
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
# cp /root/.zshrc /home/$SSH_USER/.zshrc
sed -i 's/ZSH_THEME=\"robbyrussell\"/ZSH_THEME=\"gnzh\"/g' /home/$SSH_USER/.zshrc

# Add Autosuggestions and Syntax Highlighting
echo "Installing zsh plugins..."
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git /home/$SSH_USER/.oh-my-zsh/custom/plugins/zsh-syntax-highlighting
git clone https://github.com/zsh-users/zsh-autosuggestions.git /home/$SSH_USER/.oh-my-zsh/custom/plugins/zsh-autosuggestions

# Enable the plugins
echo "Enabling zsh plugins..."
sed -i 's/plugins=(git)/plugins=(git zsh-syntax-highlighting zsh-autosuggestions)/g' /home/$SSH_USER/.zshrc
