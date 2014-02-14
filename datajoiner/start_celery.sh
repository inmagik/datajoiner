#!/bin/bash

source ../env/bin/activate
celery -A datajoiner  worker -l info