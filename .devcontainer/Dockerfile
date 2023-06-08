ARG VARIANT=bullseye
FROM mcr.microsoft.com/vscode/devcontainers/base:0-${VARIANT}
RUN export DEBIAN_FRONTEND=noninteractive \
***REMOVED*** && apt-get update && apt-get install -y xdg-utils \
***REMOVED*** && apt-get clean -y && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /opt/microsoft/azd \
***REMOVED*** && curl -L https://github.com/Azure/azure-dev/releases/download/azure-dev-cli_0.9.0-beta.2/azd-linux-arm64-beta.tar.gz | tar zxvf - -C /opt/microsoft/azd \
***REMOVED*** && ln -s /opt/microsoft/azd/azd-linux-arm64 /usr/local/bin/azd
