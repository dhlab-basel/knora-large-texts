#!/usr/bin/env python3

import requests

json = """{
      "knora-api:mappingHasName": "LinguisticMapping",
      "knora-api:attachedToProject": {
          "@id": "http://rdfh.ch/projects/00FD"
      },
      "rdfs:label": "Linguistic Mapping",
      "@context": {
          "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
          "xsd" : "http://www.w3.org/2001/XMLSchema#",
          "knora-api": "http://api.knora.org/ontology/knora-api/v2#"
      }
}"""

url = "http://0.0.0.0:3333/v2/mapping"

files = {
    "json": (
        "request.json",
        json,
        "application/json"
    ),
    "xml": (
        "linguistic-mapping.xml",
        open("linguistic-mapping.xml", "rb"),
        "application/xml"
    )
}

r = requests.post(url, files=files, auth=("root@example.com", "test"))
print(r.text)
