import os
from pathlib import Path

import xmltodict

CONFIG_FILE_PATH = Path("/config/config.xml")


def msg(m: str):
    return f"[Envarr] {m}"


def get_app():
    apps = ["sonarr", "radarr", "lidarr", "readarr", "prowlarr"]

    try:
        return next((app for app in apps if Path(f"/app/{app}").exists()))
    except StopIteration:
        print(
            msg(
                f"Envarr is only compatible with LinuxServer.io's Sonarr, Radarr, Lidarr, Readarr, and "
                f"Prowlarr images, so it will have no effect here."
            )
        )
        exit(0)


def check_config_file():
    if not CONFIG_FILE_PATH.exists():
        raise FileNotFoundError(msg(f"{CONFIG_FILE_PATH} does not exist."))

    if not CONFIG_FILE_PATH.is_file():
        raise IsADirectoryError(msg(f"{CONFIG_FILE_PATH} is a directory."))

    if not os.access(CONFIG_FILE_PATH, os.W_OK):
        raise PermissionError(msg(f"{CONFIG_FILE_PATH} is not writable."))


def apply(app: str):
    config_file = Path("/config/config.xml")

    config = xmltodict.parse(config_file.read_text())

    for setting, value in config["Config"].items():
        env_name = f"{app.upper()}_{setting.upper()}"

        if env_value := os.getenv(env_name):
            config["Config"][setting] = env_value
            print(msg(f'From ENV {env_name}: {setting}="{env_value}"'))

    new_xml = xmltodict.unparse(config, pretty=True).splitlines(keepends=True)[1:]
    config_file.open("w").writelines(new_xml)

    print(msg("Settings applied successfully."))


if __name__ == "__main__":
    application = get_app()
    print(
        msg(
            f"Applying {application.capitalize()} settings from environment variables..."
        )
    )
    apply(application)
