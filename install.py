#!/usr/bin/env python3
"""
GALIAS Installation Script
Automatically installs GALIAS and configures PATH on Windows/macOS/Linux
"""

import os
import sys
import subprocess
import platform
import site
from pathlib import Path


def run_command(cmd, check=True):
    """Run a command and return the result."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=check)
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    except subprocess.CalledProcessError as e:
        return e.stdout, e.stderr, e.returncode


def get_scripts_dir():
    """Get the Python scripts directory."""
    if platform.system() == "Windows":
        scripts_dir = os.path.join(site.USER_BASE, "Scripts")
    else:
        scripts_dir = os.path.join(site.USER_BASE, "bin")
    return scripts_dir


def is_in_path(directory):
    """Check if directory is in PATH."""
    path_dirs = os.environ.get("PATH", "").split(os.pathsep)
    return directory in path_dirs


def add_to_path_windows(scripts_dir):
    """Add directory to Windows PATH."""
    print(f"📝 Adding {scripts_dir} to Windows PATH...")
    
    # Use PowerShell to add to user PATH
    ps_command = f'''
    $currentPath = [Environment]::GetEnvironmentVariable("PATH", "User")
    if ($currentPath -notlike "*{scripts_dir}*") {{
        $newPath = $currentPath + ";{scripts_dir}"
        [Environment]::SetEnvironmentVariable("PATH", $newPath, "User")
        Write-Output "PATH updated successfully"
    }} else {{
        Write-Output "Directory already in PATH"
    }}
    '''
    
    stdout, stderr, returncode = run_command(f'powershell -Command "{ps_command}"', check=False)
    
    if returncode == 0:
        print("✅ PATH updated successfully!")
        print("⚠️  Please restart your terminal for changes to take effect.")
        return True
    else:
        print(f"❌ Failed to update PATH automatically: {stderr}")
        print(f"📋 Please manually add this to your PATH: {scripts_dir}")
        return False


def add_to_path_unix(scripts_dir):
    """Add directory to Unix PATH (macOS/Linux)."""
    shell = os.environ.get("SHELL", "/bin/bash")
    
    if "zsh" in shell:
        rc_file = Path.home() / ".zshrc"
    elif "fish" in shell:
        rc_file = Path.home() / ".config" / "fish" / "config.fish"
    else:
        rc_file = Path.home() / ".bashrc"
    
    export_line = f'export PATH="$PATH:{scripts_dir}"'
    
    try:
        # Check if already in rc file
        if rc_file.exists():
            content = rc_file.read_text()
            if scripts_dir in content:
                print("✅ Directory already in PATH configuration")
                return True
        
        # Add to rc file
        with open(rc_file, "a") as f:
            f.write(f"\n# Added by GALIAS installer\n{export_line}\n")
        
        print(f"✅ Added to {rc_file}")
        print("⚠️  Please restart your terminal or run: source ~/.bashrc")
        return True
        
    except Exception as e:
        print(f"❌ Failed to update PATH automatically: {e}")
        print(f"📋 Please manually add this to your shell config: {export_line}")
        return False


def install_galias():
    """Install GALIAS package."""
    print("📦 Installing GALIAS...")
    
    # Install with --user flag
    stdout, stderr, returncode = run_command(f"{sys.executable} -m pip install --user .")
    
    if returncode == 0:
        print("✅ GALIAS installed successfully!")
        return True
    else:
        print(f"❌ Installation failed: {stderr}")
        return False


def create_wrapper_script():
    """Create a wrapper script that works immediately."""
    if platform.system() == "Windows":
        # Create galias.bat in the same directory as the project
        wrapper_content = '''@echo off
python -c "import sys; sys.path.insert(0, r'%~dp0'); import improvctl; improvctl.main()" %*
'''
        wrapper_path = Path("galias.bat")
        wrapper_path.write_text(wrapper_content)
        print(f"✅ Created wrapper script: {wrapper_path.absolute()}")
        return str(wrapper_path.absolute())
    else:
        # Create galias shell script for Unix systems
        wrapper_content = '''#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 -c "import sys; sys.path.insert(0, '$SCRIPT_DIR'); import improvctl; improvctl.main()" "$@"
'''
        wrapper_path = Path("galias")
        wrapper_path.write_text(wrapper_content)
        wrapper_path.chmod(0o755)  # Make executable
        print(f"✅ Created wrapper script: {wrapper_path.absolute()}")
        return str(wrapper_path.absolute())


def test_installation():
    """Test if galias command works."""
    print("🧪 Testing installation...")

    # Test the wrapper script
    if platform.system() == "Windows":
        test_cmd = "galias.bat --version"
    else:
        test_cmd = "./galias --version"

    stdout, stderr, returncode = run_command(test_cmd, check=False)

    if returncode == 0:
        print("✅ GALIAS wrapper script works!")
        print(f"📋 Version: {stdout}")
        return True
    else:
        print(f"⚠️  Wrapper script test failed: {stderr}")
        return False


def create_env_file():
    """Create .env file from example if it doesn't exist."""
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if not env_file.exists() and env_example.exists():
        print("📝 Creating .env file from template...")
        env_file.write_text(env_example.read_text())
        print("✅ .env file created!")
        print("⚠️  Please edit .env with your ImprovMX API key and domain")
        return True
    elif env_file.exists():
        print("✅ .env file already exists")
        return True
    else:
        print("⚠️  No .env.example found")
        return False


def main():
    """Main installation process."""
    print("🚀 GALIAS Installation Script")
    print("=" * 40)

    # Step 1: Install package (optional, for completeness)
    print("📦 Installing GALIAS package...")
    install_galias()  # Don't exit on failure, wrapper will work anyway

    # Step 2: Create wrapper script (works immediately)
    wrapper_path = create_wrapper_script()

    # Step 3: Create .env file
    create_env_file()

    # Step 4: Test installation
    test_installation()

    print("\n🎉 Installation Complete!")
    print("=" * 40)
    print("📋 Usage:")
    if platform.system() == "Windows":
        print("   galias.bat --version")
        print("   galias.bat list")
        print("   galias.bat add")
        print("   galias.bat delete")
    else:
        print("   ./galias --version")
        print("   ./galias list")
        print("   ./galias add")
        print("   ./galias delete")

    print("\n📝 Next steps:")
    print("1. Edit .env with your ImprovMX API key and domain")
    print("2. Start using GALIAS with the commands above!")
    print(f"\n💡 Wrapper script location: {wrapper_path}")
    print("   You can copy this to any directory in your PATH for global access")


if __name__ == "__main__":
    main()
