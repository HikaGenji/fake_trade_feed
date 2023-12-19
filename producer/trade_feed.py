from kafka import KafkaProducer
import json
from random import sample
from entities import create_condition_codes, create_instrument, create_trade, flatten
import polars as pl
import os

n_instrument=int(os.getenv("n_instrument"))
connection = "risingwave://root:@risingwave:4566/dev"

# static data
instruments = [create_instrument() for _ in range(n_instrument)]
pl.from_dicts(instruments).write_database(table_name="universe",  connection=connection, if_table_exists= 'append')

condition_codes = flatten([create_condition_codes(instrument=instrument) for instrument in instruments])
pl.from_dicts(condition_codes).write_database(table_name="condition_codes",  connection=connection, if_table_exists= 'append')


# trade tick data
producer = KafkaProducer(bootstrap_servers=['redpanda:9092'], key_serializer=lambda m: json.dumps(m).encode('ascii'), 
                         value_serializer=lambda m: json.dumps(m).encode('ascii'))

print("connected to kafka")

while True:
    instrument = sample(instruments, 1)[0]
    trade = create_trade(instrument)
    producer.send('fake_trades', key = instrument['bbg_id'], value=trade)