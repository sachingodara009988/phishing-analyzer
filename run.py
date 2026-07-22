import os
import sys

# Find virtual env
possible_venvs = [
    os.path.join(os.path.dirname(__file__), ".venv"),
    os.path.join(os.path.dirname(__file__), "venv"),
    os.path.join(os.path.dirname(__file__), "backend", ".venv"),
    os.path.join(os.path.dirname(__file__), "backend", "venv"),
    "/opt/render/project/src/.venv",
    "/opt/render/project/src/backend/.venv",
]

venv_found = None
for path in possible_venvs:
    if os.path.isdir(path):
        # check site-packages directory
        # Linux style: lib/pythonX.Y/site-packages
        lib_dir = os.path.join(path, "lib")
        if os.path.isdir(lib_dir):
            for py_dir in os.listdir(lib_dir):
                sp = os.path.join(lib_dir, py_dir, "site-packages")
                if os.path.isdir(sp):
                    sys.path.insert(0, sp)
                    venv_found = path
                    break
        # Windows style: Lib/site-packages
        sp_win = os.path.join(path, "Lib", "site-packages")
        if os.path.isdir(sp_win):
            sys.path.insert(0, sp_win)
            venv_found = path
            
        if venv_found:
            # Also add bin/Scripts to path
            bin_path = os.path.join(path, "bin" if os.name != "nt" else "Scripts")
            os.environ["PATH"] = bin_path + os.path.pathsep + os.environ.get("PATH", "")
            break

print(f"Virtualenv path selected: {venv_found}")

# Add backend directory to sys.path
backend_path = os.path.join(os.path.dirname(__file__), "backend")
if os.path.isdir(backend_path):
    sys.path.insert(0, backend_path)

# Run uvicorn
import uvicorn
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    # We run "main:app" because "backend" is in sys.path
    uvicorn.run("main:app", host="0.0.0.0", port=port)
