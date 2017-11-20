package main

import (
	"encoding/json"
	"github.com/gin-gonic/gin"
	"github.com/go-redis/redis"
	"net/http"
	"fmt"
	    "encoding/gob"
    "bytes"
)

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

	// Routes
	r.GET("/", func(c *gin.Context) {
		c.HTML(http.StatusOK, "index.html", nil)
	})
	r.GET("/stuff", func(c *gin.Context) {
		img, err := client.Keys("*").Result()
		c.JSON(http.StatusOK, gin.H{
			"message": img,
			"other":   err,
		})
	})
	// We will be testing which version is more efficient, multiple queries that
	// asynchronously get processed, or a bulk query and then concurrently
	// processing the result
	r.GET("/stories", func(c *gin.Context) {
		value, err := RandVal.Run(client, nil, nil).Result()

		if err != nil {
			c.JSON(500, gin.H{
				"message": err,
			})

			return
		}
		fmt.Println(value)
		res := Story{}
		test, ok := value.(string)

		if ok != true {
			c.JSON(500, gin.H{
				"message": ok,
			})
			return
		}

		json.Unmarshal([]byte(test), &res)

		res2 := FmtStory{
			Title: res.Title,
			Description: res.Description,
			Story: res.Story,
			Image: res.Image,
		}

		c.JSON(http.StatusOK, gin.H{
			"data": []FmtStory{res2},
		})
	})
	r.GET("/stories2", func(c *gin.Context) {
		stuff, err := RandVals.Run(client, nil, 10).Result()
		if err != nil {
			c.JSON(500, gin.H{
				"message": err,
			})

			return
		}

		c.JSON(http.StatusOK, gin.H{
			"message": stuff,
		})
	})

	r.Run()
}

func GetBytes(key interface{}) ([]byte, error) {
    var buf bytes.Buffer
    enc := gob.NewEncoder(&buf)
    err := enc.Encode(key)
    if err != nil {
	return nil, err
    }
    return buf.Bytes(), nil
}
