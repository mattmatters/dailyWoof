package main

import (
	"bufio"
	"encoding/csv"
	"io"
	"os"
)

func loadDictionary(dirPath string) (Dictionary, error) {
	nouns, err1 := loadNouns(dirPath + "/nouns.csv")
	adjectives, err2 := loadAdjectives(dirPath + "/adjectives.txt")
	names, err3 := loadNames(dirPath + "/names.txt")

	if err1 != nil {
		return Dictionary{}, err1
	} else if err2 != nil {
		return Dictionary{}, err2
	} else if err3 != nil {
		return Dictionary{}, err3
	}

	dic := Dictionary{
		Nouns:      nouns,
		Adjectives: adjectives,
		Names:      names,
	}

	return dic, nil
}

// Gets and parses all nouns in a file
func loadNouns(filePath string) ([]Noun, error) {
	var nouns []Noun

	// Load file
	f, fErr := os.Open(filePath)
	defer f.Close()

	if fErr != nil {
		return nouns, fErr
	}

	// Create a new reader.
	r := csv.NewReader(bufio.NewReader(f))
	for {
		record, err := r.Read()

		// Stop at EOF.
		if err == io.EOF {
			break
		}

		parsedNoun := Noun{
			Singular: record[0],
			Plural:   record[1],
			Count:    0,
		}

		nouns = append(nouns, parsedNoun)
	}

	return nouns, nil
}

// Gets and parses all adjectives in a file
func loadAdjectives(filePath string) ([]Adjective, error) {
	var adjectives []Adjective
	file, fErr := os.Open(filePath)
	defer file.Close()

	if fErr != nil {
		return adjectives, fErr
	}

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		adj := Adjective{Word: scanner.Text()}
		adjectives = append(adjectives, adj)

	}

	return adjectives, nil
}

// Gets and parses all names in a file
func loadNames(filePath string) ([]Name, error) {
	var names []Name
	file, fErr := os.Open(filePath)
	defer file.Close()

	if fErr != nil {
		return names, fErr
	}

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		name := Name{Word: scanner.Text()}
		names = append(names, name)

	}

	return names, nil
}
