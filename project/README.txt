DISCOGRAPHY FETCHER
You give it and artist name, it gives you that artist's discography

root url = "https://cb361.herokuapp.com/fetch/<artist_name>"

Artist name can be provided a number of ways. For example:

- "The White Stripes"
- "the_white_stripes"
- "the white strips"

Have all worked in testing.

To accommodate artists who have released multiple albums in a single year,
this will return a dict of lists of dicts; yeah, you read that right.
Response will be sorted by release year. Take "Taylor Swift" for example.

{
  "2006": [
    {
      "name": "Taylor Swift",
      "type": "Album"
    }
  ],
  "2008": [								<- Year
    {
      "name": "Fearless",				<- [0] = Album1
      "type": "Album"
    },
    {
      "name": "Beautiful Eyes",			<- [1] = Album2
      "type": "EP"
    },
    {
      "name": "Picture to Burn",		<- [2] = Album3
      "type": "Single"
    }
  ],
  "2009": [
    {
      "name": "CMT Crossroads",
      "type": "Soundtrack"
    }
  ],
  "2010": [
    {
      "name": "Speak Now",
      "type": "Album"
    }
  ],
  "2012": [
    {
      "name": "Red",
      "type": "Album"
    }
  ],
  "2013": [
    {
      "name": "Everything Has Changed",
      "type": "Single"
    }
  ],
  "2014": [
    {
      "name": "1989",
      "type": "Album"
    }
  ],
  "2015": [
    {
      "name": "The 1989 World Tour",
      "type": "Broadcast"
    },
    {
      "name": "The Taylor Swift Megamix",
      "type": "Compilation"
    },
    {
      "name": "Greatest Hits",
      "type": "Compilation"
    }
  ],
  "2017": [
    {
      "name": "…Ready for It?",
      "type": "Single"
    },
    {
      "name": "reputation",
      "type": "Album"
    }
  ],
  "2019": [
    {
      "name": "Lover",
      "type": "Album"
    }
  ],
  "2020": [
    {
      "name": "folklore",
      "type": "Album"
    },
    {
      "name": "evermore",
      "type": "Album"
    }
  ],
  "2021": [
    {
      "name": "Fearless (Taylor’s version)",
      "type": "Album"
    }
  ]
} 