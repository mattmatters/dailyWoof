package main

type Dictionary struct {
	Names      []Name
	Nouns      []Noun
	Adjectives []Adjective
}

type Noun struct {
	Singular string `json:"singular"`
	Plural   string `json:"plural"`
	Count    int    `json:"count"`
}

type Adjective struct {
	Word  string `json:"word"`
	Count int    `json:"count"`
}

type Name struct {
	Word string `json:"name"`
}

type FmtStory struct {
	Title       string `json:"title"`
	Description string `json:"description"`
	Story       string `json:"story"`
	Image       string `json:"image"`
}

type Story struct {
	URL         string      `json:"url"`
	Title       string      `json:"title"`
	Description string      `json:"desc"`
	Story       string      `json:"story"`
	CommonNouns []Noun      `json:"commonNouns"`
	CommonAdjs  []Adjective `json:"commonAdj"`
	Names       []Name      `json:"names"`
	Image       string      `json:"image"`
}
