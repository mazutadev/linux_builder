from app.core.application import get_application
from pprint import pprint


def main():
    app = get_application()

    container = app.docker_service.run_container(
        image="nginx:latest",
        ports={"80/tcp": 8080},
    )

    logs = app.docker_service.get_logs(container.id)


if __name__ == "__main__":
    main()
