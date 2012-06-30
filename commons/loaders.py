from os.path import join

from PySide.QtGui import QIcon
from PySide.phonon import Phonon

from yaml import load as parse_yaml
from yaml import dump

def get_config(config_dir, config_name):
    return parse_yaml(open(join(config_dir, config_name)))

def save_config(config_dir, config_name, config):
    open(join(config_dir, config_name), 'w').write(dump(config, default_flow_style=False))

def get_icon(icons_dir, icon_name):
    return QIcon(join(icons_dir, icon_name))

def get_sound(sounds_dir, sound_name):
    return Phonon.MediaSource(join(sounds_dir, sound_name))
