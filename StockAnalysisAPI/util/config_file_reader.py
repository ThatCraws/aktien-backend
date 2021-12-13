import yaml

def readConfig(filePath, profile):
    with open(filePath, "r") as stream:
        try:
            configFileContent = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    return processConfigYaml(configFileContent, profile)

def processConfigYaml(configFileContent, profile):
    configs = configFileContent["configs"]

    config = getConfigForProfile(configs, profile)
    if config == None:
        print("Profile " + profile + " could not be found in config file")

    return config
    
        
def getConfigForProfile(configs, profile):
    for index, config in enumerate(configs):
        config = config["config"]
        if config["profile"] == profile:
            return config

    return None