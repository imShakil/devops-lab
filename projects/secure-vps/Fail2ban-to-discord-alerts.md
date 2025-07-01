# Fail2Ban Alerts to Discord

A simple guide to setup fail2ban action for sending an alert message to discord channel.

1. Create a Discord Webhook
   - Go to your Discord Server → Select a channel.
   - Click Edit Channel → Integrations → Webhooks → New Webhook.
   - Name it (ex: Fail2Ban Alerts) and copy the Webhook URL.
   - Example: `https://discord.com/api/webhooks/1234567890/abcdefghijklmnopqrstuvwxyz`

2. Create the Discord Notification Script
   - install `jq`:

     ```bash
     sudo apt install jq
     ```

   - Create the file `/usr/local/bin/fail2ban-discord.sh`:

      ```bash
      #!/usr/bin/bash

      JAIL="$1"
      IP="$2"
      MATCHES="$3"
      
      WEBHOOK_URL="https://discord.com/api/webhooks/1304853928789278730/e3AGSi6ZqUWmX7bWUa8xmvHqes5zAn_ZQQEHBAadqTCugVnfhAzwbuNj6TZoF-vkUaRL"
      
      JSON="$(curl -s https://api.iplocation.net/\?ip\=$IP)"
      COUNTRY=$(echo "$JSON" | jq -r '.country_name')
      CC=$(echo "$JSON" | jq -r '.country_code2' | tr 'A-Z' 'a-z')
      
      #echo $JSON
      #echo $COUNTRY
      #echo $CC
      
      HOSTNAME=$(hostname)
      TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
      
      MESSAGE="**🚨 Fail2Ban Alert**
      **Server:** $HOSTNAME
      **Time:** $TIMESTAMP
      **Jail:** \`$JAIL\`
      **Banned IP:** \`$IP\`
      **Attacked From:** $COUNTRY :flag_$CC:
      **Reason:** $MATCHES"
      
      
      curl -s -H "Content-Type: application/json" \
           -X POST \
           -d "$(jq -nc --arg content "$MESSAGE" '{content: $content}')" \
           "$WEBHOOK_URL"
      
      ```

   - Make it executable:

      ```bash
      sudo chmod +x /usr/local/bin/fail2ban-discord.sh
      ```

3. Create a Custom Fail2Ban Action

   - Create `/etc/fail2ban/action.d/discord-ban.conf`:

     ```ini
      [Definition]
      actionstart =
      actionstop =
      actioncheck =
      actionban = /usr/local/bin/fail2ban-discord.sh "<name>" "<ip>" "<matches>"
      actionunban =
     ```

4. Apply It in Jail Config
   - Edit /etc/fail2ban/jail.local or create if not existing:

      ```ini
      [sshd]
      enabled = true
      port = ssh
      logpath = /var/log/auth.log
      maxretry = 3
      findtime = 600
      bantime = 3600
      action = discord-ban
      ```

5. Restart fail2ban

      ```bash
      sudo systemctl restart fail2ban
      ```

6. Test

     To test, you can intentionally trigger a failed login from a different IP or use:

      ```bash
      sudo fail2ban-client set sshd banip 222.65.14.143
      ```

      All are done!. You should receive an alert in your Discord channel like below.
      
      ```text
      🚨 Fail2Ban Alert
      Server: srv627828
      Time: 2025-06-30 22:36:19
      Jail: sshd
      Banned IP: 222.65.14.143 
      Attacked From: China :flag_cn: 
      Reason: Jun 30 22:36:14 srv627828 sshd[2154564]: Invalid user user from 222.65.14.143 port 17607
      Jun 30 22:36:16 srv627828 sshd[2154566]: Invalid user user from 222.65.14.143 port 17608
      Jun 30 22:36:17 srv627828 sshd[2154568]: Invalid user user from 222.65.14.143 port 17609
      ```
