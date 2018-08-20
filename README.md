## SES Watcher

A small tool to prevent AWS SES from blocked by exceeding Bounces Rate or Complaints Rate

## Installation

```bash
$ pip install seswatcher
```

## Usage

Step 1 : Get AWS Credentials with **AmazonSESFullAccess** policy
Step 2 : Verify sender email in AWS SES
Step 3 : Get a blackhole email address which receives un-important emails.
Step 4 : Create a hourly cronjob that runs **seswatcher**

```bash
$ seswatcher [OPTIONS] ACCESS_KEY SECRET_KEY FROM_EMAIL TO_EMAIL
```

## License

MIT Copyright (c) 2018 KhanhIceTea