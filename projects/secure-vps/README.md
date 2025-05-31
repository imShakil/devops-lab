# Secure VPS From Bruteforce SSH Attack

## Secure SSH connection

1. Disbaled password based authentication and Make sure PublicKey based Authentication is enabled:

    ```ini
    PasswordAuthentication no
    PubkeyAuthentication yes
    ```

2. Better to keep root login disabled:

    ```ini
    PermitRootLogin no
    ```

    Alternatively, you can allow ssh-key based authentication for root user:

    ```ini
    PermitRootLogin prohibit-password
    ```

3. If it's still asking password when key doesn't match then forecuflly disabled by setting:

    ```ini
    AuthenticationMethods publickey
    ```

4. Finally, If possible change the default port `22` to something else. It's hard to guess someone which port ssh using in this case. Checkout [sshd_config](./setup-sshd-config.md)

5. (Optional): Use third party tool `fail2ban` to monitor and ban IP from suspect attack. See [How to Setup Fail2ban and connect with Discord](./Fail2ban-to-discord-alerts.md) to block IP and sending alert as action.
