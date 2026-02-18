---
date: 2024-01-10
categories:
  - Security
  - Git
  - Tutorial
---

# Git Commit Signature Verification

Learn how to set up GPG commit signing to verify the authenticity of your Git commits and enhance your repository security.

<!-- more -->

## Why Sign Your Commits?

- **Authentication**: Prove commits are actually from you
- **Integrity**: Ensure commits haven't been tampered with
- **Trust**: Build confidence in your codebase
- **Compliance**: Meet security requirements for sensitive projects

## Prerequisites

Install GnuPG on your system:

```bash
sudo apt-get install gnupg
```

## Step 1: Generate GPG Key

Create a new GPG key pair with your details:

```bash
gpg --full-generate-key
```

Choose:

- Key type: RSA and RSA (default)
- Key size: 4096 bits
- Expiration: 1-2 years (recommended)
- Enter your name and email (must match Git config)

## Step 2: Export Public Key

Get your public key in text format:

```bash
gpg --armor --export [email-id/key-id] > gpg.key
cat gpg.key
```

## Step 3: Add Key to GitHub

1. Copy the public key content
2. Go to GitHub Settings → SSH and GPG keys
3. Click "New GPG key"
4. Paste your public key

For detailed steps, check this [comprehensive guide](https://medium.com/big0one/how-to-create-a-verified-commit-in-github-using-gpg-key-signature-16acee004e0f).

## Step 4: Configure Git Client

First, find your secret key ID:

```bash
gpg --list-secret-keys --keyid-format=long
```

Look for the key ID after `rsa4096/` in the output.

Then configure Git:

```bash
git config --global user.signingkey [secret-key-id]
git config --global commit.gpgsign true
git config --global gpg.program $(which gpg)
```

## Step 5: Sign Your Commits

Now all commits will be signed automatically, or manually sign:

```bash
git commit -S -m "Your commit message"
```

## Verification

Verify signed commits:

```bash
git log --show-signature
```

On GitHub, signed commits show a "Verified" badge.

## Troubleshooting

### GPG Agent Issues

```bash
export GPG_TTY=$(tty)
echo 'export GPG_TTY=$(tty)' >> ~/.bashrc
```

### Key Expiration

```bash
gpg --edit-key [key-id]
# Use 'expire' command to extend
```

## Best Practices

- ✅ Use strong passphrases
- ✅ Backup your private key securely
- ✅ Set reasonable expiration dates
- ✅ Revoke compromised keys immediately
- ✅ Use different keys for different purposes

## Next Steps

- Set up commit signing in your IDE
- Configure organization-wide signing policies
- Explore advanced GPG features
- Learn about signed tags

---

> Secure your commits, secure your code! 🔐
