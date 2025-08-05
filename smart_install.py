#!/usr/bin/env python3
"""
Smart installer that properly configures PATH for galias command
"""

import os
import sys
import subprocess
import platform
import site
from pathlib import Path


def run_command(cmd):
    """Run a command and return success status."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
        return True, result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return False, e.stderr.strip()


def get_scripts_dir():
    """Get the Python scripts directory."""
    if platform.system() == "Windows":
        return os.path.join(site.USER_BASE, "Scripts")
    else:
        return os.path.join(site.USER_BASE, "bin")


def add_to_windows_path(scripts_dir):
    """Add directory to Windows PATH using PowerShell."""
    # Create the directory if it doesn't exist
    os.makedirs(scripts_dir, exist_ok=True)
    
    ps_command = f'''
    $currentPath = [Environment]::GetEnvironmentVariable("PATH", "User")
    if ($currentPath -eq $null) {{ $currentPath = "" }}
    if ($currentPath -notlike "*{scripts_dir}*") {{
        $newPath = if ($currentPath) {{ "$currentPath;{scripts_dir}" }} else {{ "{scripts_dir}" }}
        [Environment]::SetEnvironmentVariable("PATH", $newPath, "User")
        
        # Also update current session
        $env:PATH = $env:PATH + ";{scripts_dir}"
        
        Write-Output "SUCCESS: Added to PATH"
    }} else {{
        Write-Output "ALREADY_EXISTS: Already in PATH"
    }}
    '''
    
    success, output = run_command(f'powershell -Command "{ps_command}"')
    if success and ("SUCCESS" in output or "ALREADY_EXISTS" in output):
        print(f"✅ {scripts_dir} configured in PATH")
        return True
    else:
        print(f"❌ Failed to configure PATH: {output}")
        return False


def main():
    """Main installation process."""
    print("🚀 GALIAS Smart Installer")
    print("=" * 40)
    
    # Step 1: Install package
    print("📦 Installing GALIAS...")
    success, output = run_command(f"{sys.executable} -m pip install --user .")
    
    if not success:
        print(f"❌ Installation failed: {output}")
        sys.exit(1)
    
    print("✅ GALIAS installed successfully!")
    
    # Step 2: Configure PATH
    scripts_dir = get_scripts_dir()
    print(f"🔧 Configuring PATH for: {scripts_dir}")
    
    if platform.system() == "Windows":
        path_success = add_to_windows_path(scripts_dir)
    else:
        # For Unix systems, just show instructions
        print(f"📋 Add this to your shell config: export PATH=\"$PATH:{scripts_dir}\"")
        path_success = True
    
    # Step 3: Create .env file
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if not env_file.exists() and env_example.exists():
        env_file.write_text(env_example.read_text())
        print("✅ .env file created")
    
    # Step 4: Test
    print("🧪 Testing installation...")
    
    # Test in a new process to pick up PATH changes
    test_success, test_output = run_command("galias --version")
    
    print("\n🎉 Installation Complete!")
    print("=" * 40)
    
    if test_success:
        print("✅ galias command works!")
        print(f"📋 {test_output}")
        print("\n📋 Usage:")
        print("   galias --version")
        print("   galias list")
        print("   galias add")
        print("   galias delete")
    else:
        print("⚠️  galias command test failed")
        print("💡 Try closing and reopening your terminal")
        print(f"📁 galias.exe should be in: {scripts_dir}")
    
    print("\n📝 Next steps:")
    print("1. Close and reopen your terminal")
    print("2. Edit .env with your API key and domain")
    print("3. Run: galias list")


if __name__ == "__main__":
    main()
