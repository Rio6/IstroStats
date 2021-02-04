#!/bin/sh
pg_dump istrostats --column-inserts --file $@
