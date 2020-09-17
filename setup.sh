mkdir /opt/HabitTracker
python3 ./data.py
mv ./* /opt/HabitTracker/
chmod -R 775 /opt/HabitTracker/

# Create service
echo "[Unit]
Description=Telegram bot HabitTracker

[Service]
Type=simple
ExecStart=/usr/bin/python3 /opt/HabitTracker/main.py

[Install]
WantedBy=multi-user.target" > /etc/systemd/system/bot_HabbitTracker.service

systemctl enable bot_HabbitTracker
systemctl restart bot_HabbitTracker
