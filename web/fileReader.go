package main

import (
	"encoding/json"
	"io/ioutil"
)

func loadConfig(filePath string) (Config, error) {
	config := Config{}
	config.People = make(map[string]PersonConfig)

	data, err := ioutil.ReadFile(filePath)

	if err != nil {
		return config, err
	}

	err = json.Unmarshal([]byte(data), &config)

	return config, err
}
