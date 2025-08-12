# HCMUS - Computer Networks Projects

We are from [fit@hcmus](https://www.fit.hcmus.edu.vn/vn/). This repository collects our projects for the Computer Networks (CSC10008) course. It includes: a remote-control system driven by email, a UDP-based “Favorite Places” demo, Wireshark reports, and Packet Tracer labs.

### Table of contents
- 1. Remote Control PC via Email
- 2. Favorite Places (UDP)
- 3. Wireshark
- 4. Packet Tracer
- About us

---

## 1. Remote Control PC via Email
<h5 id="mail"></h5>

### 1.1 Overview
Client–server application that allows users to control remote PCs via commands sent by email. A control server polls an inbox via POP3, parses commands from mail subjects/bodies, executes actions on connected clients, and replies over SMTP.

Supported OS: The “victim” client and many features (registry, screen/webcam capture) require Windows.

### 1.2 Features
- Register controller email with a connected IP (authorization)
- List current connections and disconnect
- Process/app management: list, kill, start
- Screen and webcam capture (returns images/videos via email attachments)
- Keylogging (start/stop/print)
- System power: shutdown, logout, restart
- Windows Registry: list subtree, get/set value
- Directory operations: list and copy files

### 1.3 Quick start
1) Configure email credentials used by the control server
- Edit `socket_email/server_control/mail_provider_handle/env.py` and set `email`, `password` (SMTP: `smtp.office365.com:587`, POP3: `outlook.office365.com:995`).

2) Start the control server (receives client sockets and polls mailbox)
```bash
python -m socket_email.server_control.main
```

3) Start remote clients on Windows hosts to be controlled
```bash
python -m socket_email.victim.client
```

4) Send commands to the configured inbox from your controller address
- The server parses subjects/bodies and replies via email. Key examples:
  - Authorization and listing
    - `AUTH 1234 127.0.0.1:1337`
    - `LIST 1234`
    - `DISC`
  - App/Process
    - `LIST_PROC`
    - `LIST_APP`
    - `KILL <PID>`
  - Capture
    - `SCREENSHOT 10` (seconds)
    - `WEB 5` or `REC 5` (seconds)
    - `KEYLOG 10`
  - Registry and Directory
    - `REGISTRY LIST HKEY_LOCAL_MACHINE\SOFTWARE`
    - `REGISTRY UPDATE <absolute_path> <value> <REG_TYPE>`
    - `DIR LIST C:\Users`
    - `DIR COPY C:\src.txt C:\Dest\`
  - Power
    - `SHUTDOWN` | `LOGOUT` | `RESTART`

Notes:
- The AUTH key is `1234` by default and the endpoint format is `IPv4:port`.
- Some commands require a prior `AUTH` mapping to a live client.

### 1.4 Optional: Local GUI variant (telepc)
Run a local socket server on the remote machine, and connect using the GUI client.

Server (on remote/controlled machine):
```bash
python -m socket_email.telepc.server
```
Client (controller):
```bash
python -m socket_email.telepc.client
```

### 1.5 Dependencies (common)
- Python ≥ 3.10
- Windows-only features: `Pillow (PIL)`, `psutil`, `opencv-python`, `keyboard`, `pynput` and `tkinter` (bundled on many Python installs)

Install per host as needed, for example:
```bash
python -m pip install pillow psutil opencv-python keyboard pynput
```

---

## 2. Favorite Places (UDP)
<h5 id="sk"></h5>

### 2.1 Overview
Client–server demo using UDP with a simple ARQ-like protocol. The server serves a small places database (JSON); the client provides a Tkinter UI to browse places, fetch details, and download images/avatars. Multiple clients are supported.

### 2.2 Quick start
Server:
```bash
python -m socket_place.server.main
```

Client (Tkinter UI):
```bash
python -m socket_place.client.main
```

Optional: Regenerate the sample JSON database (writes `socket_place/server/db.json`):
```bash
python -m socket_place.server.create_db
```

### 2.3 Features
- Query all places (ID, name, number of images)
- Query a place’s detail (coordinates, description)
- Download avatar and gallery images per place
- Basic reliability over UDP with windowed acks

---

## 3. Wireshark
<h5 id="ws"></h5>

### 3.1 Requirements
See `Wireshark/Requirements/Wireshark-CNTN.docx`.

### 3.2 Description
Exercises capturing traffic when browsing to a website and analyzing provided `.pcapng` traces.

### 3.3 Details
Artifacts and LaTeX reports are in `Wireshark/`.

---

## 4. Packet Tracer
<h5 id="pt"></h5>

### 4.1 Requirements
See `packet-tracer/Requirements/20_6_Project3_PacketTracer (1).pdf`.

### 4.2 Description
Set up a small routed network in Packet Tracer with DHCP, DNS, and static routing exercises.

### 4.3 Details
Solutions and LaTeX reports are in `packet-tracer/`.

---

## Development

### Code style and docs
- Formatting, linting, and docstrings: Ruff
  - Format: `python -m ruff format .`
  - Lint & fix: `python -m ruff check . --fix`
  - Docstrings: we use concise, meaningful module/class/function docstrings

### Repository structure (high level)
- `socket_email/`: email-driven control server and Windows clients
  - `server_control/`: POP3/SMTP providers, command parser, handlers, TCP broker
  - `telepc/`: local GUI variant (server+client)
  - `victim/`: Windows client utilities (registry, live screen, webcam, etc.)
- `socket_place/`: UDP demo (server+client UI)
- `Wireshark/`: reports and packet captures
- `packet-tracer/`: Packet Tracer projects and LaTeX sources

Security notice: These projects control remote machines and interact with system resources. Run only on machines you own and understand. Do not expose servers to untrusted networks.

---

## About us
We are [Nguyen Van Loc](https://github.com/vanloc1808), [Vo Trong Nghia](https://github.com/mekanican), and [Nguyen Kieu Minh Tam](https://github.com/nkmt3x7x7x7), students in class CNTN2020, University of Science, VNUHCM.
