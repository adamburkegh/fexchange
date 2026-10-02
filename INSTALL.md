# Installing fexchange on AWS EC2

Assumes a disposable instance: the public hostname changes on stop/start or replacement, so `<public-dns>` below means "whatever it is today" (see the end). Data lives on the instance and disappears with it, by design.

## 1. Launch

- Amazon Linux 2023 (on Ubuntu, use `ubuntu` as the user and `apt` for packages), any small instance size, default 8 GiB disk.
- ED25519 key pair; keep the `.pem`.
- Security group inbound: **22** from My IP, **5000** from `0.0.0.0/0` (or narrower). The service has no authentication.

## 2. Connect

```bash
mkdir -p ~/.ssh && mv ~/Downloads/my-key.pem ~/.ssh/ && chmod 400 ~/.ssh/my-key.pem
ssh -i ~/.ssh/my-key.pem ec2-user@<public-dns>
```

## 3. Install

No git needed, as the repo is public:

```bash
curl -L https://github.com/adamburkegh/fexchange/archive/refs/heads/main.tar.gz | tar xz
cd fexchange-main
sudo dnf install -y python3-pip      # Ubuntu: sudo apt install -y python3-venv python3-pip
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 4. Run and test

```bash
python fexwaitress.py
```

Waitress serves plain HTTP on port 5000, with all routes under the `ifn653` prefix set in `fexwaitress.py`. From your own machine:

```bash
curl -X POST --data 'content=hello' http://<public-dns>:5000/ifn653/fexchange/teststudent/plastic
curl http://<public-dns>:5000/ifn653/fexchange/teststudent/plastic
```

Use `http://`, not `https://`. An https URL just hangs, and browsers may auto-upgrade, so type the scheme.

## 5. Keep it running

Create `/etc/systemd/system/fexchange.service`:

```ini
[Unit]
Description=fexchange
After=network.target

[Service]
User=ec2-user
WorkingDirectory=/home/ec2-user/fexchange-main
ExecStart=/home/ec2-user/fexchange-main/venv/bin/python fexwaitress.py
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now fexchange
journalctl -u fexchange -f      # logs
```

For a quick job, `nohup python fexwaitress.py > fex.log 2>&1 &` survives logout but not a reboot.

## Finding the server name

Console: EC2 → Instances → *Public IPv4 DNS*. Or from the server:

```bash
TOKEN=$(curl -sX PUT http://169.254.169.254/latest/api/token -H "X-aws-ec2-metadata-token-ttl-seconds: 60")
curl -s -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/public-hostname
```

An Elastic IP would keep the address stable, but it's rarely worth it for a throwaway.

## Troubleshooting

- **Hangs**: using `https://`, port 5000 not open in the security group, or your network blocks the port (try a phone hotspot).
- **Connection refused**: app not running (`ss -tlnp | grep 5000`).
- **404**: missing the `/ifn653` prefix. The full path is `/ifn653/fexchange/<student>/<contentid>`.

## Tear down

Terminate the instance, then delete the security group and key pair if you won't reuse them. The README's example URLs use an old hostname and omit the prefix, so treat them as illustrative.
