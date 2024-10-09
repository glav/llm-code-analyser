#!/bin/bash
# Define the path to your Zsh profile
zshrc_path="$HOME/.zshrc"
bashrc_path="$HOME/.bashrc"

echo "export PATH=\"$HOME/.local/bin:$PATH\"" >> "$zshrc_path"
echo "export PATH=\"$HOME/.local/bin:$PATH\"" >> "$bashrc_path"

cat "$HOME"/.zshrc
export PATH="$HOME/.local/bin:$PATH"

# install the requirements
# pip install --upgrade pip
pip install ruff
pip install --user -r requirements.txt

# install the pre-commit hooks
pre-commit autoupdate
pre-commit install

# remove warning in az cli
#az config set clients.show_secrets_warning=False

sudo cp -r /root/.ssh/  ~/
