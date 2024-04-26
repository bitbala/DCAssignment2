import configparser

def getString(config_file, section, config_key):
    config = configparser.ConfigParser()
    config.read(config_file)
    config_value = config.get(section, config_key)

    return config_value

def getInt(config_file, section, config_key):
    config = configparser.ConfigParser()
    config.read(config_file)
    config_value = config.getint(section, config_key)

    return config_value


def getall (config_file, section):
    config = configparser.ConfigParser()
    config.read(config_file)
    return config.items(section)


def fetch_all_configs(config_file):
    all_configs = {}
    config = configparser.ConfigParser()
    config.read(config_file)
    for section in config.sections():
        for key, value in config.items(section):
            if value.isdigit():
                value = int(value)
            all_configs[key] = value
    return all_configs
