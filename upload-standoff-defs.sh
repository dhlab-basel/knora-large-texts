#!/usr/bin/env bash

curl -X POST -H "Content-Type: application/trig" -d @linguistic-standoff.trig -u "root@example.com:test" "http://localhost:7200/repositories/knora-test/statements" | tee /dev/null
