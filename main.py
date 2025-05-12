from app.core.application import get_application

from app.services.os_builder_service import OSBuildConfig


def main():
    app = get_application()

    app.os_builder.build_os(
        OSBuildConfig(
            name="my_custom_os",
            distro="ubuntu",
            release="latest",
            architecture="amd64",
            packages=["neofetch", "btop"],
        )
    )


if __name__ == "__main__":
    main()
