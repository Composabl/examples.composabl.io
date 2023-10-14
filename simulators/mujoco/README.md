# Mujoco

## Installing

```bash
mkdir -p ~/.mujoco
cd ~/.mujoco

# Download for Linux or Mac depending on uname and unzip into ~/.mujoco/mjpro150
if [[ "$(uname)" == "Darwin" ]]; then
    brew install gcc@9

    wget https://www.roboti.us/download/mujoco200_macos.zip
    unzip mujoco200_macos.zip
    rm mujoco200_macos.zip

    mv mujoco200_macos mujoco210

    # Hack for M1
    ln -sf /opt/homebrew/bin/gcc-11 /usr/local/bin/gcc-9
elif [[ "$(expr substr $(uname -s) 1 5)" == "Linux" ]]; then
    wget https://www.roboti.us/download/mujoco200_linux.zip
    unzip mujoco200_linux.zip
    rm mujoco200_linux.zip

    mv mujoco200_linux mujoco210
fi

# Rename the dir
mv ~/.mujoco/mjpro150 ~/.mujoco/mujoco210

# Install the license key
# https://www.roboti.us/file/mjkey.txt
wget https://www.roboti.us/file/mjkey.txt
mv mjkey.txt ~/.mujoco/mjkey.txt

# Install Library
pip install -U 'mujoco-py<1.50.2,>=1.50.1'

# Try it
python -c 'import mujoco_py'
```

~/.mujoco/mjpro150

1. Download the MuJoCo version 1.50 binaries for Linux or macOS.
2. Unzip the downloaded `mjpro150` directory into `~/.mujoco/mjpro150`, and place your license key (the mjkey.txt file from your email) at `~/.mujoco/mjkey.txt`.
3. Run `pip3 install -U 'mujoco-py<1.50.2,>=1.50.1'`
4. Run `python3 -c 'import mujoco_py'`
