package main

type Noun struct {
	Singular string
	Plural   string
	Count    int
}

type Adjective struct {
	Word  string
	Count int
}

type Name struct {
	Word  string
	Count int
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
