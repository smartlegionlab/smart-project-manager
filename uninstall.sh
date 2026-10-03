#!/bin/bash
set -e

APP_ID="smart-project-manager"
INSTALL_DIR="$HOME/.local/share/$APP_ID"
APPS_DIR="$HOME/.local/share/applications"
MENU_ENTRY="$APPS_DIR/$APP_ID.desktop"
DESKTOP_FILE="$APP_ID.desktop"
USER_DATA_DIR="$HOME/.smart_project_manager"
USER_DATA_FILE="$USER_DATA_DIR/projects.json"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m'

info()  { echo -e "${GREEN}==>${NC} $*"; }
warn()  { echo -e "${YELLOW}==>${NC} $*"; }
error() { echo -e "${RED}==>${NC} $*" >&2; }
step()  { echo -e "${BOLD}${BLUE}[*]${NC} $*"; }

banner() {
    echo ""
    echo -e "${BOLD}${RED}==============================================${NC}"
    echo -e "${BOLD}${RED}  Smart Project Manager - Uninstaller${NC}"
    echo -e "${BOLD}${RED}==============================================${NC}"
    echo ""
}

banner

echo "Will remove:"
echo "  - Application:      $INSTALL_DIR"
echo "  - Menu entry:       $MENU_ENTRY"
echo "  - Desktop shortcut: ~/Desktop/$DESKTOP_FILE"
echo ""
echo -e "${BOLD}${GREEN}Your projects data is NOT touched.${NC}"
echo "  $USER_DATA_FILE"
echo ""

step "Removing application files..."
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    info "Removed: $INSTALL_DIR"
else
    warn "Not found: $INSTALL_DIR"
fi

step "Removing menu entry..."
if [ -f "$MENU_ENTRY" ]; then
    rm -f "$MENU_ENTRY"
    info "Removed: $MENU_ENTRY"
else
    warn "Not found: $MENU_ENTRY"
fi

step "Removing Desktop shortcut..."
DESKTOP_DIR="$(xdg-user-dir DESKTOP 2>/dev/null || true)"
[ -z "$DESKTOP_DIR" ] && DESKTOP_DIR="$HOME/Desktop"
if [ -f "$DESKTOP_DIR/$DESKTOP_FILE" ]; then
    rm -f "$DESKTOP_DIR/$DESKTOP_FILE"
    info "Removed: $DESKTOP_DIR/$DESKTOP_FILE"
else
    warn "Not found: $DESKTOP_DIR/$DESKTOP_FILE"
fi

if command -v update-desktop-database >/dev/null 2>&1; then
    update-desktop-database "$APPS_DIR" >/dev/null 2>&1 || true
fi

echo ""
echo -e "${BOLD}${GREEN}  Uninstall complete${NC}"
echo ""
echo "  Kept: $USER_DATA_FILE"
echo "  To delete projects data too: rm -rf $USER_DATA_DIR"
echo ""