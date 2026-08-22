import os
import hashlib
import json
import sys
from pathlib import Path

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTreeView, QPushButton, QLabel, QMessageBox
)
from PySide6.QtGui import QStandardItemModel, QStandardItem, QColor, QFont
from PySide6.QtCore import Qt

# --- CONFIGURATION ---
def load_env(path=".env"):
    """Parse a .env file and return a dict of key-value pairs."""
    env = {}
    env_path = Path(path)
    if env_path.is_file():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            env[key.strip()] = value.strip().strip("\"'")
    return env


def load_sources(env_file=".env"):
    """Read SOURCE_<id> entries from .env and return a list of (Path, id) tuples."""
    env = load_env(env_file)
    sources = []
    for key, value in sorted(env.items()):
        if key.startswith("SOURCE_"):
            source_id = key[len("SOURCE_"):]
            sources.append((Path(value).expanduser(), source_id))
    if not sources:
        print("Warning: No SOURCE_ entries found in .env file. Create one from .env.example.")
    return sources


SOURCES = load_sources()

# State file stored in your destination repo to track last known status
STATE_FILE = Path("./sync-state.json").expanduser()

# Theme Colors
COLOR_NEW = "#4CAF50"      # Green
COLOR_MODIFIED = "#2196F3" # Blue
COLOR_DELETED = "#F44336"  # Red
COLOR_TEXT = "#E0E0E0"
COLOR_BG = "#1E1E1E"
COLOR_ACCENT = "#3A3A3A"

def get_file_hash(filepath):
    """Calculate SHA-256 hash of a file."""
    hasher = hashlib.sha256()
    try:
        if not filepath.is_file():
            return None
        with open(filepath, 'rb') as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
        return hasher.hexdigest()
    except Exception:
        return None

def load_state():
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                return json.loads(content) if content else {}
        except json.JSONDecodeError:
            print(f"[Error] Could not parse {STATE_FILE}.")
    return {}

def save_state(state):
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, indent=4)

def get_diff():
    state = load_state()
    seen_keys = []
    changes = {"new": [], "modified": [], "deleted": []}

    for source_root, source_id in SOURCES:
        source_root = source_root.expanduser()
        if not source_root.exists(): continue

        current_files = [f for f in source_root.rglob("*") if f.is_file()]
        for src_path in current_files:
            relative_path = str(src_path.relative_to(source_root))
            state_key = f"{source_id}:{relative_path}"
            seen_keys.append(state_key)
            
            current_hash = get_file_hash(src_path)
            if state_key not in state:
                changes["new"].append({"key": state_key, "path": src_path, "rel": relative_path, "id": source_id, "hash": current_hash, "type": "new"})
            elif state[state_key].get('hash') != current_hash:
                changes["modified"].append({"key": state_key, "path": src_path, "rel": relative_path, "id": source_id, "hash": current_hash, "type": "modified"})

    deleted_keys = set(state.keys()) - set(seen_keys)
    for k in deleted_keys:
        changes["deleted"].append({"key": k, "type": "deleted"})
    return state, changes

class SyncItem(QStandardItem):
    """Custom item that handles recursive checkbox toggling."""
    def __init__(self, text, data=None, is_folder=False):
        super().__init__(text)
        self.is_folder = is_folder
        self.sync_data = data
        self._is_updating = False 
        
        self.setCheckable(True)
        self.setCheckState(Qt.Checked) 
        
        if is_folder:
            font = QFont()
            font.setBold(True)
            self.setFont(font)

    def setData(self, value, role=Qt.EditRole):
        if role == Qt.CheckStateRole:
            new_state = Qt.CheckState(value)
            if new_state == self.checkState():
                return super().setData(value, role)
            
            if self._is_updating:
                return super().setData(value, role)
            
            self._is_updating = True
            try:
                for i in range(self.rowCount()):
                    child = self.child(i)
                    if isinstance(child, SyncItem):
                        child.setCheckState(new_state)
                
                result = super().setData(value, role)
                
                if self.parent():
                    self._update_parent_state(self.parent())
                return result
            finally:
                self._is_updating = False
        
        return super().setData(value, role)

    def _update_parent_state(self, parent):
        if not isinstance(parent, SyncItem) or parent._is_updating:
            return
            
        checked_count = 0
        unchecked_count = 0
        total = parent.rowCount()
        
        for i in range(total):
            state = parent.child(i).checkState()
            if state == Qt.Checked: checked_count += 1
            elif state == Qt.Unchecked: unchecked_count += 1
            
        if checked_count == total:
            new_state = Qt.Checked
        elif unchecked_count == total:
            new_state = Qt.Unchecked
        else:
            new_state = Qt.PartiallyChecked
            
        if parent.checkState() != new_state:
            parent._is_updating = True
            try:
                parent.setCheckState(new_state)
            finally:
                parent._is_updating = False
                
            if parent.parent():
                self._update_parent_state(parent.parent())

class CommitWindow(QMainWindow):
    def __init__(self, state, diff):
        super().__init__()
        self.state = state
        self.diff = diff
        self.setWindowTitle("Zensical Status Monitor")
        self.resize(1000, 700)
        
        font_family = "sans-serif"
        if sys.platform == "win32":
            font_family = "'Segoe UI', sans-serif"
        elif sys.platform == "darwin":
            font_family = "'SF Pro Text', 'Helvetica Neue', sans-serif"

        self.setStyleSheet(f"""
            QMainWindow, QWidget {{
                background-color: {COLOR_BG};
                color: {COLOR_TEXT};
                font-family: {font_family};
            }}
            QTreeView {{
                background-color: #252526;
                border: 1px solid #3F3F46;
                border-radius: 4px;
                outline: 0;
            }}
            QTreeView::item {{
                padding: 6px;
            }}
            QTreeView::item:hover {{
                background-color: #2D2D30;
            }}
            QPushButton {{
                background-color: {COLOR_ACCENT};
                border: none;
                padding: 8px 20px;
                border-radius: 4px;
                font-weight: bold;
            }}
            QPushButton#updateBtn {{
                background-color: {COLOR_NEW};
                color: white;
            }}
            QPushButton#updateBtn:hover {{
                background-color: #45a049;
            }}
            QPushButton:hover {{
                background-color: #4A4A4A;
            }}
            QLabel#title {{
                font-size: 18px;
                font-weight: bold;
            }}
        """)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        header_layout = QVBoxLayout()
        title = QLabel("Status Monitor")
        title.setObjectName("title")
        subtitle = QLabel("Identify changes in source folders and update tracking state.")
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        layout.addLayout(header_layout)

        self.view = QTreeView()
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["Name", "Status", "Relative Path"])
        self.view.setModel(self.model)
        self.view.setColumnWidth(0, 400)
        self.view.setColumnWidth(1, 100)
        self.view.setIndentation(20)
        layout.addWidget(self.view)

        self._populate_tree()

        footer = QHBoxLayout()
        self.status_lbl = QLabel("Ready")
        footer.addWidget(self.status_lbl)
        
        footer.addStretch()
        
        cancel_btn = QPushButton("Close")
        cancel_btn.clicked.connect(self.close)
        footer.addWidget(cancel_btn)
        
        update_btn = QPushButton("Acknowledge Changes")
        update_btn.setObjectName("updateBtn")
        update_btn.clicked.connect(self.perform_update)
        footer.addWidget(update_btn)
        
        layout.addLayout(footer)

    def _populate_tree(self):
        all_items = self.diff["new"] + self.diff["modified"] + self.diff["deleted"]
        structure = {}
        
        for item in all_items:
            sid = item.get("id") or item["key"].split(":")[0]
            if sid not in structure: structure[sid] = {}
            rel_path = item.get("rel", item["key"].split(":", 1)[-1])
            parts = Path(rel_path).parts
            
            curr = structure[sid]
            for part in parts[:-1]:
                if part not in curr or not isinstance(curr[part], dict):
                    curr[part] = {}
                curr = curr[part]
            curr[parts[-1]] = item

        def insert_recursive(parent_item, name, content):
            if isinstance(content, dict) and not ("type" in content and "key" in content):
                node = SyncItem(name, is_folder=True)
                parent_item.appendRow([node, QStandardItem("FOLDER"), QStandardItem("")])
                for k, v in sorted(content.items(), key=lambda x: (not isinstance(x[1], dict), x[0])):
                    insert_recursive(node, k, v)
            else:
                item = content
                name_node = SyncItem(name, data=item)
                
                status_node = QStandardItem(item["type"].upper())
                color = {"new": COLOR_NEW, "modified": COLOR_MODIFIED, "deleted": COLOR_DELETED}.get(item["type"], COLOR_TEXT)
                status_node.setForeground(QColor(color))
                
                path_node = QStandardItem(item.get("rel", ""))
                path_node.setForeground(QColor("#888888"))
                
                parent_item.appendRow([name_node, status_node, path_node])

        root_node = self.model.invisibleRootItem()
        for sid, content in sorted(structure.items()):
            source_node = SyncItem(f"Source: {sid}", is_folder=True)
            root_node.appendRow([source_node, QStandardItem("SOURCE"), QStandardItem("")])
            for k, v in sorted(content.items(), key=lambda x: (not isinstance(x[1], dict), x[0])):
                insert_recursive(source_node, k, v)
        
        self.view.expandAll()

    def get_selected_items(self):
        selected = []
        def walk(item):
            if isinstance(item, SyncItem) and not item.is_folder and item.checkState() == Qt.Checked:
                selected.append(item.sync_data)
            for i in range(item.rowCount()):
                walk(item.child(i))
        
        root = self.model.invisibleRootItem()
        for i in range(root.rowCount()):
            walk(root.child(i))
        return selected

    def perform_update(self):
        to_update = self.get_selected_items()
        if not to_update:
            QMessageBox.warning(self, "No Selection", "Please select at least one change to acknowledge.")
            return

        reply = QMessageBox.question(self, "Confirm Update", 
                                   f"Acknowledge {len(to_update)} changes? This will update the tracking state but will NOT copy any files.",
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            count = 0
            for item in to_update:
                key = item["key"]
                if item['type'] == "deleted":
                    if key in self.state:
                        del self.state[key]
                        count += 1
                else:
                    # Update state with the new hash/info without moving the file
                    self.state[key] = {
                        "source_id": item['id'], 
                        "relative_path": item['rel'], 
                        "hash": item['hash']
                    }
                    count += 1

            save_state(self.state)
            QMessageBox.information(self, "Success", f"State updated for {count} items.")
            self.close()

def main():
    state, diff = get_diff()
    if not any(diff.values()):
        print("Nothing to sync, working tree clean.")
        return
    
    app = QApplication(sys.argv)
    window = CommitWindow(state, diff)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()