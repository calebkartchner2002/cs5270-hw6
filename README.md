# CS5270 AWS HW

## Buckets
bucket 1 = usu-cs5270-sky-dist
bucket 2 = usu-cs5270-sky-requests = where requests are stored
bucket 3 = usu-cs5270-sky-web = website

## Quick Commands
consumer for `s3`: `python consumer.py --backend s3 --requests-bucket usu-cs5270-sky-requests --widgets-bucket usu-cs5270-sky-web`
consumer for `ddb`: `python consumer.py --backend ddb --requests-bucket usu-cs5270-sky-requests --widgets-table widgets`

## Running Tests
`pytest -q`