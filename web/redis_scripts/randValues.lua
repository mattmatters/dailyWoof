--[[
   Basic Script for getting a bunch of random values.

   It's more efficient to do this all in Redis.
--]]

local values = {}
local valsToGet = ARGV[1]

for i = 1, valsToGet do
   local key = redis.call("RANDOMKEY")
   local value = redis.call("GET", key)
   values[i] = value
end

return values
