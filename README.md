# Envarr

Envarr is a mod for [LinuxServer.io](https://linuxserver.io)'s [Sonarr](https://docs.linuxserver.io/images/docker-sonarr),
[Radarr](https://docs.linuxserver.io/images/docker-radarr), [Lidarr](https://docs.linuxserver.io/images/docker-lidarr),
[Readarr](https://docs.linuxserver.io/images/docker-readarr), and [Prowlarr](https://docs.linuxserver.io/images/docker-prowlarr)
images that lets you configure the settings for those apps via environment variables.

Settings configured with Envarr take precedence over settings manually defined in the app's config file or via
the app's web UI.

## Installation

Set the container's `DOCKER_MODS` environment variable to `celsiusnarhwal/lscr-mods:universal-envarr`.

> [!WARNING]
> Despite `universal` being in the tag, this mod only works with the Sonarr, Radarr, Lidarr, Readarr, and Prowlarr
images.

```yaml
sonarr:  # or radarr, lidarr, etc.
    image: lscr.io/linuxserver/sonarr:latest  # or lscr.io/linuxserver/radarr:latest, lscr.io/linuxserver/lidarr:latest, etc.
    environment:
      - DOCKER_MODS=celsiusnarhwal/lscr-mods:universal-envarr
```

If you're using other mods in addition to this one, you can separate them with pipes (`|`). For example:

```yaml
sonarr:  # or radarr, lidarr, etc.
    image: lscr.io/linuxserver/sonarr:latest  # or lscr.io/linuxserver/radarr:latest, lscr.io/linuxserver/lidarr:latest, etc.
    environment:
      - DOCKER_MODS=celsiusnarhwal/lscr-mods:universal-envarr|linuxserver/mods:universal-cloudflared
```

## Usage

Each setting can be configured with an environment variable of the name `APPNAME_SETTING`, where `APPNAME` is one
of either `SONARR`, `RADARR`, `LIDARR`, `READARR`, or `PROWLARR` (all case-sensitive), and `SETTING` is the name
of the setting in all caps.

For example, to set Sonarr's `Port` setting to `6868`:

```yaml
sonarr:  # or radarr, lidarr, etc.
    image: lscr.io/linuxserver/sonarr:latest  # or lscr.io/linuxserver/radarr:latest, lscr.io/linuxserver/lidarr:latest, etc.
    environment:
      - DOCKER_MODS=celsiusnarhwal/lscr-mods:universal-envarr
      - SONARR_PORT=6868
```

`APPNAME` must actually be the name of the app in the container; environment variables beginning with `RADARR_`,
for instance, will have no effect in a Sonarr container.

Note that the `SETTING` part of the environment variable is always one word and is never separated with
underscores, even if the corresponding setting is verbally spoken as two words. For example, Sonarr's 
`AuthenticationMethod` setting is set via `SONARR_AUTHENTICATIONMETHOD` and **not** `SONARR_AUTHENTICATION_METHOD`.