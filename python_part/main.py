import time
import pandas as pd
from random import random
from fastparquet import write

file = "/home/kir/Documents/prices.parquet"


def generate_movement():
    movement = -1 if random() < 0.5 else 1
    return movement


def next_price(p):
    return p + generate_movement()


def init():
    init_df = pd.DataFrame(columns=['id', 'price', 'time'])
    s_time = time.time()
    start_time = round(s_time)
    for i in range(100):
        init_df.loc[i] = [i, 0, start_time]
    time2 = time.time()
    print(f"{s_time}; {time2}")
    return init_df, s_time


def run():
    res, prev_time = init()
    res.to_parquet(file, index=False)
    curr_df = res

    while True:
        tm = time.time()
        t = round(tm)
        if t - prev_time > 0:
            curr_df.price = curr_df.apply(lambda x: next_price(x.price), axis=1)
            curr_df.time = t
            with open(file, mode="a+") as f:
                write(f.name, curr_df, write_index=False, append=True)
            print(f'{tm}, {time.time()}')
            prev_time = t
        time.sleep(0.2)


if __name__ == '__main__':
    try:
        run()
    except Exception as e:
        print(e)
        raise e
