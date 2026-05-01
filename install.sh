#!/usr/bin/env bash
# Install mobilecore-trace-toolkit profiles into Wireshark's per-user
# personal-configuration directory on Linux or macOS.
#
# Usage:
#   ./install.sh                # symlink every profile (changes flow back into git)
#   ./install.sh --copy         # copy instead of symlinking (frozen snapshot)
#   ./install.sh --uninstall    # remove this toolkit's profiles
#
# By default, profiles are SYMLINKED so editing them in place updates this
# repo. Pass --copy if you would rather have a frozen snapshot in your
# Wireshark config dir.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROFILES_DIR="${REPO_ROOT}/profiles"

# Wireshark's personal-config dir.
#   Linux:   $XDG_CONFIG_HOME/wireshark or ~/.config/wireshark
#   macOS:   ~/.config/wireshark  (or ~/.wireshark on older versions)
detect_config_dir() {
    if [[ "$(uname -s)" == "Darwin" ]]; then
        if [[ -d "${HOME}/.config/wireshark" ]]; then
            echo "${HOME}/.config/wireshark"
        elif [[ -d "${HOME}/.wireshark" ]]; then
            echo "${HOME}/.wireshark"
        else
            echo "${HOME}/.config/wireshark"
        fi
    else
        echo "${XDG_CONFIG_HOME:-${HOME}/.config}/wireshark"
    fi
}

CONFIG_DIR="$(detect_config_dir)"
PROFILES_TARGET="${CONFIG_DIR}/profiles"

mode="symlink"
case "${1:-}" in
    --copy) mode="copy" ;;
    --uninstall) mode="uninstall" ;;
    --help|-h)
        sed -n '2,16p' "${BASH_SOURCE[0]}"
        exit 0
        ;;
    "") ;;
    *)
        echo "unknown option: $1" >&2
        exit 2
        ;;
esac

mkdir -p "${PROFILES_TARGET}"

for src in "${PROFILES_DIR}"/*/; do
    name="$(basename "${src}")"
    dst="${PROFILES_TARGET}/${name}"

    case "${mode}" in
        uninstall)
            if [[ -L "${dst}" || -d "${dst}" ]]; then
                rm -rf "${dst}"
                echo "removed   ${dst}"
            fi
            ;;
        copy)
            rm -rf "${dst}"
            cp -R "${src%/}" "${dst}"
            echo "copied    ${dst}"
            ;;
        symlink)
            rm -rf "${dst}"
            ln -s "${src%/}" "${dst}"
            echo "symlinked ${dst} -> ${src%/}"
            ;;
    esac
done

echo
case "${mode}" in
    uninstall) echo "done. removed mobilecore-trace-toolkit profiles from ${PROFILES_TARGET}" ;;
    *) echo "done. open Wireshark and pick a profile from the bottom-right of the status bar." ;;
esac
