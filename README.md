## SES Watcher

A small tool to prevent AWS SES from blocked by exceeding Bounces Rate or Complaints Rate

## Installation

```bash
$ pip install seswatcher
```

## Usage

1. Step 1 : Get AWS Credentials with **AmazonSESFullAccess** policy
2. Step 2 : Verify sender email in AWS SES
3. Step 3 : Get a blackhole email address which receives un-important emails.
4. Step 4 : Create a hourly cronjob that runs **seswatcher**

```bash
$ seswatcher [OPTIONS] ACCESS_KEY SECRET_KEY FROM_EMAIL TO_EMAIL
```

## License

MIT Copyright (c) 2018 KhanhIceTea