package main

import (
	"encoding/json"
	"github.com/gin-gonic/gin"
	"github.com/go-redis/redis"
	"net/http"
	"time"
	"fmt"
)

func main() {
	// Wait for other processes to finish before starting
	time.Sleep(time.Duration(40 * time.Second))

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

	// Redis scripts
	RandVal := redis.NewScript(`
		local key = redis.call("RANDOMKEY")
		return redis.call("GET", key)
	`)
	RandVals := redis.NewScript(`
		local values = {}
		local valsToGet = ARGV[1]
		for i = 1, valsToGet do
		    local key = redis.call("RANDOMKEY")
		    local value = redis.call("GET", key)
		    values[i] = value
		end
		return values
	`)

	config, configErr := loadConfig("./config/config.json")

	if configErr != nil {
		panic(configErr)
	}

	// Routes
	r.GET("/", func(c *gin.Context) {
		c.HTML(http.StatusOK, "index.html", nil)
	})

	// We will be testing which version is more efficient, multiple queries that
	// asynchronously get processed, or a bulk query and then concurrently
	// processing the result
	r.GET("/stories", func(c *gin.Context) {
		var stories []FmtStory

		readingRainbow := make(chan FmtStory)

		for i := 0; i < 10; i++ {
			// Get story
			val, err := RandVal.Run(client, nil, nil).Result()

			if err != nil {
				c.JSON(500, gin.H{
					"message": err,
				})
				return
			}

			// Assert result
			castVal, ok := val.(string)

			if ok != true {
				c.JSON(500, gin.H{
					"message": ok,
				})
				return
			}

			// Start Concurrency
			go func() {
				// Marshal story
				story := Story{}
				json.Unmarshal([]byte(castVal), &story)

				// Process it
				if val, ok := config.People[story.Tag]; ok {
					readingRainbow <- NatLangProcess(val, story)
				} else {
					readingRainbow <- NatLangProcess(config.People["dmx"], story)
				}
			}()
		}

		// Recieve from channel
		for j := 0; j < 10; j++ {
			stories = append(stories, <-readingRainbow)
		}

		c.JSON(http.StatusOK, gin.H{
			"data": stories,
		})
	})
	r.GET("/stories2", func(c *gin.Context) {
		vals, err := RandVals.Run(client, nil, 10).Result()
		if err != nil {
			c.JSON(500, gin.H{
				"message": err,
			})

			return
		}

		c.JSON(http.StatusOK, gin.H{
			"message": vals,
		})
	})

	r.Run()
}
