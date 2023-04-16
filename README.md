# beancount-scripts

This repository contains code to work with my [Beancount](https://beancount.github.io/) ledger. It converts the ledger to various Pandas dataframes and then uploads the relevant data to InfluxDB, where it is read by Grafana.

## Local setup

In order to run this, you need to set the following values in a `.env` file in the root of the repo:

`BEANCOUNT_FILE` - The relative or absolute path to your Beancount ledger.

`INFLUXDB_HOST` - The URL of the InfluxDB host you want to upload to.

`INFLUXDB_TOKEN` - The token used to authenticate with the InfluxDB instance.