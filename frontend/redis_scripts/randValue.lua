local key = redis.call("RANDOMKEY")
return redis.call("GET", key)
