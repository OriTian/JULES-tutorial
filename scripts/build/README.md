# Building and running JULES on the group's EC2 instance

The team provisioned a small AWS EC2 instance (Amazon Linux 2023, t3.micro) specifically for this purpose. All subsequent operations were performed within this SSH session.

## 1. Connect

```bash
chmod 400 your-key.pem
ssh -i your-key.pem ec2-user@<instance-public-dns>
```
