# hs_aloha
This repository is a proposal of implementation for the Hierarchical Slotted ALOHA using python language

![aloha - Time-sequence diagram](aloha.png "Time-sequence diagram")


## Simulation variables
The simulation variables can be set as environment variables.
To do this you just need uncomment the fillowing lines in the `main.py` and change the values.

```python
# os.environ["SUBNETS"] = "2"
# os.environ["NODES_PER_NET"] = "2"
# os.environ["LOOPS"] = "1000"
# os.environ["GENERATE_INTERVAL"] = "100"
```

## How to use
```bash
# install dependencies
python3 -m pip install -r requirements.txt

# run the main file
python3 main.py
```

When executed a file called `aloha.log` will be created containing the log interactions.
```bash
# non collisons
DEBUG:root:SUBNET_0:GENERATING PACKAGES
DEBUG:root:SUBNET_0:MEMBER -> HEAD_NODE
DEBUG:root:BASE_STATION:HEAD_NODE -> BASE_STATION

# collisions
DEBUG:root:SUBNET_0:MEMBER COLLISION
DEBUG:root:SUBNET_0:HEAD_MEMBER COLLISION
DEBUG:root:BASE_STATION:HEAD_NODE COLLISION
```

Also a resume called `metrics.csv` will be generated containing metrics like:
```
|---------------|------------|----------------------|-------|----------|
| network       |  COLLISION |  GENERATING_PACKAGES |  IDLE |  SUCCESS |
|---------------|------------|----------------------|-------|----------|
|  BASE_STATION |       31.0 |                  0.0 | 318.0 |    151.0 |
|---------------|------------|----------------------|-------|----------|
|  SUBNET_0     |       31.0 |                  5.0 | 409.0 |     67.0 |
|---------------|------------|----------------------|-------|----------|
|  SUBNET_1     |       36.0 |                  5.0 | 415.0 |     64.0 |
|---------------|------------|----------------------|-------|----------|
|  SUBNET_2     |       26.0 |                  5.0 | 412.0 |     71.0 |
|---------------|------------|----------------------|-------|----------|
|  SUBNET_3     |       37.0 |                  5.0 | 411.0 |     63.0 |
|---------------|------------|----------------------|-------|----------|
|  SUBNET_4     |       31.0 |                  5.0 | 407.0 |     67.0 |
|---------------|------------|----------------------|-------|----------|
```

### References:
[T. Oku, T. Kimura and J. Cheng, "Performance Evaluation of Hierarchical Slotted ALOHA for IoT Applications," 2020 IEEE International Conference on Consumer Electronics - Taiwan (ICCE-Taiwan), 2020, pp. 1-2, doi: 10.1109/ICCE-Taiwan49838.2020.9258134.](paper.pdf)
