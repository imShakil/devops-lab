# Fail2Ban Alerts to Discord
A simple guide to setup fail2ban action for sending an alert message to discord channel.

1. Create a Discord Webhook
   - Go to your Discord Server → Select a channel.
   - Click Edit Channel → Integrations → Webhooks → New Webhook.
   - Name it (ex: Fail2Ban Alerts) and copy the Webhook URL.
   - Example: https://discord.com/api/webhooks/1234567890/abcdefghijklmnopqrstuvwxyz

2. Create the Discord Notification Script
   - install `jq`:
     ```
     sudo apt install jq
     ```
   - Create the file /usr/local/bin/fail2ban-discord.sh:
      ```
      #!/bin/bash
      
      JAIL="$1"
      IP="$2"
      MATCHES="$3"
      
      WEBHOOK_URL="YOUR-WEBHOOK-URL"
      
      HOSTNAME=$(hostname)
      TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
      
      MESSAGE="** Fail2Ban Alert**
      **Server:** ${HOSTNAME}
      **Time:** ${TIMESTAMP}
      **Jail:** \`${JAIL}\`
      **Banned IP:** \`${IP}\`
      **Reason:** ${MATCHES}"
      
      # Send to Discord
      curl -s -H "Content-Type: application/json" \
           -X POST \
           -d "$(jq -nc --arg content "$MESSAGE" '{content: $content}')" \
           "$WEBHOOK_URL"
      ```
    - Make it executable:
      ```
      sudo chmod +x /usr/local/bin/fail2ban-discord.sh
      ```
3. Create a Custom Fail2Ban Action
   - Create /etc/fail2ban/action.d/discord-ban.conf:
     ```
      [Definition]
      actionstart =
      actionstop =
      actioncheck =
      actionban = /usr/local/bin/fail2ban-discord.sh "<name>" "<ip>" "<matches>"
      actionunban =
     ```
    
4. Apply It in Jail Config
   - Edit /etc/fail2ban/jail.local or create if not existing:
      ```
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
     ```
     sudo systemctl restart fail2ban
     ```

6. Test
     To test, you can intentionally trigger a failed login from a different IP or use:
     ```
     sudo fail2ban-client set sshd banip 1.2.3.4
     ```

All are done!. You should receive an alert in your Discord channel.
