import os
from pathlib import Path

import xmltodict

CONFIG_FILE = Path("/config/config.xml")


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
    if not CONFIG_FILE.exists():
        raise FileNotFoundError(msg(f"{CONFIG_FILE} does not exist."))

    if not CONFIG_FILE.is_file():
        raise IsADirectoryError(msg(f"{CONFIG_FILE} is a directory."))

    if not os.access(CONFIG_FILE, os.W_OK):
        raise PermissionError(msg(f"{CONFIG_FILE} is not writable."))


def apply(app: str):
    print(
        msg(
            f"Applying {application.capitalize()} settings from environment variables..."
        )
    )

    config = xmltodict.parse(CONFIG_FILE.read_text())

    for setting, value in config["Config"].items():
        env_name = f"{app.upper()}_{setting.upper()}"

        if env_value := os.getenv(env_name):
            config["Config"][setting] = env_value
            print(msg(f'From ENV {env_name}: {setting}="{env_value}"'))

    new_xml = xmltodict.unparse(config, pretty=True).splitlines(keepends=True)[1:]
    CONFIG_FILE.open("w").writelines(new_xml)

    print(msg("Settings applied successfully."))


if __name__ == "__main__":
    application = get_app()
    check_config_file()
    apply(application)
