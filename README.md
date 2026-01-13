# pyIAX-Register

IAX2 Registration Server (Python)

Overview
- Listens for IAX2 registration packets and authenticates/registers
	nodes using pluggable backends. Successful registrations are optionally
	published as protobuf `update` messages to Kafka for consumption by
	other services (for example a DNS service).

Project layout
- `threaded_server.py` — UDP server entrypoint handling IAX2 packets.
- `iax2/` — IAX2 packet parsing and helpers.
- `register/` — registration backends (aslold, flatfile, dummy).
- `notify/` — notification backends (kafka, dummy).
- `dns_pb2.py` — generated protobuf bindings (included in-tree).
- `pyiax-reg.conf` — example configuration file.
- `useraccess.csv` — sample flatfile user database used by `flatfile` backend.

Prerequisites
- Python 3.8+
- A running Kafka cluster if you plan to use the `kafka` notify backend
- (optional) A MySQL-compatible database containing an ASL-style
	`user_Nodes` table if you use the `aslold` registration backend

Install

1. Create and activate a virtualenv and install requirements:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. The repository already includes `dns_pb2.py`. If you need to
	 regenerate it, obtain `dns.proto` from the DNS server project
	 (GitHub: https://github.com/Apprpt-Central/dnsserver) and run `protoc`.

Configuration

- `pyiax-reg.conf` contains defaults for command line options. You can
	either edit this file or pass options to `threaded_server.py`.
- Important options include:
	- `--register` — choose a registration backend (choices are the
		names in the `register/` package, e.g. `flatfile`, `aslold`, `dummy`).
	- `--notify` — choose a notification backend (e.g. `kafka`, `dummy`).
	- Backend-specific options are documented in each module's `help()`.

Running locally

Start the UDP server with a chosen register & notify backend. Examples:

Flatfile register (uses `useraccess.csv`):

```bash
python3 threaded_server.py --register flatfile --notify dummy
```

ASL DB register (MySQL):

```bash
python3 threaded_server.py --register aslold --notify kafka --db mysql+pymysql://user:pass@host/dbname
```

Notes on backends
- `register/flatfile.py` reads `useraccess.csv` by default; see its
	`help()` for the `--file` option.
- `register/aslold.py` connects via SQLAlchemy; pass `--db` to configure
	the SQLAlchemy URL.
- `notify/kafka.py` uses `confluent_kafka.Producer` and publishes
	serialized `update` protobuf messages to the configured topic.

Testing

- `get_info.py` is a small client script that sends an IAX INFO packet
	to a local server to help exercise parsing and responses.
- `threaded_server.py` runs the server directly and supports common
	command-line help for module-specific options.

Docker

Build and run with the provided Dockerfile:

```bash
docker build -t pyiax-register .
docker run --rm -it --network host pyiax-register python3 threaded_server.py --register flatfile
```

Security & notes
- The project includes example credentials and configuration files for
	testing (`useraccess.csv`, `pyiax-reg.conf`). Do not use these in
	production.
- When referencing the DNS server/protobufs, note that `dnsserver` is
	a separate GitHub project: https://github.com/Apprpt-Central/dnsserver

License

This project is licensed under the terms in `LICENSE`.
