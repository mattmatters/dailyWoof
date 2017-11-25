package main

import (
	"math/rand"
	"regexp"
	"strings"
	"time"
)

// Utility function for random int in range
func random(min, max int) int {
	rand.Seed(time.Now().UnixNano())
	return rand.Intn(max-min) + min
}

// Returns map keyed by original words and replace words
func matchWords(dic Dictionary, story Story) map[string]string {
	bible := make(map[string]string)

	for _, noun := range story.CommonNouns {
		if noun.Count <= 1 {
			continue
		}

		i := random(0, len(dic.Nouns))
		word := dic.Nouns[i]

		bible[noun.Singular] = word.Singular
		bible[noun.Plural] = word.Plural
	}

	for _, adjective := range story.CommonAdjs {
		if adjective.Count <= 1 {
			continue
		}

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
	for str, _ := range bible {
		regWords = append(regWords, regexp.QuoteMeta(str))
	}

	reg := strings.Join(regWords, "|")
	regex := regexp.MustCompile(reg)
	replFunc := func(word string) string {
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
