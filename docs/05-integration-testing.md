# Local Integration Testing

If you would like to test your scraper locally with the 
[frontend](https://github.com/pgh-public-meetings/events),
you can follow these steps.

## 1. Clean up previous scraper results
Local calls to `scrapy crawl` store results in a
folder named `output`, in the root of the repository.
You may wish to first clean up this directory by
simply removing it (it will be regenerated by 
subsequent runs to `scrapy crawl`).

## 2. Generate spider results
Use `scrapy crawl` to generate results for your spider:
```
scrapy crawl <scraper_name>
```
This should store results in the `output` directory in the
root of your repository.

## 3. Aggregate spider results
The frontend requires that all spider results be aggregated
together into one file. This can be generated using the
`combinefeeds` scrapy command:
```
scrapy combinefeeds
```
This should produce files named `upcoming.json` and
`latest.json` in your `output` directory.

## 4. Host your spider results locally
The frontend reads normally meeting events from an AWS
S3 bucket (or Azure Blob Storage, in other configurations).
However, for local testing, we would like the frontend
to read from our local version of `upcoming.json`.

One simple way to accomplish this is to standup
a very simple HTTP server locally that hosts our
spider `output` directory. This can be done with the
`serve.py` script in this repository:

```
python serve.py <spider_output_dir> <port>
```

E.g.

```
python serve.py output 8000
```

You should see output like:
```
Serving directory 'output' at: http://localhost:8000
```
Your scraper outputs can now be fetched from this endpoint.
You can open the URL logged by the script in your browser to try it yourself!

## 4.Standup the Frontend
Next, you will need to start an instance of the front end,
locally. The [frontend repository](https://github.com/pgh-public-meetings/events)
has instructions about how to do this. The basic steps are:
- Install [Node.js](https://nodejs.org/en/)
- Clone the front end repo locally.
- `npm install` inside the cloned repo.
- `npm start` to launch the frontend.

However, we need to add one more step: we need to point
the frontend to our locally hosted spider results.
To do so, before launching the frontend,
edit [config.js](https://github.com/pgh-public-meetings/events/blob/master/src/config.js)
, by setting the `EVENT_SOURCE` field to the
URL returned by `serve.py` (step 3 above):
```
  EVENT_SOURCE:
    "http://localhost:8000/upcoming.json",
```
Leave the rest of this config file the same.
Now, when you launch your frontend (`npm start`),
you should see the results from your local 
spider run in the calendar view!
