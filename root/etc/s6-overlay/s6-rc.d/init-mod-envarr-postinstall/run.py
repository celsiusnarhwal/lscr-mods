import os
from pathlib import Path

import xmltodict


def get_app():
    apps = ["sonarr", "radarr", "lidarr", "readarr", "prowlarr"]

    try:
        return next((app for app in apps if Path(f"/app/{app}").exists()))
    except StopIteration:
        raise RuntimeError(
            f"Envarr is only compatible with LinuxServer.io's Sonarr, Radarr, Lidarr, Readarr, and Prowlarr images."
        )


def apply(app: str):
    config_file = Path("/config/config.xml")

    config = xmltodict.parse(config_file.read_text())

    for setting, value in config["Config"].items():
        env_name = f"{app.upper()}_{setting.upper()}"

        if env_value := os.getenv(env_name):
            config["Config"][setting] = env_value
            print(f'From ENV {env_name}: {setting}="{env_value}"')

    new_xml = xmltodict.unparse(config, pretty=True).splitlines(keepends=True)[1:]
    config_file.open("w").writelines(new_xml)


if __name__ == "__main__":
    application = get_app()
    print(f"Applying {application.capitalize()} settings from environment variables...")
    apply(application)
