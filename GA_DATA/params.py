api_url = "<apiUrl>"
token = "<token>"
body = {
  "dateRanges": [
    {
      "startDate": "2026-03-01",
      "endDate": "2026-03-01"
    }
  ],
  "dimensions": [
    { "name": "date" },
    { "name": "country" },
    { "name" : "city"},
    { "name" : "region"},
    { "name": "pagePath" },
    { "name": "sessionDefaultChannelGroup" }
  ],
  "metrics": [
    { "name": "activeUsers" },
    { "name": "sessions" },
    { "name": "engagementRate" },
    { "name": "eventCount" },
    { "name": "keyEvents" },
    { "name": "engagedSessions" },
    { "name": "averageSessionDuration" },
    { "name": "eventsPerSession" }
  ],
  "limit": 100000
}

host="localhost"
database="testdb"
user="postgres"
password=""
