from watchfiles import run_process

if __name__ == "__main__":
    run_process("./", target="poetry run python main.py")
