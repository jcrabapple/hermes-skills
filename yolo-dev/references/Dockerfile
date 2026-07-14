# yolo-sandbox: disposable container for AI coding agents
# Build once, reuse forever. Image is ~800MB.
#
# Build: podman build -t yolo-sandbox -f Dockerfile .
# Run:   podman run -d --rm -v /path/to/workspace:/workspace:Z -w /workspace yolo-sandbox sleep infinity

FROM docker.io/fedora:41

# System dependencies
RUN dnf install -y \
    nodejs22 \
    npm \
    python3 \
    python3-pip \
    git \
    curl \
    wget \
    gcc \
    gcc-c++ \
    make \
    procps-ng \
    findutils \
    && dnf clean all

# Gemini CLI (global install)
RUN npm install -g @google/gemini-cli

# Verify installations
RUN node --version \
    && python3 --version \
    && git --version \
    && gemini --version

# Default workspace
WORKDIR /workspace

# The container is meant to run sleep infinity, then accept podman exec commands
CMD ["sleep", "infinity"]
