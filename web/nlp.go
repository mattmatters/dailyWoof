package main

import (
	"fmt"
	"math/rand"
	"regexp"
	"time"
	"strings"
)

// Utility function for random int in range
func random(min, max int) int {
	rand.Seed(time.Now().Unix())
	return rand.Intn(max-min) + min
}

// Returns map keyed by original words and replace words
func matchWords(dic Dictionary, story Story) map[string]string {
	bible := make(map[string]string)

	for _, noun := range story.CommonNouns {
		i := random(0, len(dic.Nouns))
		word := dic.Nouns[i]

		bible[noun.Singular] = word.Singular
		bible[noun.Plural] = word.Plural
	}

	for _, adjective := range story.CommonAdjs {
		i := random(0, len(dic.Adjectives))
		word := dic.Adjectives[i]
		bible[adjective.Word] = word.Word
	}

	for _, name := range story.Names {
		i := random(0, len(dic.Names))
		bible[name.Word] = dic.Names[i].Word
	}

	return bible
}

// Main regex
func ReplaceWords(bible map[string]string, story Story) FmtStory {
	var regWords []string

	// Only want the matching values
	for str, str2 := range bible {
		fmt.Println(str + " " + str2)
		regWords = append(regWords, str)
	}

	reg := strings.Join(regWords, "|")
	fmt.Println(reg)
	regex := regexp.MustCompile(reg)

	replFunc := func (word string) string {
		fmt.Println(word)
		return bible[word]
	}
	var retStory FmtStory

	retStory.Title = regex.ReplaceAllStringFunc(story.Title, replFunc)
	retStory.Description = regex.ReplaceAllStringFunc(story.Description, replFunc)
	retStory.Story = regex.ReplaceAllStringFunc(story.Story, replFunc)
	retStory.Image = story.Image

	return retStory
}

// Entrance point
func NatLangProcess(dic Dictionary, story Story) FmtStory {
	bible := matchWords(dic, story)
	return ReplaceWords(bible, story)
}
