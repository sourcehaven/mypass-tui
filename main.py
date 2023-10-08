import argparse

from src.model.shared import set_url
from src.ui.app import MyPassApp


def main(host: str, port: str):
    base_url = f'{host}:{port}'

    set_url(
        f'{base_url}/api/auth/',
        f'{base_url}/api/db/vault/'
    )

    app = MyPassApp()
    app.run()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("host", type=str, help="API host")
    parser.add_argument("port", type=int, help="API port")

    args = parser.parse_args()

    main(args.host, args.port)
