# codenames-server

local build command: docker build --rm  -f "Dockerfile" -t yochail/hebword2vec .
docker push yochail/hebword2vec
run locally (on port 8080): docker run -p 8080:80 word2vec

test localy: curl --location --request POST '0.0.0.0:8080/findcodesfromwords'
--header 'Content-Type: application/json'
--data-raw '{ "documents":[ { "text":"testtesttest" } ] }'
