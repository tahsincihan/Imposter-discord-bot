# Hosting the Imposter bot on Oracle Cloud

The bot runs as a background service (`imposter`) on the same Oracle VM as Maya. It starts on boot and restarts itself if it crashes.

## Deploy or update

From this folder on your Mac:

```bash
deploy/push_to_server.sh ubuntu@YOUR_VM_IP ~/Downloads/YOUR-KEY-FILE.key
```

This copies the code and `.env` to `~/imposter` on the VM, installs the packages and starts the bot. It ends with ✅ when the bot is online. Run the same command again after you change the code.

Don't run the bot on your Mac at the same time, or every command gets answered twice.

## Useful commands (on the VM)

| What | Command |
| --- | --- |
| Live logs | `sudo journalctl -u imposter -f` |
| Status | `systemctl status imposter` |
| Restart | `sudo systemctl restart imposter` |
| Stop | `sudo systemctl stop imposter` |

## Setting up a new VM

If you ever need a fresh VM, see Maya's guide (`deploy/ORACLE.md` in the Maya repo): create an Ubuntu VM with the Always Free shape, download the SSH key, then run the push command above.
