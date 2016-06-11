#!/usr/bin/env python3.5
import os
import shutil
import subprocess
import sys

import yaml


def main():
    if len(sys.argv) < 2:
        print("USAGE: python3 themeswitcher.py THEMENAME")
        sys.exit(1)

    config_filename = os.path.join(os.path.dirname(__file__), "config.yaml")
    with open(config_filename) as config_fileobj:
        config = yaml.safe_load(config_fileobj)

    for application_dict in config["colorschemes_to_install"]:
        ext = application_dict.get("extension",
                                   application_dict["folder_name"])
        if application_dict.get("use_suffix", True):
            dark_suffix = "." + \
                          ("light" if config["use_light_theme"] else "dark")
        else:
            dark_suffix = ""
        filename = "base16-{}{}".format(sys.argv[1], dark_suffix)
        path = os.path.join(config["builder_directory"], "output",
                            application_dict["folder_name"], filename)
        path = os.path.expanduser(path)

        if config["use_256_colors"] and os.path.exists(path + ".256." + ext):
            path += ".256." + ext
        else:
            path += "." + ext

        if not os.path.exists(path):
            raise ValueError("Could not find valid theme for " +
                             application_dict["folder_name"] +
                             " (tried " + repr(path) + ")")
        save_to = os.path.expanduser(application_dict["save_to"])
        shutil.copy2(path, save_to)

    for command in config["run_after_changing"]:
        subprocess.run([os.path.expanduser(x) for x in command])

if __name__ == "__main__":
    main()
