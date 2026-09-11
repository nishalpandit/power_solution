import os
import sys

# Ensure current project directory is on sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Auto-detect venv if running in an environment without uvicorn
try:
    import uvicorn
except ImportError:
    venv_python = os.path.join(os.path.dirname(os.path.abspath(__file__)), "venv", "Scripts", "python.exe")
    if os.path.exists(venv_python) and sys.executable.lower() != os.path.abspath(venv_python).lower():
        import subprocess
        result = subprocess.run([venv_python] + sys.argv)
        sys.exit(result.returncode)
    else:
        print("\n[ERROR] 'uvicorn' is not installed in your active Python environment.")
        print("Please activate your virtual environment or install dependencies:")
        print("    .\\venv\\Scripts\\activate")
        print("    pip install -r requirements.txt\n")
        sys.exit(1)


def main():
    args = sys.argv[1:]
    command = args[0] if args else "runserver"

    if command == "runserver":
        host = "127.0.0.1"
        port = 8000

        # Handle optional custom host/port (e.g. `python manage.py runserver 8001` or `0.0.0.0:8000`)
        if len(args) > 1:
            arg = args[1]
            if ":" in arg:
                host, port_str = arg.split(":", 1)
                port = int(port_str)
            else:
                try:
                    port = int(arg)
                except ValueError:
                    print(f"Invalid port: {arg}")
                    return

        print(f"\nPower Solution API running at: http://{host}:{port}")
        print(f"Interactive API Docs available at: http://{host}:{port}/docs\n")
        uvicorn.run("main:app", host=host, port=port, reload=True)
    else:
        print(f"Unknown command: '{command}'")
        print("Available commands:")
        print("  runserver [port]    Run the development server (default: 8000)")


if __name__ == "__main__":
    main()
