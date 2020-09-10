#bash
echo 'Setting up for Raspberry Pi'

# Install dependencies
echo '🔷 Installing dependencies'
sudo pip3 install termcolor f1-2019-telemetry f1-2020-telemetry rpi_ws281x

# Configure ws281x module
echo '🔷 Configure ws281x module for Raspberry Pi'
echo 'blacklist snd_bcm2835' | sudo tee -a /etc/modprobe.d/snd-blacklist.conf
echo 'hdmi_force_hotplug=1' | sudo tee -a /boot/config.txt
echo 'hdmi_force_edid_audio=1' | sudo tee -a /boot/config.txt
