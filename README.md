# DLP_Lock 

## Installation 

```pip install gmpy2``` 

```pip install nprime```

## Description 

Uses the difficulty of the DLP problem to "lock" a passcode. 
That is, 

$$C = g^{passcode || salt} (mod \ p)$$

where C is the passcode locked, and salt is randomly generely generated number who's length is known.
C,p and the length of the salt is then saved.
The passcode || salt is then given by:

$$passcode || salt =DLP(C, g, p)$$

The passcode is extracted by removing the last k bits where k is the length of the salt.
