#!/usr/bin/env bash
curl -s -H "Content-Type: application/json" -L -X POST --cookie-jar cookies -d @../../examples/auth/student.json http://localhost:8080/auth/ | python -m json.tool
curl -s -H "Content-Type: application/json" -L -X GET --cookie cookies http://localhost:8080/reservation/id/$1 | python -m json.tool