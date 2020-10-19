sudo apt-get install git
git clone https://github.com/aaranyak/DesignVideoGame.git
cd DesignVideoGame/Build_versions/blocked-v1/
sudo mv ./DayInLife_Blocked-v1 /usr/bin/DayInLife_Blocked-v1
sudo mv ./DayInLife_blocked_v1.png /usr/share/icons/hicolor/symbolic/apps/DayInLife_blocked_v1.png
sudo mv DayInLife-Blocked_v1.desktop /usr/share/Applications/DayInLife-Blocked_v1.desktop
cd ../../../
rm DesignVideoGame
