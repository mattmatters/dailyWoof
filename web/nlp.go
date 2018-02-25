package main

import (
	"math/rand"
	"regexp"
	"strings"
	"time"
)

// Utility function for random int in range
func random(min, max int) int {
	if min == 0 && max == 0 {
		return 0
	}

	rand.Seed(time.Now().UnixNano())
	return rand.Intn(max-min) + min
}

// Returns map keyed by original words and replace words
func matchWords(dic PersonConfig, story Story) map[string]string {
	bible := make(map[string]string)

	for _, noun := range story.CommonNouns {
		if noun.Count <= 1 {
			continue
		}

		i := random(0, len(dic.Nouns))
		word := dic.Nouns[i]

		bible[noun.Singular] = word[0]
		bible[noun.Plural] = word[1]
	}

	for _, adjective := range story.CommonAdjs {
		if adjective.Count <= 1 {
			continue
		}

		i := random(0, len(dic.Adjectives))
		word := dic.Adjectives[i]
		bible[adjective.Word] = word
	}

	for _, name := range story.Names {
		i := random(0, len(dic.Name))
		bible[name.Word] = dic.Name[i]
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

	reg := "(" + strings.Join(regWords, "|") + ")" + "[ ,'" + regexp.QuoteMeta(".") + "]"
	regex := regexp.MustCompile(reg)
	replFunc := func(word string) string {
		// Remove the end character
		i := word[0 : len(word)-1]
		return bible[i] + string(word[len(word)-1])
	}
	var retStory FmtStory

	retStory.Title = regex.ReplaceAllStringFunc(story.Title, replFunc)
	retStory.Description = regex.ReplaceAllStringFunc(story.Description, replFunc)
	retStory.Story = regex.ReplaceAllStringFunc(story.Story, replFunc)
	retStory.Image = story.Image

	return retStory
}

// Entrance point
func NatLangProcess(dic PersonConfig, story Story) FmtStory {
	bible := matchWords(dic, story)
	return ReplaceWords(bible, story)
}
