-- Lua script for wrk load testing
-- This script performs POST requests to the /predict/ endpoint

wrk.method = "POST"
wrk.headers["Content-Type"] = "application/json"

-- Sample iris data for prediction
wrk.body = '{"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2}'

-- Response handling (optional, for debugging)
response = function(status, headers, body)
  if status ~= 200 then
    print("Error: Status " .. status)
  end
end
