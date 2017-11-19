package main

import "encoding/json"

import "github.com/gin-gonic/gin"
import "github.com/go-redis/redis"

type CommonWord struct {
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
	URL         string       `json:"url"`
	Title       string       `json:"title"`
	Description string       `json:"desc"`
	Story       string       `json:"story"`
	CommonNouns []CommonWord `json:"commonNouns"`
	CommonAdjs  []CommonWord `json:"commonAdj"`
	Names       []string     `json:"names"`
}

func main() {
	// Initialize app
	r := gin.Default()

	// Configure Middleware
	r.Use(gin.Logger())
	r.Use(gin.Recovery())

	// Static Files to serve
	r.Static("/static", "./dist/static")
	r.LoadHTMLFiles("dist/index.html")

	// Redis Client
	client := redis.NewClient(&redis.Options{
		Addr:     "redis:6379",
		Password: "",
		DB:       0,
	})

	// Routes
	r.GET("/", func(c *gin.Context) {
		c.HTML(200, "index.html", nil)
	})
	r.GET("/stories", func(c *gin.Context) {
		img, err := client.Keys("*").Result()
		c.JSON(200, gin.H{
			"message": img,
			"other":   err,
		})
	})
	r.GET("/stories", func(c *gin.Context) {
		key, err := client.RandomKey().Result()

		if err != nil {
			c.JSON(500, gin.H{
				"message": err,
			})

			return
		}

		value, _ := client.Get(key).Result()

		res := Story{}
		json.Unmarshal([]byte(value), &res)

		res2 := FmtStory{}

		res2.Title = res.Title
		res2.Description = res.Description
		res2.Story = res.Story
		res2.Image = "https://media.giphy.com/media/l41m0CPz6UCnaUmxG/giphy.gif"

		c.JSON(200, gin.H{
			"data": []FmtStory{res2},
		})
	})
	r.Run()
}
