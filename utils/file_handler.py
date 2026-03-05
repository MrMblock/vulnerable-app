"""File handling utilities with path traversal vulnerabilities."""
import os
import subprocess
import tempfile


def read_file(base_dir, filename):
    """Read a file - vulnerable to path traversal."""
    # No path sanitization
    path = os.path.join(base_dir, filename)
    with open(path, "r") as f:
        return f.read()


def process_file(filepath):
    """Process uploaded file - command injection via filename."""
    # Filename directly interpolated into shell command
    output = subprocess.check_output(
        f"file {filepath} && wc -l {filepath}",
        shell=True
    )
    return output.decode()


def save_temp_file(content, extension):
    """Save temporary file - no extension validation."""
    # Allows arbitrary file extensions (.py, .sh, .exe)
    tmp = tempfile.NamedTemporaryFile(
        suffix=f".{extension}",
        delete=False,
        mode="w"
    )
    tmp.write(content)
    tmp.close()
    return tmp.name


def cleanup_directory(path):
    """Clean up a directory - command injection."""
    os.system(f"rm -rf {path}")


def get_file_info(filename):
    """Get file info using shell - injection vulnerable."""
    info = os.popen(f"ls -la {filename}").read()
    return info
